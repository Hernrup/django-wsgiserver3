from django.http import HttpResponse, HttpResponseBadRequest
import django.http
# RequestContext always uses django.core.context_processors.csrf
from django.template import Context, RequestContext, loader
from django.core.context_processors import csrf
import autoload_test

def index(request):
    template = loader.get_template('tests.html')
    c = RequestContext(request)
    #c.update(csrf(request))
    return HttpResponse(template.render(c))

    
def testajax(request):
    # figuring out how to get csrftoken from this side of django
    # print "called testajax: ", request
    method = request.META['REQUEST_METHOD']
    c = RequestContext(request)
    # print "********************"
    # print "RequestContext info:"
    # ['autoescape', 'dicts', 'current_app', 'render_context', 'use_l10n', 'use_tz']
    # print c.META # c.dicts[1]['csrf_token'] # __dict__.keys()
    #try:
    #    print "request.META['HTTP_X_CSRFTOKEN']:", request.META['HTTP_X_CSRFTOKEN']
    #except:
    #    pass
    # .set_cookie('X-CSRFToken', csrftoken)
    if  method == 'GET':
        if request.is_ajax():
            return HttpResponse('here is the response to your ajax GET',
            content_type="text/plain")
        else:
            return HttpResponse('here is the response to your GET request')
    elif method == 'POST':
        if request.is_ajax():
            return HttpResponse('here is the response to your ajax POST')
        else:
            return HttpResponse('here is the response to your POST request')
    elif method == 'PUT':
        return HttpResponse('here is the response to your ajax PUT')
    elif method == 'DELETE':
        return HttpResponse('here is the response to your ajax DELETE')
    else:
        return HttpResponse('here is the response to the unrecognized request method %s' %method)
        # HttpResponseBadRequest ?


import autoload_test

def testautoreload(request):
    return HttpResponse("%s" % autoload_test.x)
    