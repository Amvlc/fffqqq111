from django.test import TestCase, Client
from django.urls import reverse


class RoutesTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_anonymous_user_routes(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("notes"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("add_note"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("done"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_routes(self):
        user = self.create_user()
        self.client.force_login(user)

        response = self.client.get(reverse("notes"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("add_note"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("done"))
        self.assertEqual(response.status_code, 200)

        # test note detail, edit, and delete routes
        note = self.create_note(user)
        response = self.client.get(reverse("note_detail", args=[note.slug]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("note_edit", args=[note.slug]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("note_delete", args=[note.slug]))
        self.assertEqual(response.status_code, 200)

    def test_note_permissions(self):
        user1 = self.create_user()
        user2 = self.create_user()
        note = self.create_note(user1)

        self.client.force_login(user2)
        response = self.client.get(reverse("note_detail", args=[note.slug]))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse("note_edit", args=[note.slug]))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse("note_delete", args=[note.slug]))
        self.assertEqual(response.status_code, 404)
