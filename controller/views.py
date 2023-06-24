import jwt
import traceback
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse ,Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny , IsAuthenticatedOrReadOnly


from .serializers import ArticleSerializer , UserRegistrationSerializer
from .models import Article , Author
from .decorators import relevant_user_required

# Create your views here.


class RegisterUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
    
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfile(APIView):

    permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        print(token)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        try:
    
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = Author.objects.get(id=user_id)
            user_data = {
                'first_name':user.first_name,
                'last_name':user.last_name,
                'username': user.username,
                'email': user.email,
                'bio':user.bio
            
            }
            
            return JsonResponse(user_data)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except (jwt.InvalidTokenError, KeyError, Author.DoesNotExist):
            return JsonResponse({'error': 'Invalid token'}, status=401)
        

    
    
class ArticleList(APIView):
    """
    List all articles, or create a new article.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        request.data['author']  = request.user.id
        serializer = ArticleSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Article Created Successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetail(APIView):
    """
    Retrieve, update or delete a article instance.
    """
    permission_classes = (IsAuthenticated, )
    
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    @relevant_user_required
    def patch(self, request, pk, format=None):
        article = self.get_object(pk)
        data = request.data
        data['author'] = article.author.id
        serializer = ArticleSerializer(instance = article, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response({"msg":"Article Updated Successfully!"}, status=status.HTTP_400_BAD_REQUEST)
    
    @relevant_user_required
    def delete(self, request, pk, format=None):
        article = self.get_object(pk)
        article.delete()
        return Response({"msg":"Article Deleted Successfully!"},status=status.HTTP_204_NO_CONTENT)

