from django.contrib.auth import get_user_model
from django.contrib.auth.backends import (AllowAllUsersModelBackend,
                                          ModelBackend)
from oidc_provider.models import Token

UserModel = get_user_model()


class BasicAuthBackend(AllowAllUsersModelBackend):
    def validate_bearer_token(self, token):
        try:
            token = Token.objects.get(access_token=token)
            if token:
                client_email = token.client.contact_email
                user = UserModel.objects.filter(email=client_email).first()

                if self.user_can_authenticate(user):
                    return user
        except Exception as e:
            raise e

        return None

    def authenticate(self, request, *args, **kwargs):
        if "HTTP_AUTHORIZATION" in request.META:
            jwt = request.META["HTTP_AUTHORIZATION"]

            if jwt.lower().startswith("bearer"):
                jwt = jwt[7:]
                return self.validate_bearer_token(jwt)

        return ModelBackend().authenticate(request, *args, **kwargs)
