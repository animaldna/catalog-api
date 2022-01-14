from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_route():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {
        "hello": "Welcome to the Conehead Records API",
        "api_version": "lol not sure",
        "documentation_url": "https://catalog-api.chloeboylan.work/redoc"
    }

def test_get_single_artist_success(sample_artist):
    response = client.get('/artists/90c335b/')
    assert response.status_code == 200
    assert response.json() == sample_artist

def test_get_single_artist_failure():
    response = client.get('/artists/1111111')
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Artist not found"
    }

def test_get_single_artist_validation_error(artist_validation_error):
    response = client.get('/artists/--123-1/')
    assert response.status_code == 422
    assert response.json() == artist_validation_error

def test_get_single_album_success(sample_album):
    response = client.get('/albums/12d3232/')
    assert response.status_code == 200
    assert response.json() == sample_album

def test_get_single_album_failure():
    response = client.get('/albums/1111111/')
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Album not found"
    }

def test_get_single_album_validation_error(album_validation_error):
    response = client.get('/albums/--123-1/')
    assert response.status_code == 422
    assert response.json() == album_validation_error

def test_get_all_genres():
    response = client.get('/genres/')
    assert response.status_code == 200
    assert response.json()['genres']
    