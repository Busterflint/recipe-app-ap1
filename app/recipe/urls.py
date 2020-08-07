from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

""" When you have a viewset - you may have multiple urls associated to that """
""" one viewset. /api/recipe/tags/1 to extract a specific item. """
""" The default router identifies the appropriate url. """

router = DefaultRouter()
""" You now have a new router object."""
""" Register our view """
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
