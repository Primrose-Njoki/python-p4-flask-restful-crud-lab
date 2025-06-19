import json
from app import app
from models import db, Plant

class TestPlant:
    '''Flask application in app.py'''

    def setup_method(self):
        
        with app.app_context():
            db.session.query(Plant).delete()  
            plant = Plant(
                name="Test Aloe",
                image="https://example.com/test-aloe.jpg",
                price=10.99,
                is_in_stock=True
            )
            db.session.add(plant)
            db.session.commit()

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        assert response.status_code == 200

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        data = json.loads(response.data.decode())

        assert isinstance(data, dict)
        assert "id" in data
        assert "name" in data

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        response = app.test_client().patch(
            '/plants/1',
            json={"is_in_stock": False}
        )
        data = json.loads(response.data.decode())

        assert isinstance(data, dict)
        assert data["id"] == 1
        assert data["is_in_stock"] == False

    def test_plant_by_id_delete_route_deletes_plant(self):
        '''returns no content after deleting a plant'''
        with app.app_context():
            plant = Plant(
                name="Live Oak",
                image="https://example.com/live-oak.jpg",
                price=250.00,
                is_in_stock=False,
            )
            db.session.add(plant)
            db.session.commit()
            plant_id = plant.id

        response = app.test_client().delete(f'/plants/{plant_id}')
        assert response.status_code == 204
        assert response.data.decode() == ''
