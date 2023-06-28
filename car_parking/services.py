from django.contrib.auth import get_user_model



def authenticate(username=None, password=None, **kwargs):
    User = get_user_model()
    try:
        user = User.objects.get(phone_number=username)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
    if user.check_password(password):
        return user
    return None
