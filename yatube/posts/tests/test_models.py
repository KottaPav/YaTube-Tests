from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()

CUT_POST_LENGTH = 15


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='abc' * 6,
        )

    def test_group_have_correct_object_names(self):
        """Проверяем, работу __str__ в Group."""
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_post_have_correct_object_names(self):
        """Проверяем, работу __str__ в Post."""
        post = PostModelTest.post
        expected_object_name = post.text[:CUT_POST_LENGTH]
        self.assertEqual(expected_object_name, str(post))
