import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'
    
def test_shorten_url(client):
    response = client.post('/api/shorten', json={'url': 'https://example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data

def test_redirect(client):
    response = client.post('/api/shorten', json={'url': 'https://google.com'})
    code = response.get_json()['short_code']
    response = client.get(f'/{code}', follow_redirects=False)
    assert response.status_code == 302

def test_stats(client):
    response = client.post('/api/shorten', json={'url': 'https://test.com'})
    code = response.get_json()['short_code']
    client.get(f'/{code}')  # simulate a click
    response = client.get(f'/api/stats/{code}')
    data = response.get_json()
    assert data['clicks'] == 1
    assert data['url'] == 'https://test.com'

def test_invalid_url(client):
    response = client.post('/api/shorten', json={'url': 'not-a-url'})
    assert response.status_code == 400

def test_missing_url(client):
    response = client.post('/api/shorten', json={})
    assert response.status_code == 400
    