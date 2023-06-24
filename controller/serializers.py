

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Author , Article 



class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    serializer for user registration
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = Author
        fields = ('email', 'username', 'password', 'first_name', 'last_name','bio')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        
        if Author.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email address already in use.'})
        
        if Author.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Username already in use.'})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Author(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('username',)
     

class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for article model
    """
    author_username = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Article
        fields = ('id','title' , 'description', 'created_at','updated_at','author_username','author')
    
    def get_author_username(self, obj):
        name = Author.objects.get(id = obj.author_id)
        return name.username
        
    