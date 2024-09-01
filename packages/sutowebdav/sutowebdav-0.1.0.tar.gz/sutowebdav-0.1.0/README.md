# SutoWebDav
A simple asynchronous WebDAV client in Python.
## Installation
Install using pip:
```bash
pip install sutowebdav
```
## Quick Start
```python
import asyncio
from sutowebdav.client import DavClient
async def main():
    with DavClient('https://webdav.your-domain.com', username='myuser', password='mypass') as webdav:
        # Do some stuff:
        await webdav.mkdir('some_dir')
        await webdav.rmdir('another_dir')
        await webdav.download('remote/path/to/file', 'local/target/file')
        await webdav.upload('local/path/to/file', 'remote/target/file')
asyncio.run(main())
```

