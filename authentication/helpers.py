from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
import functools
from django.shortcuts import redirect

def logout_required(function=None, logout_url=settings.LOGOUT_URL):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator




def verification_required(view_func, verification_url="check_email"):
    """
        this decorator restricts users who have not been verified
        from accessing the view function passed as it argument and
        redirect the user to page where their account can be activated
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.not_google_verified:
            if request.user.is_verified:
                return view_func(request, *args, **kwargs)
            return redirect(verification_url)  
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def super_user_required(view_func, verification_url=settings.LOGOUT_URL):
    
    """
        this decorator restricts users who have not been verified
        from accessing the view function passed as it argument and
        redirect the user to page where their account can be activated
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return redirect(verification_url)  
    return wrapper