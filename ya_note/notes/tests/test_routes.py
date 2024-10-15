import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestRoutes:
    def test_anonymous_user_can_access_main_page(self, client):
        response = client.get(reverse("main_page"))
        assert response.status_code == 200

    def test_anonymous_user_can_access_news_page(self, client):
        news_id = 1
        response = client.get(reverse("news_page", args=[news_id]))
        assert response.status_code == 200

    def test_author_can_access_comment_edit_page(self, client, user, comment):
        client.force_login(user)
        response = client.get(reverse("comment_edit", args=[comment.id]))
        assert response.status_code == 200

    def test_author_can_access_comment_delete_page(
        self, client, user, comment
    ):
        client.force_login(user)
        response = client.get(reverse("comment_delete", args=[comment.id]))
        assert response.status_code == 200

    def test_anonymous_user_redirected_to_login_on_comment_edit(
        self, client, comment
    ):
        response = client.get(reverse("comment_edit", args=[comment.id]))
        assert response.status_code == 302
        assert response.url.startswith(reverse("login"))

    def test_anonymous_user_redirected_to_login_on_comment_delete(
        self, client, comment
    ):
        response = client.get(reverse("comment_delete", args=[comment.id]))
        assert response.status_code == 302
        assert response.url.startswith(reverse("login"))

    def test_authorized_user_cannot_access_foreign_comment_edit(
        self, client, user, foreign_comment
    ):
        client.force_login(user)
        response = client.get(
            reverse("comment_edit", args=[foreign_comment.id])
        )
        assert response.status_code == 404

    def test_authorized_user_cannot_access_foreign_comment_delete(
        self, client, user, foreign_comment
    ):
        client.force_login(user)
        response = client.get(
            reverse("comment_delete", args=[foreign_comment.id])
        )
        assert response.status_code == 404

    def test_anonymous_user_can_access_registration_page(self, client):
        response = client.get(reverse("registration"))
        assert response.status_code == 200

    def test_anonymous_user_can_access_login_page(self, client):
        response = client.get(reverse("login"))
        assert response.status_code == 200

    def test_anonymous_user_can_access_logout_page(self, client):
        response = client.get(reverse("logout"))
        assert response.status_code == 200
