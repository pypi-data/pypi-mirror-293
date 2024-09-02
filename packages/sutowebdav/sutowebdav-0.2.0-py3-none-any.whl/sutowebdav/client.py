#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2024. Suto-Commune
#  _
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  _
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  _
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
@File       : client.py

@Author     : hsn

@Date       : 2024/8/31 下午7:57
"""
import contextlib
import io
import tempfile
from dataclasses import dataclass
from datetime import datetime
from hashlib import md5
from os import PathLike
from typing import AsyncGenerator, Any, Iterable, AsyncIterable, Literal
from xml.etree import cElementTree

import httpx
from httpx import AsyncByteStream, SyncByteStream


@dataclass
class DavFile:
    name: str
    path: str
    size: int
    mtime: datetime
    content_type: str


def _parse_prop(elem, name, default=None):
    child = elem.find('.//{DAV:}' + name)
    return default if child is None else child.text


class NetworkException(Exception):
    def __init__(self, method, path, code, message):
        self.code = code
        self.message = message
        self.method = method
        self.path = path

    def __str__(self):
        return f"Request failed: {self.method} {self.path} {self.code} {self.message}"


class DavClient:
    def __init__(self, url: str, username: str | None = None, password: str | None = None, *, proxy=None, cwd='/',
                 **kwargs):
        self.url = url
        self.username = username
        self.password = password
        if username and password:
            auth = (username.encode('utf8'), password.encode('utf8'))
        else:
            auth = None

        self.http_client = httpx.AsyncClient(
            auth=auth,
            base_url=self.url,
            proxies=proxy,
            **kwargs)
        self.cwd = cwd
        if not self.cwd.endswith('/'):
            self.cwd = self.cwd + '/'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    async def request(self, method: str, path: str, expected_status_codes: tuple = (200,), **kwargs):
        if not path.startswith('/'):
            _path = self.cwd + path
        else:
            _path = self.cwd + path[1:]

        resp = await self.http_client.request(method, _path, **kwargs)
        if resp.status_code not in expected_status_codes:
            raise NetworkException(method, _path, resp.status_code, resp.text)
        return resp

    async def mkdir(self, path: str):
        await self.request('MKCOL', path, (201,))

    async def rmdir(self, path: str):
        await self.request('DELETE', path, (204,))

    async def upload(self, data: str | PathLike | bytes | Iterable[bytes] | AsyncIterable[bytes], path: str):
        if isinstance(data, bytes):
            data = data
        elif isinstance(data, Iterable | AsyncIterable):
            pass
        else:
            with open(data, 'rb') as f:
                data = f.read()

        await self.request('PUT', path, (201, 204), content=data)

    async def delete(self, path: str):
        await self.request('DELETE', path, (204,))

    async def is_exists(self, path: str) -> bool:
        resp = await self.request('HEAD', path, (200, 404))
        return resp.status_code == 200

    async def download(self, path: str, local_path: str):
        resp = await self.request('GET', path, (200,))
        with open(local_path, 'wb') as f:
            f.write(resp.content)

    async def download_stream(self, path: str) -> SyncByteStream | AsyncByteStream | None:
        resp = await self.request('GET', path, (200,))
        return resp.stream

    async def ls(self, path: str) -> AsyncGenerator[DavFile, Any]:
        resp = await self.request('PROPFIND', path, (207,), headers={'Depth': '1'})
        # print(resp.status_code, resp.content)
        tree = cElementTree.fromstring(resp.content)
        for elem in tree.findall('{DAV:}response'):
            name = _parse_prop(elem, 'displayname', '')
            path = _parse_prop(elem, 'href', '')
            size = int(_parse_prop(elem, 'getcontentlength', 0))
            mtime = datetime.strptime(_parse_prop(elem, 'getlastmodified', 'Thu, 1 Jan 1970 00:00:00 GMT'),
                                      '%a, %d %b %Y %H:%M:%S %Z')
            content_type = _parse_prop(elem, 'getcontenttype', 'directory')
            yield DavFile(name, path, size, mtime, content_type)

    async def walk(self, path: str) -> AsyncGenerator[DavFile, Any]:
        async for file in self.ls(path):
            if file.content_type == 'directory':
                async for f in self.walk(file.path):
                    yield f
            else:
                yield file

    @contextlib.asynccontextmanager
    async def open(self,
                   path: str,
                   mode: Literal['w', 'a', 'wb', 'ab'] = 'ab',
                   *,
                   decoding='utf-8') -> AsyncGenerator[io.IOBase, None]:
        assert mode in ('w', 'a', 'wb', 'ab')
        hasher = md5()
        if mode.endswith('b'):
            tmp_f_mode = "w+b"
        else:
            tmp_f_mode = "w+"
        with tempfile.TemporaryFile(tmp_f_mode) as f:

            try:
                resp = await self.request('GET', path, (200,))
                async for chunk in resp.aiter_bytes():
                    hasher.update(chunk)
                    f.write(chunk if tmp_f_mode == "w+b" else chunk.decode(decoding))

            except NetworkException as e:
                if e.code == 404:
                    pass
                else:
                    raise e
            initial_hash = hasher.hexdigest()

            if mode.startswith('w'):
                f.seek(0)

            yield f
            f.seek(0)
            f.seek(0)
            hasher = md5()
            for chunk in f:
                hasher.update(chunk)
            final_hash = hasher.hexdigest()

            f.seek(0)

            async def reader(_f):
                nonlocal chunk
                for chunk in _f:
                    print(chunk)
                    yield chunk

            print(initial_hash, final_hash)

            if initial_hash != final_hash:
                await self.upload(reader(f), path)

    async def cd(self, path: str):
        if not path.startswith('/'):
            self.cwd = self.cwd + path
        else:
            if path.endswith('/'):
                self.cwd = path
            else:
                self.cwd = path + '/'

    async def close(self):
        await self.http_client.aclose()
