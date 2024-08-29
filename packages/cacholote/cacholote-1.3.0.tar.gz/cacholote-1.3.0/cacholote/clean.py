"""Functions to clean cache database and files."""

# Copyright 2022, European Union.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import collections
import datetime
import posixpath
from typing import Any, Callable, Literal, Optional

import pydantic
import sqlalchemy as sa
import sqlalchemy.orm
from sqlalchemy import BinaryExpression, ColumnElement

from . import config, database, decode, encode, extra_encoders, utils

FILE_RESULT_KEYS = ("type", "callable", "args", "kwargs")
FILE_RESULT_CALLABLES = (
    "cacholote.extra_encoders:decode_xr_dataarray",
    "cacholote.extra_encoders:decode_xr_dataset",
    "cacholote.extra_encoders:decode_io_object",
)


def _get_files_from_cache_entry(cache_entry: database.CacheEntry) -> dict[str, str]:
    result = cache_entry.result
    if not isinstance(result, (list, tuple, set)):
        result = [result]

    files = {}
    for obj in result:
        if (
            isinstance(obj, dict)
            and set(FILE_RESULT_KEYS) == set(obj)
            and obj["callable"] in FILE_RESULT_CALLABLES
        ):
            fs, urlpath = extra_encoders._get_fs_and_urlpath(*obj["args"][:2])
            files[fs.unstrip_protocol(urlpath)] = obj["args"][0]["type"]
    return files


def _delete_cache_entry(
    session: sa.orm.Session, cache_entry: database.CacheEntry
) -> None:
    fs, _ = utils.get_cache_files_fs_dirname()
    files_to_delete = _get_files_from_cache_entry(cache_entry)
    logger = config.get().logger

    # First, delete database entry
    logger.info("deleting cache entry", cache_entry=cache_entry)
    session.delete(cache_entry)
    database._commit_or_rollback(session)

    # Then, delete files
    for urlpath, file_type in files_to_delete.items():
        if fs.exists(urlpath):
            logger.info("deleting cache file", urlpath=urlpath)
            fs.rm(urlpath, recursive=file_type == "application/vnd+zarr")


def delete(func_to_del: str | Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    """Delete function previously cached.

    Parameters
    ----------
    func_to_del: callable, str
        Function to delete from cache
    *args: Any
        Argument of functions to delete from cache
    **kwargs: Any
        Keyword arguments of functions to delete from cache
    """
    hexdigest = encode._hexdigestify_python_call(func_to_del, *args, **kwargs)
    with config.get().instantiated_sessionmaker() as session:
        for cache_entry in session.scalars(
            sa.select(database.CacheEntry).filter(database.CacheEntry.key == hexdigest)
        ):
            _delete_cache_entry(session, cache_entry)


class _Cleaner:
    def __init__(self, depth: int) -> None:
        self.logger = config.get().logger
        self.fs, self.dirname = utils.get_cache_files_fs_dirname()

        self.urldir = self.fs.unstrip_protocol(self.dirname)

        self.logger.info("getting disk usage")
        self.file_sizes: dict[str, int] = collections.defaultdict(int)
        for path, size in self.fs.du(self.dirname, total=False).items():
            # Group dirs
            urlpath = self.fs.unstrip_protocol(path)
            parts = urlpath.replace(self.urldir, "", 1).strip("/").split("/")
            if parts:
                self.file_sizes[posixpath.join(self.urldir, *parts[:depth])] += size
        self.disk_usage = sum(self.file_sizes.values())
        self.log_disk_usage()

    def pop_file_size(self, file: str) -> int:
        size = self.file_sizes.pop(file, 0)
        self.disk_usage -= size
        return size

    def log_disk_usage(self) -> None:
        self.logger.info("check disk usage", disk_usage=self.disk_usage)

    def stop_cleaning(self, maxsize: int) -> bool:
        return self.disk_usage <= maxsize

    def get_unknown_files(self, lock_validity_period: float | None) -> set[str]:
        self.logger.info("getting unknown files")

        utcnow = utils.utcnow()
        locked_files = set()
        for urlpath in self.file_sizes:
            if urlpath.endswith(".lock"):
                modified = self.fs.modified(urlpath)
                if modified.tzinfo is None:
                    modified = modified.replace(tzinfo=datetime.timezone.utc)
                delta = utcnow - modified
                if lock_validity_period is None or delta < datetime.timedelta(
                    seconds=lock_validity_period
                ):
                    locked_files.add(urlpath)
                    locked_files.add(urlpath.rsplit(".lock", 1)[0])

        if unknown_files := (set(self.file_sizes) - locked_files):
            with config.get().instantiated_sessionmaker() as session:
                for cache_entry in session.scalars(sa.select(database.CacheEntry)):
                    for known_file in _get_files_from_cache_entry(cache_entry):
                        unknown_files.discard(known_file)
                    if not unknown_files:
                        break
        return unknown_files

    def delete_unknown_files(
        self, lock_validity_period: float | None, recursive: bool
    ) -> None:
        unknown_files = self.get_unknown_files(lock_validity_period)
        for urlpath in unknown_files:
            self.pop_file_size(urlpath)
        self.remove_files(
            list(unknown_files),
            recursive=recursive,
        )
        self.log_disk_usage()

    @staticmethod
    @pydantic.validate_call
    def _get_tag_filters(
        tags_to_clean: Optional[list[Optional[str]]],
        tags_to_keep: Optional[list[Optional[str]]],
    ) -> list[sa.ColumnElement[bool]]:
        if (tags_to_clean is not None) and (tags_to_keep is not None):
            raise ValueError("tags_to_clean/keep are mutually exclusive.")

        filters = []
        if tags_to_keep is not None:
            filters.append(
                sa.or_(
                    database.CacheEntry.tag.not_in(tags_to_keep),
                    database.CacheEntry.tag.is_not(None)
                    if None in tags_to_keep
                    else database.CacheEntry.tag.is_(None),
                )
            )
        elif tags_to_clean is not None:
            filters.append(
                sa.or_(
                    database.CacheEntry.tag.in_(tags_to_clean),
                    database.CacheEntry.tag.is_(None)
                    if None in tags_to_clean
                    else database.CacheEntry.tag.is_not(None),
                )
            )
        return filters

    @staticmethod
    @pydantic.validate_call
    def _get_method_sorters(
        method: Literal["LRU", "LFU"],
    ) -> list[sa.orm.InstrumentedAttribute[Any]]:
        sorters: list[sa.orm.InstrumentedAttribute[Any]] = []
        if method == "LRU":
            sorters.extend(
                [database.CacheEntry.updated_at, database.CacheEntry.counter]
            )
        elif method == "LFU":
            sorters.extend(
                [database.CacheEntry.counter, database.CacheEntry.updated_at]
            )
        else:
            raise ValueError(f"{method=}")
        sorters.append(database.CacheEntry.expiration)
        return sorters

    def remove_files(
        self,
        files: list[str],
        max_tries: int = 10,
        **kwargs: Any,
    ) -> None:
        assert max_tries >= 1
        if not files:
            return

        self.logger.info("deleting files", n_files_to_delete=len(files), **kwargs)

        n_tries = 0
        while files:
            n_tries += 1
            try:
                self.fs.rm(files, **kwargs)
                return
            except FileNotFoundError:
                # Another concurrent process might have deleted files
                if n_tries >= max_tries:
                    raise
                files = [file for file in files if self.fs.exists(file)]

    def delete_cache_files(
        self,
        maxsize: int,
        method: Literal["LRU", "LFU"],
        tags_to_clean: list[str | None] | None,
        tags_to_keep: list[str | None] | None,
    ) -> None:
        filters = self._get_tag_filters(tags_to_clean, tags_to_keep)
        sorters = self._get_method_sorters(method)

        if self.stop_cleaning(maxsize):
            return

        files_to_delete = []
        dirs_to_delete = []
        self.logger.info("getting cache entries to delete")
        n_entries_to_delete = 0
        with config.get().instantiated_sessionmaker() as session:
            for cache_entry in session.scalars(
                sa.select(database.CacheEntry).filter(*filters).order_by(*sorters)
            ):
                files = _get_files_from_cache_entry(cache_entry)
                if any(file.startswith(self.urldir) for file in files):
                    n_entries_to_delete += 1
                    session.delete(cache_entry)

                    for file, file_type in files.items():
                        self.pop_file_size(file)
                        if file_type == "application/vnd+zarr":
                            dirs_to_delete.append(file)
                        else:
                            files_to_delete.append(file)

                if self.stop_cleaning(maxsize):
                    break

            if n_entries_to_delete:
                self.logger.info(
                    "deleting cache entries", n_entries_to_delete=n_entries_to_delete
                )
            database._commit_or_rollback(session)

        self.remove_files(files_to_delete, recursive=False)
        self.remove_files(dirs_to_delete, recursive=True)
        self.log_disk_usage()

        if not self.stop_cleaning(maxsize):
            raise ValueError(
                (
                    f"Unable to clean {self.dirname!r}."
                    f" Final disk usage: {self.disk_usage!r}."
                    f" Target disk usage: {maxsize!r}"
                )
            )


def clean_cache_files(
    maxsize: int,
    method: Literal["LRU", "LFU"] = "LRU",
    delete_unknown_files: bool = False,
    recursive: bool = False,
    lock_validity_period: float | None = None,
    tags_to_clean: list[str | None] | None = None,
    tags_to_keep: list[str | None] | None = None,
    depth: int = 1,
) -> None:
    """Clean cache files.

    Parameters
    ----------
    maxsize: int
        Maximum total size of cache files (bytes).
    method: str, default: "LRU"
        * LRU: Last Recently Used
        * LFU: Least Frequently Used
    delete_unknown_files: bool, default: False
        Delete all files that are not registered in the cache database.
    recursive: bool, default: False
        Whether to delete unknown directories or not
    lock_validity_period: float, optional, default: None
        Validity period of lock files in seconds. Expired locks will be deleted.
    tags_to_clean, tags_to_keep: list of strings/None, optional, default: None
        Tags to clean/keep. If None, delete all cache entries.
        To delete/keep untagged entries, add None in the list (e.g., [None, 'tag1', ...]).
        tags_to_clean and tags_to_keep are mutually exclusive.
    depth: int, default: 1
        depth for grouping cache files
    """
    cleaner = _Cleaner(depth=depth)

    if delete_unknown_files:
        cleaner.delete_unknown_files(lock_validity_period, recursive)

    cleaner.delete_cache_files(
        maxsize=maxsize,
        method=method,
        tags_to_clean=tags_to_clean,
        tags_to_keep=tags_to_keep,
    )


def clean_invalid_cache_entries(
    check_expiration: bool = True, try_decode: bool = False
) -> None:
    """Clean invalid cache entries.

    Parameters
    ----------
    check_expiration: bool
        Whether or not to delete expired entries
    try_decode: bool
        Whether or not to delete entries that raise DecodeError (this can be slow!)
    """
    filters = []
    if check_expiration:
        filters.append(database.CacheEntry.expiration <= utils.utcnow())
    if filters:
        with config.get().instantiated_sessionmaker() as session:
            for cache_entry in session.scalars(
                sa.select(database.CacheEntry).filter(*filters)
            ):
                _delete_cache_entry(session, cache_entry)

    if try_decode:
        with config.get().instantiated_sessionmaker() as session:
            for cache_entry in session.scalars(sa.select(database.CacheEntry)):
                try:
                    decode.loads(cache_entry._result_as_string)
                except decode.DecodeError:
                    _delete_cache_entry(session, cache_entry)


def expire_cache_entries(
    tags: list[str] | None = None,
    before: datetime.datetime | None = None,
    after: datetime.date | None = None,
    delete: bool = False,
) -> int:
    now = utils.utcnow()

    filters: list[BinaryExpression[bool] | ColumnElement[bool]] = []
    if tags is not None:
        filters.append(database.CacheEntry.tag.in_(tags))
    if before is not None:
        filters.append(database.CacheEntry.created_at < before)
    if after is not None:
        filters.append(database.CacheEntry.created_at > after)

    count = 0
    with config.get().instantiated_sessionmaker() as session:
        for cache_entry in session.scalars(
            sa.select(database.CacheEntry).filter(*filters)
        ):
            count += 1
            if delete:
                session.delete(cache_entry)
            else:
                cache_entry.expiration = now
        database._commit_or_rollback(session)
    return count
