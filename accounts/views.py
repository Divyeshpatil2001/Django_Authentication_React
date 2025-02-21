from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import OneTimePassword

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
                'message':"code is invalid user already verified"
            },status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({
                'message':"passcode does not provided"
            },status=status.HTTP_404_NOT_FOUND)

class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        if serializer.is_valid(raise_exception=True):
