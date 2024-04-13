from App import create_app,db
import pytest


@pytest.fixture()
def app():
    app=create_app(conf="Test")
    
    with app.app_context():
        db.create_all()
    yield app
    
@pytest.fixture()
def client(app):
    return app.test_client()