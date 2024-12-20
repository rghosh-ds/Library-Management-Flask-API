import unittest
from library_management_app import create_app, db
from library_management_app.models import Book, Member


class ModelTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    def setUp(self):
        with self.app.app_context():
            db.session.query(Book).delete()
            db.session.query(Member).delete()
            db.session.commit()

    def test_create_book(self):
        with self.app.app_context():
            new_book = Book(title="Test Book", author="Test Author")
            db.session.add(new_book)
            db.session.commit()

            book_in_db = Book.query.filter_by(title="Test Book").first()
            self.assertIsNotNone(book_in_db)
            self.assertEqual(book_in_db.title, "Test Book")
            self.assertEqual(book_in_db.author, "Test Author")

    def test_create_member(self):
        with self.app.app_context():
            new_member = Member(username="new_user", password="password123")
            db.session.add(new_member)
            db.session.commit()

            member_in_db = Member.query.filter_by(username="new_user").first()
            self.assertIsNotNone(member_in_db)
            self.assertEqual(member_in_db.username, "new_user")

    def test_unique_username(self):
        with self.app.app_context():
            member1 = Member(username="testuser", password="password123")
            db.session.add(member1)
            db.session.commit()

            member2 = Member(username="testuser", password="password456")
            db.session.add(member2)

            with self.assertRaises(Exception):
                db.session.commit()

    def test_book_constraints(self):
        with self.app.app_context():
            book_without_title = Book(title=None, author="No Title Author")
            with self.assertRaises(Exception):
                db.session.add(book_without_title)
                db.session.commit()

            book_without_author = Book(title="Test Book without Author", author=None)
            with self.assertRaises(Exception):
                db.session.add(book_without_author)
                db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
