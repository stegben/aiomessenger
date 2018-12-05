import asyncio as aio

import pytest
from aiohttp import ClientSession
from asynctest import Mock, CoroutineMock, MagicMock

from aiomessenger import Client


def test_client_correct_member():
    mock_access_token = 'mock_access_token'
    mock_app_id = 'mock_app_id'
    mock_app_secret = 'some_app_secret'
    mock_graph_api_version = '3.0'
    mock_base_graph_url = 'https://fb.graph'
    client = Client(
        access_token=mock_access_token,
        app_id=mock_app_id,
        app_secret=mock_app_secret,
        graph_api_version=mock_graph_api_version,
        base_graph_url=mock_base_graph_url,
    )

    assert client._access_token == mock_access_token
    assert client._app_id == mock_app_id
    assert client._app_secret == mock_app_secret
    assert client._graph_api_version == mock_graph_api_version
    assert client._base_graph_url == mock_base_graph_url

    assert client.base_url == 'https://fb.graph/v3.0'


def test_client_raise():
    mock_access_token = 'mock_access_token'
    mock_app_id = 'mock_app_id'
    mock_app_secret = 'some_app_secret'
    mock_graph_api_version = '3.0'
    with pytest.raises(RuntimeError):
        Client(
            access_token=mock_access_token,
            app_id=mock_app_id,
            app_secret=mock_app_secret,
            graph_api_version=mock_graph_api_version,
            session=ClientSession(),  # use default loop
            loop=aio.new_event_loop(),
        )


@pytest.fixture(scope='function')
def session():
    sess = MagicMock()
    mock_resp = MagicMock()
    mock_resp.json = CoroutineMock()
    mock_resp_gen = CoroutineMock(return_value=mock_resp)
    request_ctx_mgr = MagicMock()
    request_ctx_mgr.__aenter__ = mock_resp_gen
    request_ctx_mgr.__aexit__ = CoroutineMock()
    sess.get = Mock(return_value=request_ctx_mgr)
    sess.post = Mock(return_value=request_ctx_mgr)
    return sess


@pytest.fixture(scope='function')
def client(session):
    mock_access_token = 'mock_access_token'
    mock_app_id = 'mock_app_id'
    mock_app_secret = 'some_app_secret'
    mock_graph_api_version = '3.0'
    mock_base_graph_url = 'https://fb.graph'
    client = Client(
        access_token=mock_access_token,
        app_id=mock_app_id,
        app_secret=mock_app_secret,
        graph_api_version=mock_graph_api_version,
        base_graph_url=mock_base_graph_url,
        session=session,
    )
    return client


@pytest.mark.asyncio
async def test_get(client):
    await client.get(endpoint='/test', params=None)
    client._session.get.assert_called_once_with(
        'https://fb.graph/v3.0/test',
        params={'access_token': client._access_token},
    )


@pytest.mark.asyncio
async def test_get_with_params(client):
    get_params = {'var': 'value'}
    await client.get(endpoint='/test', params=get_params)
    client._session.get.assert_called_once_with(
        'https://fb.graph/v3.0/test',
        params=get_params,
    )


@pytest.mark.asyncio
async def test_post(client):
    await client.post(endpoint='/test')
    client._session.post.assert_called_once_with(
        'https://fb.graph/v3.0/test',
        params={'access_token': client._access_token},
        json={},
    )


@pytest.mark.asyncio
async def test_post_with_param(client):
    post_param = {'some': 'params'}
    await client.post(endpoint='/test', params=post_param)
    client._session.post.assert_called_once_with(
        'https://fb.graph/v3.0/test',
        params=post_param,
        json={},
    )


@pytest.mark.asyncio
async def test_post_with_data(client):
    post_data = {'some': 'data'}
    await client.post(endpoint='/test', data=post_data)
    client._session.post.assert_called_once_with(
        'https://fb.graph/v3.0/test',
        params={'access_token': client._access_token},
        json=post_data,
    )


@pytest.mark.asyncio
async def test_post_with_param_and_data(client):
    post_param = {'some': 'params'}
    post_data = {'some': 'data'}
    await client.post(endpoint='/test', data=post_data, params=post_param)
    client._session.post.assert_called_once_with(
        'https://fb.graph/v3.0/test',
        params=post_param,
        json=post_data,
    )


@pytest.mark.asyncio
async def test_send_raw_data(client):
    client.post = CoroutineMock()
    psid = '12uyg34iu12y34'
    message = {'text': 'hello'}
    messaging_type = 'UPDATE'
    await client.send_raw_data(psid, message, messaging_type)
    client.post.assert_called_once_with(
        '/me/messages',
        data={
            "messaging_type": messaging_type,
            "recipient": {
                "id": psid,
            },
            'message': message,
        },
    )


@pytest.mark.asyncio
async def test_send_raw_data_with_persona_id(client):
    client.post = CoroutineMock()
    psid = '12uyg34iu12y34'
    message = {'text': 'hello'}
    messaging_type = 'UPDATE'
    persona_id = 'asdf'
    await client.send_raw_data(psid, message, messaging_type, persona_id)
    client.post.assert_called_once_with(
        '/me/messages',
        data={
            "messaging_type": messaging_type,
            "recipient": {
                "id": psid,
            },
            'message': message,
            'persona_id': persona_id,
        },
    )


@pytest.mark.asyncio
async def test_debug_token(client):
    client.get = CoroutineMock()
    await client.debug_token()
    client.get.assert_called_once_with(
        '/debug_token',
        params={
            'input_token': client._access_token,
            'access_token': '{0}|{1}'.format(client._app_id, client._app_secret),
        },
    )
