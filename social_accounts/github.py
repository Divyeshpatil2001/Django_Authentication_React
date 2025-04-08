import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class Github:
    @staticmethod
    def exchange_code_for_token(code):
        param_payload = {
            "client_id":settings.GITHUB_CLIENT_ID,
            "client_secret":settings.GITHUB_CLIENT_SECRET,
            "code":code
        }
        try:
            print(param_payload)
            res = requests.post("https://github.com/login/oauth/access_token",params=param_payload,headers={'Accept': 'application/json'})
            res.raise_for_status()
        except Exception as e:
            print("error",e)
            raise AuthenticationFailed("Failed to exchange code for token")
        payload = res.json()
        print("pay",payload)
        if "error" in payload:
            raise AuthenticationFailed(f"GitHub OAuth Error: {payload.get('error_description', 'Unknown error')}")
        token = payload.get("access_token")
        print("tojen",token)
        if not token:
            raise AuthenticationFailed("GitHub authentication failed. No access token received.")
        print(token)
        return token

    @staticmethod
    def retrieve_github_user(access_token):
        print("under retrireve")
        try:
            headers = {
                "Authorization":f"Bearer {access_token}"
            }
            response = requests.get("https://api.github.com/user",headers=headers)
            user_data = response.json()
            return user_data
        
        except Exception as e:
            raise AuthenticationFailed(detail="token is invalid or has expired")