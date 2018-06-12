from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def home(request):
    if request.user.is_authenticated():
        return redirect('/volunteer/slots')
    else:
        return redirect('/login')
