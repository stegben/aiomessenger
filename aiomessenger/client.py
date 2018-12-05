import asyncio as aio
from typing import Optional, Mapping

from aiohttp import ClientSession


GRAPH_URL = 'https://graph.facebook.com'
GRAPH_API_VERSION = '3.2'


class Client:

    # TODO: list all members here
    # __slots__ = ()

    def __init__(
            self,
            access_token: str,
            app_id: str,
            app_secret: str,
            graph_api_version: str = GRAPH_API_VERSION,
            base_graph_url: str = GRAPH_URL,
            session: ClientSession = None,
            loop: Optional[aio.AbstractEventLoop] = None,
        ):
        self._access_token = access_token
        self._app_id = app_id
        self._app_secret = app_secret
        self._graph_api_version = graph_api_version
        self._base_graph_url = base_graph_url

        if session is None:
            self._session = ClientSession(
                headers={'Content-Type': 'application/json'},
            )
        else:
            self._session = session

        if loop is None:
            self._loop = self._session.loop
        else:
            if loop != self._session.loop:
                raise RuntimeError("The client and session should use the same event loop.")
            self._loop = loop

    @property
    def base_url(self):
        return "{0}/v{1}".format(self._base_graph_url, self._graph_api_version)

    async def get(self, endpoint: str, params: Optional[Mapping] = None):
        target_url = "{0}{1}".format(
            self.base_url,
            endpoint,
        )
        if params is None:
            params = {
                'access_token': self._access_token,
            }
        async with self._session.get(target_url, params=params) as resp:
            resp_data = await resp.json()
            return resp_data

    async def post(
            self,
            endpoint: str,
            params: Optional[Mapping] = None,
            data: Optional[Mapping] = None,
        ):
        target_url = "{0}{1}".format(
            self.base_url,
            endpoint,
        )
        if data is None:
            data = {}
        if params is None:
            params = {
                'access_token': self._access_token,
            }
        async with self._session.post(target_url, params=params, json=data) as resp:
            return await resp.json()

    async def send_raw_data(
            self,
            psid: str,
            message: Mapping[str, str],
            messaging_type: str,
            persona_id: str = None,
        ):
        # TODO: validate messaging to have correct value
        # ref: https://developers.facebook.com/docs/messenger-platform/send-messages/#messaging_types  # noqa
        post_data = {
            "messaging_type": messaging_type,
            "recipient": {
                "id": psid,
            },
            'message': message,
        }
        if persona_id is not None:
            post_data['persona_id'] = persona_id
        resp = await self.post('/me/messages', data=post_data)
        return resp

    async def debug_token(self):
        params = {
            'input_token': self._access_token,
            'access_token': '{0}|{1}'.format(self._app_id, self._app_secret),
        }
        return await self.get('/debug_token', params=params)

    def __del__(self):
        self._loop.run_until_complete(self._session.close())
