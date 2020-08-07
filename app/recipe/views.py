from django.shortcuts import render

# Create your views here.
""" Create a viewset - generic viewset - use the list model mixit """
""" Use a combination of the two."""
""" It is a django rest model feature. You can pull in different parts of a viewset."""
""" We only want the list model function. We do not want the create,update,delete function"""
from rest_framework import viewsets, mixins
""" Add the token authentication. You want to authenticate the request. """
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
""" We just need to import the tag and the serializer."""
from core.models import Tag, Ingredient
from recipe import serializers
""" Create your viewset """
class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    """Add the authentication classes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    """User is authenticated to use the api."""
    """Add the query set """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag."""
        serializer.save(user=self.request.user)

class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage ingredients in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
