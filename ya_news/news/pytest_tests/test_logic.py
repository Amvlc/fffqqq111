from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from ya_news.news.models import News


class LogicTestCase(TestCase):
    def setUp(self):
        self.user = self.create_user()

    def create_news(self, user, title="Test news", text="Test text"):
        return News.objects.create(user=user, title=title, text=text)

    def test_authenticated_user_can_create_news(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("add_news"),
            {"title": "Test news", "text": "Test text"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(News.objects.filter(title="Test news").exists())

    def test_anonymous_user_cannot_create_news(self):
        response = self.client.post(
            reverse("add_news"),
            {"title": "Test news", "text": "Test text"},
        )
        self.assertEqual(response.status_code, 302)

    def test_user_can_edit_own_news(self):
        news = self.create_news(self.user)
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("edit_news", args=[news.id]),
            {"title": "Updated title", "text": "Updated text"},
        )
        self.assertEqual(response.status_code, 302)
        news.refresh_from_db()
        self.assertEqual(news.title, "Updated title")
        self.assertEqual(news.text, "Updated text")

    def test_user_cannot_edit_other_user_news(self):
        user2 = self.create_user()
        news = self.create_news(user2)
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("edit_news", args=[news.id]),
            {"title": "Updated title", "text": "Updated text"},
        )
        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_own_news(self):
        news = self.create_news(self.user)
        self.client.force_login(self.user)
        response = self.client.post(reverse("delete_news", args=[news.id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            News.objects.get(id=news.id)

    def test_user_cannot_delete_other_user_news(self):
        user2 = self.create_user()
        news = self.create_news(user2)
        self.client.force_login(self.user)
        response = self.client.post(reverse("delete_news", args=[news.id]))
        self.assertEqual(response.status_code, 404)

    def test_news_creation_with_empty_title(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("add_news"), {"title": "", "text": "Test text"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(News.objects.filter(text="Test text").exists())

    def test_news_creation_with_empty_text(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("add_news"), {"title": "Test news", "text": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(News.objects.filter(title="Test news").exists())

    def test_news_editing_with_empty_title(self):
        news = self.create_news(self.user)
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("edit_news", args=[news.id]),
            {"title": "", "text": "Updated text"},
        )
        self.assertEqual(response.status_code, 200)
        news.refresh_from_db()
        self.assertNotEqual(news.title, "")

    def test_news_editing_with_empty_text(self):
        news = self.create_news(self.user)
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("edit_news", args=[news.id]),
            {"title": "Updated title", "text": ""},
        )
        self.assertEqual(response.status_code, 200)
        news.refresh_from_db()
        self.assertNotEqual(news.text, "")

    def test_news_title_is_required(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("add_news"), {"title": "", "text": "Test text"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(News.objects.filter(text="Test text").exists())

    def test_news_text_is_required(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("add_news"), {"title": "Test news", "text": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(News.objects.filter(title="Test news").exists())

    def test_news_editing_requires_login(self):
        news = self.create_news(self.user)
        response = self.client.post(
            reverse("edit_news", args=[news.id]),
            {"title": "Updated title", "text": "Updated text"},
        )
        self.assertEqual(response.status_code, 302)

    def test_news_deletion_requires_login(self):
        news = self.create_news(self.user)
        response = self.client.post(reverse("delete_news", args=[news.id]))
        self.assertEqual(response.status_code, 302)

    def test_news_deletion_by_owner(self):
        news = self.create_news(self.user)
        self.client.force_login(self.user)
        response = self.client.post(reverse("delete_news", args=[news.id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            News.objects.get(id=news.id)

    def test_news_deletion_by_non_owner(self):
        user2 = self.create_user()
        news = self.create_news(user2)
        self.client.force_login(self.user)
        response = self.client.post(reverse("delete_news", args=[news.id]))
        self.assertEqual(response.status_code, 404)

    def create_user(self):
        # создание пользователя
        pass

    def test_news_creation(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("add_news"),
            {"title": "Test news", "text": "Test text"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(News.objects.filter(title="Test news").exists())

    def test_news_editing(self):
        news = self.create_news(self.user)
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("edit_news", args=[news.id]),
            {"title": "Updated title", "text": "Updated text"},
        )
        self.assertEqual(response.status_code, 302)
        news.refresh_from_db()
        self.assertEqual(news.title, "Updated title")
        self.assertEqual(news.text, "Updated text")

    def test_news_deletion(self):
        news = self.create_news(self.user)
        self.client.force_login(self.user)
        response = self.client.post(reverse("delete_news", args=[news.id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            News.objects.get(id=news.id)
