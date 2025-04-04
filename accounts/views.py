from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer,LoginSerializer,PasswordResetRequestSerializer,SetNewPasswordSerializer,LogoutSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import OneTimePassword,User
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.
class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self,request):
        user_data = request.data
        print("request data, ",request.data)
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            print("serializer data is ",user)
            # send email function user['email']
            send_code_to_user(user['email'])
            return Response({
                'data': user,
                'message': f"hi {user['email']} thanks for signing up a passcode has be sent to mail"
                },
                status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class VerifyUserEmail(GenericAPIView):

    def post(self,request):
        otpcode = request.data.get('otp')
        try:
            user_code_obj = OneTimePassword.objects.get(code=otpcode)
            print("user object:",user_code_obj)
            user = user_code_obj.user
            print("this is user::",user)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    'message':"account email verified succesfully"
                },status=status.HTTP_200_OK)
            return Response({
                'message':"user already verified"
            },status=status.HTTP_208_ALREADY_REPORTED)
        except OneTimePassword.DoesNotExist:
            return Response({
                'message':"Invalid OTP. Please try again."
            },status=status.HTTP_404_NOT_FOUND)

class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
        except Exception as e:
            print("last except:",e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
    
class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        print(request.data)
        data = {'msg':"is it works"}
        return Response(data,status=status.HTTP_200_OK)
    
class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':"a link has been sent to your email to reset your password"},status=status.HTTP_200_OK)
    
class PasswordResetConfirm(GenericAPIView):
    def get(self,request,uidb64,token):
        try:
            user_id = urlsafe_base64_decode(uidb64)
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'message':"token is invalid or has expired"},status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True,'message':"creditanls is valid",'uidb64':uidb64,'token':token},status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'message':"token is invalid or has expired"},status=status.HTTP_401_UNAUTHORIZED)
        
class SetNewPassword(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message':'password reset successfull'},status=status.HTTP_200_OK)
    
class LogoutUserView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)