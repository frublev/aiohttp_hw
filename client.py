import aiohttp
import asyncio

HOST = 'http://127.0.0.1:8080'
TOKEN = '1707ffb8-aea7-4b51-b13f-70e32effcfed'


async def main():
    async with aiohttp.ClientSession() as session:
        # async with session.post(f'{HOST}/test/', json={'key': 'value'}) as response:
        #     print(response.status)
        #     print(await response.json())

        # async with session.post(f'{HOST}/create_user/', json={'user_name': 'User2', 'password': '12345'}) as response:
        #     print(response.status)
        #     print(await response.json())

        # async with session.get(f'{HOST}/users/1/') as response:
        #     print(response.status)
        #     print(await response.json())
        #
        # async with session.get(f'{HOST}/users/') as response:
        #     print(response.status)
        #     print(await response.json())
        #
        # async with session.post(f'{HOST}/login/', json={'user_name': 'User2', 'password': '12345'}) as response:
        #     print(response.status)
        #     print(await response.json())

        # async with session.post(
        #         f'{HOST}/create_ads/',
        #         json={'head': 'Head_10', 'body': 'Text_10', 'user_id': 5},
        #         headers={'Content-Type': 'application/json', 'token': TOKEN}) as response:
        #     print(response.status)
        #     print(await response.json())
        #
        async with session.get(f'{HOST}/ads/') as response:
            print(response.status)
            print(await response.json())

        # async with session.get(f'{HOST}/ads/1/') as response:
        #     print(response.status)
        #     print(await response.json())
        #
        async with session.delete(
                f'{HOST}/ads/14/',
                headers={'Content-Type': 'application/json', 'token': TOKEN}) as response:
            print(response.status)
            print(await response.json())
        #
        # async with session.patch(
        #         f'{HOST}/ads/14/',
        #         json={'head': 'Head_12', 'body': 'Text_12', 'user_id': 5},
        #         headers={'Content-Type': 'application/json', 'token': TOKEN}) as response:
        #     print(response.status)
        #     print(await response.json())

asyncio.run(main())
