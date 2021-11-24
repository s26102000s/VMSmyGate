from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

def unauthenticated_user(view_f):
    def wrapper_f(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('visit:dashboard'))
        else:
            return view_f(request, *args, **kwargs)

    return wrapper_f

"""
def admin_only(view_f):
    def wrapper_f(request, *args, **kwargs):
        if request.user.is_staff:
            return view_f(request, *args, **kwargs)
        else:
            return redirect(reverse('vms:employee_profile'))

    return wrapper_f


def allowed_user(view_f):
    def wrapper_f(request, *args, **kwargs):
        if request.user.is_staff:
            return view_f(request, *args, **kwargs)
        else:
            return HttpResponse("You are not allowed on this page!!")
    return wrapper_f
"""