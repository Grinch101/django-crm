from .models import Activities
from apps.user.models import Users
from apps.contacts.models import Contacts
from CRM.utility import json_output, pass_pop, login_required
from CRM.settings import SECRET_KEY
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.http import JsonResponse


class activity(APIView):

    @method_decorator(login_required)
    def get(self, request, user_id, contact_id):
        user_obj = Users.objects.get(id=user_id)
        try:
            contact_obj = Contacts.objects.get(id=contact_id, user_id=user_obj)
        except ObjectDoesNotExist:
            return json_output(error="Contact was not found", status=400)
        try:
            rows = Activities.objects.filter(
                user_id=user_obj, contact_id=contact_obj)
            output_list = []
            for row in rows:
                output_list.append({
                    'action': row.action,
                    'description': row.description,
                    'activity_id': row.id,
                    'date': row.date,
                    'time': row.time,
                    'contact_id': contact_id
                })
            return json_output(
                data=output_list,
                info=f'all activities for contact {contact_id} retrived!'
            )
        except ObjectDoesNotExist:
            return json_output(error='No activity was found!', status=404)

    @method_decorator(login_required)
    def post(self, request, user_id, contact_id):
        user_obj = Users.objects.get(id=user_id)
        try:
            contact_obj = Contacts.objects.get(id=contact_id, user_id=user_obj)
        except ObjectDoesNotExist:
            # Not Found!
            return json_output(error="Contact was not found", status=404)
        try:
            description = request.data['description']
        except:
            description = None
        try:
            action = request.data['action']
            date = request.data['date']
            time = request.data['time']
        except KeyError:
            # Bad Request
            return json_output(error='Mandatory fields cannot be empty', status=400)
        qs = Activities(action=action,
                        date=date,
                        time=time,
                        description=description,
                        user_id=user_obj,
                        contact_id=contact_obj
                        )
        qs.save()
        activity_id = qs.id
        attrs = ['action', 'description', 'time', 'date', 'id']
        data = {attr: getattr(qs, attr) for attr in attrs}
        return json_output(data=data, info='Activity added')


@login_required
@api_view(['DELETE'])
def delete_activity(request, user_id, contact_id, activity_id):
    user_obj = Users.objects.get(id=user_id)
    try:
        contact_obj = Contacts.objects.get(id=contact_id, user_id=user_obj)
    except ObjectDoesNotExist:
        # Not Found!
        return json_output(error="Contact was not found", status=404)
    try:
        qs = Activities.objects.get(id=activity_id,
                                    user_id=user_obj,
                                    contact_id=contact_obj
                                    )
        attrs = ['action', 'description', 'time', 'date', 'id']
        data = {attr: getattr(qs, attr, None) for attr in attrs}
        qs.delete()
        return json_output(info='Activity is deleted', data=data)
    except ObjectDoesNotExist:
        # Not Found!
        return json_output(info='Activity was not found', status=404)
