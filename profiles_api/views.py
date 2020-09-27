from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers, models, permissions

class HelloApiView(APIView):
    """"Hello Api View"""
    
    serializer_class = serializers.HelloSerializer
    
    def get(self, request, format=None):
        an_apiview = [
            'Something goes here'
        ]
    
        return Response({'an_apiview': an_apiview})
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            return Response({'message': f"Hello {name}"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewset(viewsets.ModelViewSet):
    """User Profile Viewset API"""
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email', )
    

class UserLoginView(ObtainAuthToken):
    """Handle creation of user authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    

class UserProfileFeedItemViewset(viewsets.ModelViewSet):
    """User Profile Viewset API"""
    queryset = models.ProfileFeedItem.objects.all()
    serializer_class = serializers.ProfileFeedItemSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated, )
    
    def perform_create(self, serializer):
        """Set user profile to an authenticated user"""
        serializer.save(user_profile=self.request.user)