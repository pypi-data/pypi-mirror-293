import pathlib

import aiohttp.web_response
from aiohttp import web


@web.middleware
async def mokei_resp_type_middleware(request, handler):
    resp = await handler(request)
    if isinstance(resp, tuple) and len(resp) == 2 and isinstance(resp[1], int):
        status = resp[1]
        resp = resp[0]
    else:
        status = 200
    if isinstance(resp, pathlib.Path):
        if resp.exists():
            with open(resp, mode='rb') as file:
                file_resp = web.Response(
                    body=file.read(),
                    headers={
                        'Content-Disposition': f'attachment; filename="{resp.name}"',
                        'Content-Type': 'application/octet-stream',
                    }
                )
            return file_resp
        raise aiohttp.web.HTTPNotFound()
    if isinstance(resp, dict):
        return web.json_response(resp, status=status)
    if isinstance(resp, str):
        return web.Response(body=resp, status=status)
    return resp
