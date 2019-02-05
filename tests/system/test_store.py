from models.store import StoreModel
from models.item import ItemModel
from tests.test_base import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))

    def test_create_duplicate_store(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/store/test')
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "A store with name 'test' already exists."}, json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/store/test')
                response = client.delete('/store/test')

                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/store/test')
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'name': 'test', 'items': []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/store/test')
                response = client.get('/store/test2')

                self.assertIsNone(StoreModel.find_by_name('test2'))
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                auth_response = client.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})
                client.post('/store/test')
                # ItemModel('stuff', 12.34, 1).save_to_db()
                # the following call requires the user to be logged in
                client.post('/item/stuff', data={'store_id': 1, 'price': 12.34})

                response = client.get('/store/test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'test', 'items': [{'name': 'stuff',
                                                                 'price': 12.34}]}, json.loads(response.data))
                self.assertIsNotNone(ItemModel.find_by_name('stuff'))


    def test_store_list(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/store/test')

                response = client.get('/stores')
                self.assertDictEqual({'stores': [{'name': 'test', 'items': []}]}
                                     , json.loads(response.data))


    def test_store_list_with_items(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/store/test')
                ItemModel('stuff', 12.34, 1).save_to_db()

                response = client.get('/stores')
                self.assertDictEqual({'stores': [{'name': 'test',
                                                  'items': [{'name':
                                                             'stuff',
                                                             'price': 12.34}]}]}
                                     , json.loads(response.data))

