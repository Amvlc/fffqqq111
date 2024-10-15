import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestLogic:
    def test_anonymous_user_cannot_send_comment(self, client, news):
        response = client.post(
            reverse("comment_create", args=[news.id]), {"text": "test comment"}
        )
        assert response.status_code == 403

    def test_authorized_user_can_send_comment(self, client, user, news):
        client.force_login(user)
        response = client.post(
            reverse("comment_create", args=[news.id]), {"text": "test comment"}
        )
        assert response.status_code == 302

    def test_comment_with_prohibited_words_is_not_published(
        self, client, user, news
    ):
        client.force_login(user)
        response = client.post(
            reverse("comment_create", args=[news.id]),
            {"text": "test comment with prohibited words"},
        )
        assert response.status_code == 400

    def test_authorized_user_can_edit_own_comment(self, client, user, comment):
        client.force_login(user)
        response = client.post(
            reverse("comment_edit", args=[comment.id]),
            {"text": "edited comment"},
        )
        assert response.status_code == 302

    def test_authorized_user_cannot_edit_foreign_comment(
        self, client, user, foreign_comment
    ):
        client.force_login(user)
        response = client.post(
            reverse("comment_edit", args=[foreign_comment.id]),
            {"text": "edited comment"},
        )
        assert response.status_code == 404

    def test_authorized_user_can_delete_own_comment(
        self, client, user, comment
    ):
        client.force_login(user)
        response = client.post(reverse("comment_delete", args=[comment.id]))
        assert response.status_code == 302

    def test_authorized_user_cannot_delete_foreign_comment(
        self, client, user, foreign_comment
    ):
        client.force_login(user)
        response = client.post(
            reverse("comment_delete", args=[foreign_comment.id])
        )
        assert response.status_code == 404
