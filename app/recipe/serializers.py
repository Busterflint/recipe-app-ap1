from rest_framework import serializers

from core.models import Tag

""" It will be a simple serialzer. Create a modal serializer. """
""" link to this our tag model. Pull in the id and name values."""
class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""
    class Meta:
        model = Tag
        fields = ('id','name')
        read_only_fields = ('id',)
