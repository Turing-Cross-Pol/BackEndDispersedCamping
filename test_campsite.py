# test_campsite.py
import unittest
import os
import json
from flask import jsonify
from app import create_app, db
import pdb


class CampsiteTestCase(unittest.TestCase):
    """This class represents the campsite test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.campsite = {'name': 'Go to Borabora for vacation', 'description': 'test', 'city': 'test', 'image_url': 'test', 'state': 'test', 'driving_tips': 'test', 'lon': 123, 'lat': 456}
        self.comment = {'title': 'amazing', 'description': 'this is a really great place', 'rating': '5'}
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_campsite_creation(self):
        """Test API can create a campsite (POST request)"""
        res = self.client().post('/campsites/', data=self.campsite)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_all_campsites(self):
        """Test API can get a campsite (GET request)."""
        res = self.client().post('/campsites/', data=self.campsite)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/campsites/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_campsite_by_id(self):
        """Test API can get a single campsite by using it's id."""
        rv = self.client().post('/campsites/', data=self.campsite)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/campsites/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Borabora', str(result.data))

    def test_campsite_can_be_edited(self):
        """Test API can edit an existing campsite. (PUT request)"""
        rv = self.client().post(
            '/campsites/',
            data=self.campsite)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/campsites/1',
            data={
                "name": "Dont just eat, but also pray and love :-)"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/campsites/1')
        self.assertIn('Dont just eat', str(results.data))

    def test_campsite_deletion(self):
        """Test API can delete an existing campsite. (DELETE request)."""
        rv = self.client().post(
            '/campsites/',
            data=self.campsite)
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/campsites/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/campsites/1')
        self.assertEqual(result.status_code, 404)

    @unittest.skip
    def test_comment_creation(self):
        res = self.client().post('/campsites/', data=self.campsite)
        self.assertEqual(rv.status_code, 201)
        res = self.client().post('/campsites/1/comments', data=self.comment)
        self.assertEqual(res.status_code, 201)
        self.assertIn('amazing', str(res.data))


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()