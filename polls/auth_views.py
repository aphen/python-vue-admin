from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .auth_serializers import RegisterSerializer, CustomTokenObtainPairSerializer
import logging

# Configure logging
logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        # Add logging to troubleshoot
        logger.info(f"Token request received from: {request.META.get('REMOTE_ADDR')}")
        try:
            response = super().post(request, *args, **kwargs)
            logger.info(f"Token request successful for user: {request.data.get('username')}")
            return response
        except Exception as e:
            logger.error(f"Token request failed: {str(e)}")
            raise e

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            # Log authentication info for debugging
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            logger.info(f"Auth header present: {bool(auth_header)}")
            
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                logger.error("No refresh token provided")
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
                
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"Successfully logged out user: {request.user}")
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return Response({"error": f"Invalid token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)