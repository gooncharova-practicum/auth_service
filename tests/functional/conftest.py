import json
from dataclasses import dataclass

import aiofiles
import aiohttp
import pytest_asyncio
from config import BASE_URL, EXPECTED_RESPONSE_DIR


@dataclass
class HTTPResponse:
    body: dict
    headers: dict
    status: int


@pytest_asyncio.fixture
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
def make_get_request(session):
    async def inner(route: str, params: dict = None) -> HTTPResponse:
        url = f"{BASE_URL}{route}"
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest_asyncio.fixture
def make_post_request(session):
    async def inner(route: str, body: dict = None) -> HTTPResponse:
        url = f"{BASE_URL}{route}"
        async with session.post(url, json=body) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest_asyncio.fixture(scope="function")
async def expected_json_response(request):
    file = EXPECTED_RESPONSE_DIR.joinpath(f"{request.node.name}.json".split("test_")[1])
    async with aiofiles.open(file) as f:
        response = json.loads(await f.read())
    return response
