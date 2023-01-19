from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostFormTests(TestCase):
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

    def test_post_create(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
            'author': self.author
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': self.user.username}
        ))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        new_post = Post.objects.latest('pub_date')
        self.assertEqual(new_post.text, form_data['text'])
        self.assertEqual(new_post.group_id, form_data['group'])

    def test_post_edit(self):
        """Валидная форма изменяет запись в Post."""
        new_group = Group.objects.create(
            title='Новая тестовая группа',
            slug='test_slug_new',
            description='Новое тестовое описание',
        )
        form_data = {
            'text': 'Измененный текст',
            'group': new_group.id,
            'author': self.author
        }
        response = self.authorized_client_author.post(
            reverse('posts:post_edit', args=({self.post.id})),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id}
        ))
        post = Post.objects.latest('id')
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group_id, form_data['group'])
        self.assertEqual(post.author, form_data['author'])

    def test_notauthorized_cannot_create_post(self):
        """Проверка запрета создания не авторизованного пользователя"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
        }
        response = self.guest_client.post(reverse('posts:post_create'),
                                          data=form_data,
                                          follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(
            Post.objects.count(),
            posts_count + 1,
        )
