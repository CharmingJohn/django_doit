from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post

# Create your tests here.

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About_me', navbar.text)

        logo_btn = navbar.find('a', text='go to redwood')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About_me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def test_post_list(self):
        # 1.1 get the post list page
        response = self.client.get('/blog/')
        # 1.2 Load page well
        self.assertEqual(response.status_code, 200)
        # 1.3 Title of page is 'Blog'
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        # 1.4 navigation bar
        # navbar = soup.nav
        # 1.5 sentence in navigation Bar - 'Blog, About me'
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About me', navbar.text)
        self.navbar_test(soup)

        # 2.1 if not posts
        self.assertEqual(Post.objects.count(), 0)
        # 2.2 'there is no any post' on main area
        main_area = soup.find('div', id='main-area')
        self.assertIn('there is no any post', main_area.text)

        # 3.1 if there are 2 posts
        post_001 = Post.objects.create(
            title='first post',
            content='Hello World.',
        )
        post_002 = Post.objects.create(
            title='second post',
            content='It\'s second post',
        )
        self.assertEqual(Post.objects.count(), 2)

        # 3.2 refresh the post list page
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.cotent, 'html.parser')
        self.assertEqual(response.status, 200)
        # 3.3 2 post titles in main area
        main_area = soup.find('div', id='main-ara')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4 no more 'there is no any post'
        self.assertNotIn('there is no any post', main_area.text)

    def test_post_detail(self):
        # 1.1 one post
        post_001 = Post.objects.create(
            title='first post',
            conent='hello world',
        )
        # 1.2 url of upper post is 'blog/1/'
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 2. test detail of the first post
        # 2.1 first post url
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2 same navigation bar of post list page
        self.navbar_test(soup)
        # navbar = soup.nav
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About me', navbar.text)

        # 2.3 web browser title in title of first post
        self. assertIn(post_001.title, soup.title.text)

        # 2.4 title of the first post in post_area
        main_area = soup.find('div', id='main-area')
        post_area = soup.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)

        # 2.5 author of the first post in post_area

        # 2.6 content of the first post in post_area
        self.assertIn(post_001.content, post_area.text)
