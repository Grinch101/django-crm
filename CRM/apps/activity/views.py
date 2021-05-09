from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from rest_framework.views import APIView
# Create your views here.


class activity(APIView):
    def get(self, req, contact_id):
        return JsonResponse(data=f'all activities using GET for {contact_id}', status=200, safe=False)

    def post(self, req, contact_id):
        return JsonResponse(data=f'add page for activity to contact {contact_id}', status=201, safe=False)


@require_http_methods(['DELETE'])
def delete_activity(req, contact_id, activity_id):
    return JsonResponse(data=f'delete {activity_id} from contact {contact_id}', status=200, safe=False)
