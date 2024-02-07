from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Test case for the IndexView
class IndexViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

    # Test if the index view is accessible for an unauthenticated user
    def test_index_unauthenticated_user(self):
        # Send a GET request to the index view
        response = self.client.get(reverse('index'), follow=True)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
