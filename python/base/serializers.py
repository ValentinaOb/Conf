'''from rest_framework import serializers
from .models import Document
from django.utils import timezone

class DocUploatSerializer(serializers.ModelSerializer):
    uploaded_at=serializers.DateTimeField(read_only=True)
    file_size=serializers.IntegerField(read_only=True)
    category=serializers.CharField(read_only=True)
    #user=serializers.SerializerMethodField('user')
    id = serializers.ReadOnlyField()
    class Meta:
        model=Document
        fields=['id', 'category', 'user', 'file', 'file_size' ,'uploaded_at']

    def update(self, instance, validated_data):
        instance.uploaded_at = timezone.now()
        return super().update(instance, validated_data)
    
    '''