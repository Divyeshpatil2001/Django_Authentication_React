from rest_framework import serializers
from .utils import Google,register_social_user
from .github import Github
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed,ValidationError
import requests

class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length=6)

    def validate_access_token(self,access_token):
        google_user_data = Google.validate(access_token)
        print(google_user_data)
        try:
            userid = google_user_data["sub"]
            print(userid)
        except:
            raise serializers.ValidationError("this token is invalid or has expired")
        if google_user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed(detail="could not verify user")
        email = google_user_data['email']
        first_name = google_user_data['given_name']
        last_name = google_user_data['family_name']
        provider = "google"
        return register_social_user(provider,email,first_name,last_name)
    
class GithubOauthSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=2)

    def validate_code(self,code):
        access_token = Github.exchange_code_for_token(code)
        if access_token:
            user = Github.retrieve_github_user(access_token)
            print("compelte rete",user)
            full_name = user.get('name') or user.get('login')
            email = user.get('email')

            # Get email if it's not returned directly
            if not email:
                headers = {"Authorization": f"Bearer {access_token}"}
                email_response = requests.get("https://api.github.com/user/emails", headers=headers)
                try:
                    email_data = email_response.json()
                except Exception as e:
                    print("Error parsing JSON:", e)
                    print("Raw response text:", email_response.text)
                    raise
                email = get_primary_verified_email(email_data)
            print("email_data ->", email)

            # Split full_name by space
            names = full_name.split(" ")
            firstName = names[0]
            lastName = names[1] if len(names) > 1 else "-"
            provider = "github"
            return register_social_user(provider,email,firstName,lastName)

        else:
            raise ValidationError("token is invalid or has expired")
def get_primary_verified_email(email_data):
    for item in email_data:
        if item.get("primary") and item.get("verified"):
            return item.get("email")
    return None