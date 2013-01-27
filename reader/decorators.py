import sys
import re

from django.shortcuts import render_to_response
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url as _url
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

_IPHONE_UA = re.compile(r'Mobile.*Safari')
def _is_iphone(request):
    return _IPHONE_UA.search(request.META['HTTP_USER_AGENT']) is not None

def _get_module():
    caller = sys._getframe(2).f_code.co_filename
    for m in sys.modules.values():
        if m and '__file__' in m.__dict__ and m.__file__.startswith(caller):
            return m

def view(pattern, template=None, require_login=False, *url_args, **url_kwargs):
    if type(template) is bool:
        require_login = template
        template = None

    module = _get_module()
    package = module.__package__.split('.')[-1]

    def _wrapper(func):
        if require_login:
            func = login_required(func)

        def _handle_request(request, *args, **kwargs):
            result = func(request, *args, **kwargs) or dict()
            if template and isinstance(result, dict):
                path = 'iphone' if _is_iphone(request) else 'web'
                return render_to_response('%s/%s' % (path, template), RequestContext(request, result))
            else:
                return result 

        if module:
            if 'urlpatterns' not in module.__dict__:
                module.urlpatterns = []
            url_kwargs.setdefault('name', func.func_name)
            module.urlpatterns += patterns('', _url(pattern, _handle_request, *url_args, **url_kwargs))

        return _handle_request
    return _wrapper

