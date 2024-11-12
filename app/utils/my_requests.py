import httpx


async def post_request(url, data, headers=None, timeout=180.0):
    if headers is None:
        headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data, timeout=timeout)
        return response.json(), response.status_code
