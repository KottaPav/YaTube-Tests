from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='HasNoName'
        )
        cls.author = User.objects.create_user(
            username='Автор'
        )
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.author,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.author)

    def test_url_redirect_nonauthor(self):
        """Перенаправление пользователя - не автора поста"""
        response = self.authorized_client.get(
            f'/posts/{self.post.id}/edit/',
        )
        self.assertRedirects(response, ('/create/'))
        self.assertEqual(response.status_code, 302)

    def test_url_redirect_guest_client(self):
        """Перенаправление неавторизированного пользователя"""
        url1 = '/auth/login/?next=/create/'
        url2 = f'/auth/login/?next=/posts/{self.post.id}/edit/'
        pages = {
            '/create/': url1,
            f'/posts/{self.post.id}/edit/': url2
        }
        for page, value in pages.items():
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertRedirects(response, value)

    def test_url_redirect_guest_client(self):
        """Перенаправление неавторизированного пользователя"""
        url1 = '/auth/login/?next=/create/'
        url2 = f'/auth/login/?next=/posts/{self.post.id}/edit/'
        pages = {
            '/create/': url1,
            f'/posts/{self.post.id}/edit/': url2
        }
        for page, value in pages.items():
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertRedirects(response, value)

    def test_unexisting_page_url_exists_at_desired_location(self):
        """Несуществующая страница возвращает ошибку 404."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_url_notauthorized_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': f'{self.group.slug}'}): 'posts/'
                                                            'group_list.html',
            reverse('posts:profile',
                    kwargs={'username':
                            f'{self.user.username}'}): 'posts/'
                                                       'profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': f'{self.post.id}'}): 'posts/'
                                                            'post_detail.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
                self.assertEqual(response.status_code, 200)

    def test_url_authorized_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        address = reverse('posts:post_create')
        template = 'posts/post_create.html'
        response = self.authorized_client.get(address)
        self.assertTemplateUsed(response, template)
        self.assertEqual(response.status_code, 200)

    def test_url_author_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        address = reverse(
            'posts:post_edit',
            kwargs={'post_id': f'{self.post.id}'}
        )
        template = 'posts/post_create.html'
        response = self.authorized_client_author.get(address)
        self.assertTemplateUsed(response, template)
        self.assertEqual(response.status_code, 200)
