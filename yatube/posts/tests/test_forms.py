from posts.forms import PostForm
from posts.models import Group, Post, User
from django.test import Client, TestCase
from django.urls import reverse


class PostCreateFormTests(TestCase):
    @classmethod
    class PostFormTests(TestCase):

        def setUpClass(cls):
            super().setUpClass()
            Post.objects.create(
                title='Тестовый заголовок',
                text='Тестовый текст',
                slug='first'
            )
            cls.form = PostForm()

    def setUp(self):
        self.user = User.objects.create(username="HasNoName")
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            # 'group': 'Тестовая группа', Необязательная. Надо ли проверять?
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            "posts:profile",
            kwargs={"username": self.user.username})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(
            text='Тестовый текст',
            group='Тестовая группа',
        ).exists()
        )

    def test_post_edit(self):
        """Валидная форма изменяет запись в Post."""
        self.post = Post.objects.create(
            author=self.user,
            text="Тестовый текст",
        )
        self.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug",
            description="Тестовое описание",
        )
        posts_count = Post.objects.count()
        form_data = {"text": "Измененный текст", "group": self.group.id}
        response = self.authorized_client.post(
            reverse("posts:post_edit", args=({self.post.id})),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            "posts:post_detail", kwargs={"post_id": self.post.id}
        ))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(Post.objects.filter(text="Измененный текст").exists())
