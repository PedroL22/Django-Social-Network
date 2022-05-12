from django.http import Http404
from django.shortcuts import redirect

def groupcheck(*groups):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            else:
                return redirect('/')
            raise Http404

        return wrapper

    return decorator