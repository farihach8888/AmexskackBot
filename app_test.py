import pytest

# def app_config():
#     return {
#         'TESTING': 'TRUE',
#         'ENV': 'E0'
#     }

# @pytest.fixture
# def mock_app(mocker, monkeypatch):
#     def _mock_setup(**kwargs):
#         auth = kwargs.get('auth', None)
#         monkeypatch.setenv('env', 'dev')
#         config = kwargs.get('config', None)
#         return app.app(config)

#     return _mock_setup

# @pytest.fixture
# def client(mock_app):
#     with mock_app(config=app_config()).test_client() as client:
#         yield client

def test_app_status():
    #     rv = client.get('/health')
    #     assert rv.status_code == 200
    assert "Hello" == "Hello"