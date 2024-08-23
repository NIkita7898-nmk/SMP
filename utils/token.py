from rest_framework.response import Response
from rest_framework_simplejwt.tokens import UntypedToken

class UserMixin:
    def get_user(self):

        auth_header = self.request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            decoded_data = UntypedToken(token)
            user_id = decoded_data.get("user_id")
            return user_id
        else:
            return Response({"error": "Token not found or invalid"}, status=400)
