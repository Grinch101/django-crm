from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

# Create your views here.

@require_http_methods(['GET'])
def index(req):
    return JsonResponse(data='This is index page', safe=False, status=200)


@require_http_methods(['POST'])
def add(req):
    return JsonResponse(data='This is contact-add page', safe=False, status=200)


@require_http_methods(['GET'])
def all(req):
    return JsonResponse(data='This is contact-all page', safe=False, status=200)

@require_http_methods(['DELETE'])

def delete(req, id):
    return JsonResponse(data=f'This is contact-delete page for id: -- {id}', safe=False, status=200)


@require_http_methods(['PUT'])
def update(req, id):
    return JsonResponse(data=f'This is contact-update page  for id: -- {id}', safe=False, status=200)

