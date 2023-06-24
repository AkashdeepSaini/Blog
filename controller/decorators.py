from django.core.exceptions import PermissionDenied
from .models import Author , Article

def relevant_user_required(function):
    """
    Decorator function for authorized user  access
    """
    def wrap(request, *args, **kwargs):
        try:
            article_obj = Article.objects.get(id = kwargs['pk'])
        except:
            return function(request, *args, **kwargs)
        if args[0].user.id == article_obj.author.id:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap