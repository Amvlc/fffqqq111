import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestContent:
    def test_news_count_on_main_page(self, client):
        response = client.get(reverse("main_page"))
        news_list = response.context["news_list"]
        assert len(news_list) <= 10

    def test_news_order_on_main_page(self, client):
        response = client.get(reverse("main_page"))
        news_list = response.context["news_list"]
        assert news_list[0].created_at >= news_list[-1].created_at

    def test_comments_order_on_news_page(self, client, news):
        response = client.get(reverse("news_page", args=[news.id]))
        comments_list = response.context["comments_list"]
        assert comments_list[0].created_at <= comments_list[-1].created_at

    def test_anonymous_user_cannot_see_comment_form(self, client, news):
        response = client.get(reverse("news_page", args=[news.id]))
        assert "comment_form" not in response.context

    def test_authorized_user_can_see_comment_form(self, client, user, news):
        client.force_login(user)
        response = client.get(reverse("news_page", args=[news.id]))
        assert "comment_form" in response.context
