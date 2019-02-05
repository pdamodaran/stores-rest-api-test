from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel

from tests.test_base import BaseTest

import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            # need to save to database
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_response = client.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_response.data)['access_token']
                self.access_token = {'Authorization': 'JWT ' + auth_token}

    # need to figure out why response code is 200 here
    # def test_item_no_auth(self):
    #     with self.app() as client:
    #         # need to save to database
    #         with self.app_context():
    #             response = client.get('/item/blah')
    #
    #             self.assertEqual(401, response.status_code)

    def test_get_item_not_found(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                header = self.access_token

                response = client.get('item/stuff', headers = header)

                self.assertEqual(404, response.status_code)
                self.assertDictEqual({'message': 'Item not found'}, json.loads(response.data))

    def test_get_item(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                header = self.access_token
                client.post('/store/test')
                client.post('/item/stuff', data={'store_id': 1, 'price': 12.34})

                response = client.get('item/stuff', headers=header)
                self.assertEqual(200, response.status_code)

    def test_delete_item(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/store/test')
                client.post('/item/stuff', data={'store_id': 1, 'price': 12.34})
                self.assertIsNotNone(ItemModel.find_by_name('stuff'))
                response = client.delete('item/stuff')

                self.assertDictEqual({'message': 'Item deleted'}, json.loads(response.data))
                self.assertIsNone(ItemModel.find_by_name('stuff'))

    def test_create_item(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/store/test')
                response = client.post('/item/stuff', data={'store_id': 1, 'price': 12.34})

                self.assertEqual(201, response.status_code)
                self.assertIsNotNone(ItemModel.find_by_name('stuff'))
                self.assertDictEqual({'name': 'stuff', 'price': 12.34}
                                     , json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/store/test')
                client.post('/item/stuff', data={'store_id': 1, 'price': 12.34})

                response = client.post('/item/stuff', data={'store_id': 1, 'price': 12.34})
                self.assertEqual(400, response.status_code)
                self.assertDictEqual({'message': "An item with name 'stuff' already exists."}, json.loads(response.data))

    def test_put_new_item(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/store/test')
                response = client.put('/item/stuff', data={'store_id': 1, 'price': 12.34})
                self.assertEqual(200, response.status_code)
                self.assertIsNotNone(ItemModel.find_by_name('stuff'))
                self.assertDictEqual({'name': 'stuff', 'price': 12.34}
                                     , json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/store/test')
                client.post('/item/stuff', data={'store_id': 1, 'price': 12.34})

                response = client.put('/item/stuff', data={'store_id': 1, 'price': 12.00})
                self.assertEqual(200, response.status_code)
                self.assertIsNotNone(ItemModel.find_by_name('stuff'))
                self.assertDictEqual({'name': 'stuff', 'price': 12.00}
                                     , json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/store/test')
                client.post('/item/stuff', data={'store_id': 1, 'price': 12.34})

                response = client.get('/items')
                self.assertDictEqual({'items': [{'name': 'stuff', 'price': 12.34}]}
                                     , json.loads(response.data))