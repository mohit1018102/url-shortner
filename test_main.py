from urlshort import create_app

def test_shorten(client):
    response= client.get('/')
    assert b'Generate' in response.data

def test_code(client):
    response= client.get('/')
    assert b'Short Code' in response.data
