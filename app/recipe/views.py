from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
""" Create a viewset - generic viewset - use the list model mixit """
""" Use a combination of the two."""
""" It is a django rest model feature. You can pull in different parts of a viewset."""
""" We only want the list model function. We do not want the create,update,delete function"""
from rest_framework import viewsets, mixins, status
""" Add the token authentication. You want to authenticate the request. """
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
""" We just need to import the tag and the serializer."""

from core.models import Tag, Ingredient, Recipe
from recipe import serializers

class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)

""" Create your viewset """
class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    """Add the authentication classes"""
    """User is authenticated to use the api."""
    """Add the query set """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """ Return appropriate serializer class """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """ Create a new recipe """
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data = request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
