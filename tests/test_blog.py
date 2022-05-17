import unittest
from app.models import Blog, User
from app import db


class BlogModelTest(unittest.TestCase):
    def setUp(self):
        self.user_rachel = User(username='ray', password='rachel', email='test@test.com')
        self.new_blog = Blog(id=1, title='Test', post='This is a blog', user_id=self.user_rachel.id)

    def tearDown(self):
        Blog.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog.title, 'Test')
        self.assertEquals(self.new_blog.post, 'This is a test blog')
        self.assertEquals(self.new_blog.user_id, self.user_rachel.id)

    def test_save_blog(self):
        self.new_blog.save()
        self.assertTrue(len(Blog.query.all()) > 0)

    def test_get_blog(self):
        self.new_blog.save()
        got_blog = Blog.get_blog(1)
        self.assertTrue(got_blog is not None)