from server import app
import unittest
import os
from model import db, connect_to_db
import os
from seed_database_test import load_test

# Drop and re-create the test database.
os.system("dropdb games")
os.system("createdb games")



class DataBaseTesting(unittest.TestCase):
    """Examples of integration tests: testing Flask server."""
    def setUp(self):
        """Stuff to do before every test."""

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, db_uri="postgresql:///games")
        db.drop_all()
        db.create_all()
        load_test()

        # Put user1 into session.
        with self.client as c:
            with c.session_transaction() as sess:
                sess["current_user"] = 1
                
    def test_login_route_correct(self):
        """tests that the login route is working correctly with correct login information"""
        result = self.client.post("/login",
        data={"username":"test_user1", "password":"test_pass1"}, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Nice to see you back, test_user1!", result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()