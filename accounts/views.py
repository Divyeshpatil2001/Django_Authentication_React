from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user

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


