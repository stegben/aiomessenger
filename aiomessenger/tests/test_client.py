import aio

from aiomessenger import Client


def test_client_correct_member():
    mock_access_token = 'mock_access_token'
    mock_app_id = 'mock_app_id'
    mock_app_secret = 'some_app_secret'
    mock_graph_api_version = '3.0'
    client = Client(
        access_token=mock_access_token,
        app_id=mock_app_id,
        app_secret=mock_app_secret,
        graph_api_version=mock_graph_api_version,
    )

    assert client._access_token == mock_access_token
    assert client._app_id == mock_app_id
    assert client._app_secret == mock_app_secret
    assert client._graph_api_version == mock_graph_api_version
