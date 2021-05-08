from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Create your views here.

@require_http_methods(['POST'])
def signup(req):
    return JsonResponse(data='this is sign-up page', safe=False, status=200)


@require_http_methods(['POST'])
def login(req):
    return JsonResponse(data='This is Login Page', safe=False, status=200)


@require_http_methods(['GET'])
def current_user(req):
    return JsonResponse(data='This is current user page', safe=False, status=200)


@require_http_methods(['PUT'])
def user_update(req):
    return JsonResponse(data='This is update user page', safe=False, status=200)