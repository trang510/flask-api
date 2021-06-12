from unittest import TestCase
from app import create_app
import json
from api.route.pool import find_quantile
import numpy as np

class TestPool(TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_insert_pool_success(self):
    	payload = json.dumps({'pool_id': 2,'pool_values': [1]})
    	response = self.app.post('/api/pools/append_pool', headers={"Content-Type": "application/json"}, data=payload)
    	self.assertEqual(200, response.status_code)

    def test_insert_pool_error(self):
    	payload = json.dumps({'pool_id': '2','pool_values': [1]})
    	response = self.app.post('/api/pools/append_pool', headers={"Content-Type": "application/json"}, data=payload)
    	self.assertEqual(400, response.status_code)

    def test_query_pool_success(self):
    	payload = json.dumps({'pool_id': 1,'percentile': 95})
    	response = self.app.post('/api/pools/query_pool', headers={"Content-Type": "application/json"}, data=payload)
    	self.assertEqual(200, response.status_code)   

    def test_query_pool_error(self):
    	payload = json.dumps({'pool_id': 2,'percentile': 101})
    	response = self.app.post('/api/pools/query_pool', headers={"Content-Type": "application/json"}, data=payload)
    	self.assertEqual(400, response.status_code)

    def test_find_quantile(self):
    	pool_values = [1, 1, 1, 1, 3, 5, 6, 9, 10]
    	for i in range(0,101,5):
	    	result_numpy = np.percentile(pool_values, i)
	    	result_function = find_quantile(pool_values, i) # return 50th percentile, e.g median.
	    	self.assertEqual(result_function, result_numpy)