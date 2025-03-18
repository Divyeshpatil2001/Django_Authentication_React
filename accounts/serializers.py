from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_bytes,force_str
from django.urls import reverse
from .utils import send_normal_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,min_length=6,write_only=True)
    password2 = serializers.CharField(max_length=68,min_length=6,write_only=True)

    class Meta:
        model = User
        fields = ['email','first_name','last_name','password','password2']

    def validate(self, attrs):
        password = attrs.get('password','')
        password2 = attrs.get('password2','')
        if password != password2:
            raise serializers.ValidationError("password does not match")
        return attrs
    
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
        )
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=6)
    password = serializers.CharField(max_length=68,write_only=True)
    full_name = serializers.CharField(max_length=255,read_only=True)
    access_token = serializers.CharField(max_length=255,read_only=True)
    refresh_token = serializers.CharField(max_length=255,read_only=True)

    class Meta:
        model = User
        fields = ['email','password','full_name','access_token','refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request,email=email,password=password)
        if not user:
            raise AuthenticationFailed("Invalid credintals try again")
        user_tokens = user.tokens()
        return {
            'email' : user.email,
            'full_name' : user.get_full_name,
            'access_token' : str(user_tokens.get('access')),
            'refresh_token' : str(user_tokens.get('refresh'))
        }
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain = get_current_site(request).domain
            relative_link = reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
            abslink = f"http://{site_domain}{relative_link}"
            email_body = f"Hi use the link below to reset your password \n {abslink}"
            email_subject = "Reset Your Password"
            data = {
                'email_body':email_body,
                'email_subject':email_subject,
                'to_email':user.email
            }
            send_normal_email(data)

        return super().validate(attrs)

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100,min_length=6,write_only=True)
    confirm_password = serializers.CharField(max_length=100,min_length=6,write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ["password","confirm_password","uidb64","token"]
    
    def validate(self, attrs):
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({"error": "Password does not match"})
    
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
        
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({"error": "Reset link is invalid or has expired"})
        
            user.set_password(password)
            user.save()
        
            return user
        except Exception as e:
            raise serializers.ValidationError({"error": "Link is invalid or has expired"})
        
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError  

class LogoutSerializer(serializers.Serializer):
    """
    Serializer for handling user logout by blacklisting a refresh token.

    This serializer receives a refresh token, validates its presence, 
    and attempts to blacklist it to prevent further use.

    Attributes:
        refresh_token (CharField): A required field that holds the user's refresh token.

    Errors:
        bad_token: Raised if the provided token is invalid or has expired.
    """
    
    refresh_token = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is invalid or has expired')
    }

    def validate(self, attrs):
        """
        Extracts and stores the refresh token from the input data.

        Args:
            attrs (dict): The dictionary containing the refresh token.

        Returns:
            dict: The validated attributes containing the refresh token.
        """
        self.token = attrs.get('refresh_token')
        return attrs
    
    def save(self, **kwargs):
        """
        Blacklists the provided refresh token to prevent further use.

        This method converts the refresh token string into a RefreshToken object.
        If the token is valid, it is blacklisted, making it unusable for future authentication. 

        If the token is invalid or has already expired, a `TokenError` exception 
        is raised, and an error message is returned.

        Raises:
            TokenError: If the provided refresh token is invalid or expired.
        """
        try:
            token = RefreshToken(self.token)  # Convert to RefreshToken instance
            token.blacklist()  # Blacklist the token to prevent reuse
        except TokenError:
            self.fail('bad_token')  # Return a validation error if the token is invalid
