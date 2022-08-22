from aiohttp import web
import pydantic
import bcrypt
import asyncpg
import uuid
from errors import AppError
from models import db, UserModel, Token, AdsModel

PG_DSN = 'postgresql://admin:12345@127.0.0.1:5432/aiohttp_hw'


@web.middleware
async def errors_handler(request, handler):
    try:
        response = await handler(request)
    except pydantic.ValidationError as er:
        response = web.json_response({'error': str(er)}, status=400)
    except asyncpg.exceptions.UniqueViolationError as er:
        response = web.json_response({'error': str(er)}, status=400)
    except AppError as er:
        response = web.json_response({'error': str(er)}, status=400)
    return response


app = web.Application(middlewares=[errors_handler])


class CreateUserValidation(pydantic.BaseModel):
    user_name: str
    password: str

    @pydantic.validator('password')
    def strong_password(cls, value):
        if len(value) < 5:
            raise ValueError('too easy')
        return value


class UserView(web.View):
    async def get(self):
        user_id = self.request.match_info['user_id']
        user = await UserModel.get(int(user_id))
        try:
            user_data = user.to_dict()
        except AttributeError:
            raise AppError('User does not exist')
        return web.json_response(user_data)

    async def post(self):
        user_data = await self.request.json()
        validated_data = CreateUserValidation(**user_data).dict()
        salt = bcrypt.gensalt().decode()
        validated_data['salt'] = salt
        validated_data['password'] = bcrypt.hashpw(validated_data['password'].encode(), salt.encode()).decode()
        new_user = await UserModel.create(**validated_data)
        return web.json_response({
            'id': new_user.id
        })


class AllUserView(web.View):
    async def get(self):
        users = []
        all_users = await UserModel.query.gino.all()
        for item in all_users:
            users.append(item.to_dict())
        return web.json_response(users)


async def login(request):
    login_data = await request.json()
    user = await UserModel.query.where(UserModel.user_name == login_data['user_name']).gino.first()
    password = bcrypt.hashpw(login_data['password'].encode(), user.salt.encode()).decode()
    if user.password != password:
        raise AppError('Incorrect login or password')
    token_id = uuid.uuid4()
    new_token = {'id': token_id, 'user_id': user.id}
    token = await Token.create(**new_token)
    token = token.to_dict()
    return web.json_response(token)


async def check_token(request):
    headers = dict(request.headers)
    token = headers.get('token')
    try:
        is_token = await Token.get(token)
        return is_token.id
    except AttributeError:
        raise AppError('Invalid token')


class AdsView(web.View):
    async def get(self):
        ads_id = self.request.match_info['ads_id']
        ads = await AdsModel.get(int(ads_id))
        try:
            ads_data = ads.to_dict()
        except AttributeError:
            raise AppError('Ads does not exist')
        return web.json_response(ads_data)

    async def post(self):
        ads_data = await self.request.json()
        await check_token(self.request)
        new_ads = await AdsModel.create(**ads_data)
        return web.json_response(new_ads.to_dict())

    async def delete(self):
        ads_id = self.request.match_info['ads_id']
        await check_token(self.request)
        ads = await AdsModel.get(int(ads_id))
        try:
            await ads.delete()
        except AttributeError:
            raise AppError('Ads does not exist')
        return web.json_response({'status': 'Ads deleted'})

    async def patch(self):
        ads_id = self.request.match_info['ads_id']
        await check_token(self.request)
        new_data = await self.request.json()
        ads = await AdsModel.get(int(ads_id))
        try:
            await ads.update(**new_data).apply()
        except AttributeError:
            raise AppError('Ads does not exist')
        return web.json_response(ads.to_dict())


class AllAdsView(web.View):
    async def get(self):
        ads = []
        all_ads = await AdsModel.query.gino.all()
        for item in all_ads:
            ads.append(item.to_dict())
        return web.json_response(ads)


async def test_view(request):
    json_data = await request.json()
    headers = dict(request.headers)
    return web.json_response({'json': json_data})


async def init_orm(app):
    print('Application started')
    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


app.router.add_route('POST', '/login/', login)
app.router.add_routes(
    [
        web.get('/users/{user_id:\d+}/', UserView),
        web.post('/create_user/', UserView),
        web.get('/users/', AllUserView),
        web.post('/create_ads/', AdsView),
        web.get('/ads/{ads_id:\d+}/', AdsView),
        web.delete('/ads/{ads_id:\d+}/', AdsView),
        web.patch('/ads/{ads_id:\d+}/', AdsView),
        web.get('/ads/', AllAdsView),
    ]
)

app.cleanup_ctx.append(init_orm)
web.run_app(app)
