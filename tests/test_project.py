from User.Models.models import *
def test_inscription(client, app):
    
    data = {
        'nom': 'Tests',
        'prenom': 'Users',
        'email': 'test@examples.com',
        'password': 'Cuadrado2002',
        'Confirm_password': 'Cuadrado2002',
        'nationalite': 'FR'
    }
    response = client.post('/inscription', data=data)
    
    with app.app_context():
        assert response.status_code == 200  
        user = User.query.filter_by(mail='test@examples.com').first()
        assert user is not None


def test_connexion(client,app):
        response = client.post('/connexion', data=dict(
            email='test@examples.com',
            password='Cuadrado2002'
        ))
        with app.app_context():
            assert response.status_code == 302

