from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Profile

class UsersViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = self.user.profile

    def test_home_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('users:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_circles.html')

    def test_home_view_anonymous(self):
        url = reverse('users:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')

    def test_profile_details_authenticated(self):
        login = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login, "Login failed, check username/password")

        url = reverse('users:profile_details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_details.html')


    def test_profile_details_redirect_anonymous(self):
        url = reverse('users:profile_details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_get(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('users:edit_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        self.assertIn('form', response.context)

    def test_edit_profile_post(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('users:edit_profile')
        data = {
            'bio': 'Updated bio',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')

    def test_delete_profile_get(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('users:delete_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_details.html')

    def test_delete_profile_post(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('users:delete_profile')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='testuser')
