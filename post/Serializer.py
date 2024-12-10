from rest_framework import serializers
from post.models import Post

class PSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author' , 'title' , 'content' , 'created_at' , 'updated_at' , 'created_by' , 'updated_by']