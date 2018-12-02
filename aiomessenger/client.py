import asyncio as aio
from typing import Optional, Mapping

from aiohttp import ClientSession


GRAPH_URL = "https://graph.facebook.com"


class Client:

    # TODO: list all members here
    # __slots__ = ()

    def __init__(
            self,
            access_token: str,
            app_id: str,
            app_secret: str,
            graph_api_version: str = '3.2',
            session: ClientSession = None,
            loop: Optional[aio.AbstractEventLoop] = None,
        ):
        self._access_token = access_token
        self._app_id = app_id
        self._app_secret = app_secret
        self._graph_api_version = graph_api_version

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
        return "{0}/v{1}".format(GRAPH_URL, self._graph_api_version)

    async def get(self, endpoint: str, params: Optional[Mapping] = None):
        async with self._session as sess:
            target_url = "{0}{1}".format(
                self.base_url,
                endpoint,
            )
            if params is None:
                params = {
                    'access_token': self._access_token,
                }
            async with sess.get(target_url, params=params) as resp:
                return await resp.json()

    async def post(
            self,
            endpoint: str,
            params: Optional[Mapping] = None,
            data: Optional[Mapping] = None,
        ):
        async with self._session as sess:
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
            async with sess.post(target_url, params=params, data=data) as resp:
                return await resp.json()

    async def send_raw_data(
            self,
            user_id: str,
            message: Mapping[str, str],
            messaging_type: str,
        ):
        # TODO: validate messaging to have correct value
        # ref: https://developers.facebook.com/docs/messenger-platform/send-messages/#messaging_types  # noqa
        post_data = {
            "messaging_type": messaging_type,
            "recipient": {
                "id": user_id,
            },
            **message,
        }
        resp = await self.post('/me/messages', data=post_data)
        return resp

    async def debug_token(self):
        params = {
            'input_token': self._access_token,
            'access_token': '{0}|{1}'.format(self._app_id, self._app_secret),
        }
        return await self.get('/debug_token', params=params)
