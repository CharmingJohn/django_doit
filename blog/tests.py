from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category, Tag

# Create your tests here.

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_chae1234 = User.objects.create_user(username='chae1234', password='')

        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.tag_python_kor = Tag.objects.create(name='python study', slug='python-study')
        self.tag_python = Tag.objects.create(name='python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')

        self.post_001 = Post.objects.create(
            title='first post',
            content='hello world',
            category=self.category_programming,
            author=self.user_chae1234,
        )
        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title='second post',
            content='second world',
            category=self.category_music,
            author=self.user_chae1234,
        )

        self.post_003 = Post.objects.create(
            title='third post',
            content='there may be no category',
            author=self.user_chae1234
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)

    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.conent, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_programming.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertIn(self.post_002.title, main_area.text)
        self.assertIn(self.post_003.title, main_area.text)

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn('{} ({})'.format(self.category_programming.name, self.category_programming.post_set.count()), categories_card.text)
        self.assertIn('{} ({})'.format(self.category_music.name, self.category_music.post_set.count()), categories_card.text)
        self.assertIn('미분류 (1)', categories_card.text)

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
        # Post가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual(soup.title.text, 'Blog')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('there is no any post', main_area.text)

        post_001_card = main_area.find('div', id='post-1')  # id가 post-1인 div를 찾아서, 그 안에
        self.assertIn(self.post_001.title, post_001_card.text)  # title이 있는지
        self.assertIn(self.post_001.category.name, post_001_card.text)  # category가 있는지
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)  # 작성자명이 있는지
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.post_002.author.username.upper(), post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)

        # Post가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')  # id가 main-area인 div태그를 찾습니다.
        self.assertIn('there is no any post', main_area.text)

    def test_post_detail(self):
        # 1.1 one post
        '''
        post_001 = Post.objects.create(
            title='first post',
            conent='hello world',
        )
        '''
        # 1.2 url of upper post is 'blog/1/'
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1')

        # 2. test detail of the first post
        # 2.1 first post url
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2 same navigation bar of post list page
        self.navbar_test(soup)
        # navbar = soup.nav
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About me', navbar.text)

        self.category_card_test(soup)

        # 2.3 web browser title in title of first post
        self. assertIn(self.post_001.title, soup.title.text)

        # 2.4 title of the first post in post_area
        main_area = soup.find('div', id='main-area')
        post_area = soup.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        # 2.5 author of the first post in post_area
        self.assertIn(self.category_programming.name, post_area.text)

        # 2.6 content of the first post in post_area
        self.assertIn(self.post_001.content, post_area.text)

        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertIn(self.tag_python.name, post_area.text)
        self.assertIn(self.tage_python_kor.name, post_area.text)


'''
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
            category=self.category_programming,
            author=self.user_chae1234
        )
        post_002 = Post.objects.create(
            title='second post',
            content='It\'s second post',
            category=self.category_music,
            author=self.user_chae1234,
        )
        post_003 = Post.objects.create(
            title='third post',
            content='there may be no category',
            author=self.user_chae1234,
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
        
'''