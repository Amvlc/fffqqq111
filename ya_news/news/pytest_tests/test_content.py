from django.test import TestCase
from django.urls import reverse


class ContentTestCase(TestCase):
    def setUp(self):
        self.user = self.create_user()
        self.note = self.create_note(self.user)

    def test_note_in_object_list(self):
        response = self.client.get(reverse("notes"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.note, response.context["object_list"])

    def test_note_not_in_other_user_list(self):
        user2 = self.create_user()
        note2 = self.create_note(user2)
        response = self.client.get(reverse("notes"))
        self.assertNotIn(note2, response.context["object_list"])

    def test_form_on_create_edit_pages(self):
        response = self.client.get(reverse("add_note"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)

        response = self.client.get(reverse("note_edit", args=[self.note.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
