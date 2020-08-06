from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

class PublicTagsApiTests(TestCase):
    """Test the publicly available tag API."""

    def setUP(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'password123'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags."""
        """ Get a couple of sample tags """
        """ Make a request to the api """
        """ Check if the tag is equal to what is expected """
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')
        """ Lets make our request"""
        res = self.client.get(TAGS_URL)
        """ This will make a http get request to the url """
        """ this will return your tags """
        """ make a query on the model that you expect to compare to the result """
        tags = Tag.objects.all().order_by('-name')
        """ This ensures that the tags are returned in aphabetcal order """
        """ Serialize your tag objects. """
        serializer = TagSerializer(tags,many=True)
        """ Add the assertions to your test. First assert the http status code. """
        """ Assert that the result is what you expected."""
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        """ The data that was return in the response should equal the """
        """ serializer data we passed in. """

        """ Our test tags limited to user. """
        """ Test that the tags are retrieved """
        """ Check that the tags are limited only to the user that logged in """
        """ See tags assigned to the authenticated user. """
        """ Create a new test """
    def test_tags_limited_to_user(self):
        """ Test that tags returned are for the authenticated user"""
        """ Create a new user. In addition to the one created in def setUP. """
        """ just so you can assign a tag to that user. You can then say that """
        """ the tag was not included in the response - not authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        """ Create a new tag object"""
        Tag.objects.create(user=user2, name='Fruity')
        """Create a new tag which is assigned to the authenticated user"""
        tag = Tag.objects.create(user=self.user,name='Comfort food')
        """ Now we will make our request"""
        res = self.client.get(TAGS_URL)
        """ Run some assert codes."""
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        """Length of the array that was returned in the request"""
        self.assertEqual(len(res.data),1)
        """ Test that the name returned in the tag """
        self.assertEqual(res.data[0]['name'],tag.name)
