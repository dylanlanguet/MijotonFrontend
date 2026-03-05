from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class MijotonOIDCBackend(OIDCAuthenticationBackend):

    def verify_claims(self, claims):
        """Seul le 'sub' (identifiant unique Keycloak) est requis, pas l'email."""
        return "sub" in claims

    def filter_users_by_claims(self, claims):
        """Recherche l'utilisateur par username (preferred_username) au lieu de l'email."""
        username = claims.get("preferred_username")
        if not username:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(username__iexact=username)

    def create_user(self, claims):
        """Crée un utilisateur Django depuis les claims Keycloak."""
        username = claims.get("preferred_username", claims.get("sub"))
        email = claims.get("email", "")
        user = self.UserModel.objects.create_user(
            username=username,
            email=email,
            first_name=claims.get("given_name", ""),
            last_name=claims.get("family_name", ""),
        )
        return user

    def update_user(self, user, claims):
        """Met à jour l'utilisateur Django avec les claims Keycloak."""
        user.email = claims.get("email", user.email)
        user.first_name = claims.get("given_name", user.first_name)
        user.last_name = claims.get("family_name", user.last_name)
        user.save()
        return user
