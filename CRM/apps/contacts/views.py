import jwt
import datetime as dt
from .models import Contacts
from apps.user.models import Users
from CRM.utility import json_output, pass_pop, login_required
from CRM.settings import SECRET_KEY
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from django.core import serializers
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


@login_required
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
def add(request, user_id):
    data_list = list(dict(request.data).keys())
    if len(data_list) < 2:
        # Bad Request!
        return json_output(error='incomplete request!', status=400)
    else:
        name = request.data['Name']
        phone = request.data['Number']
        user_obj = Users.objects.get(id=user_id)
        if user_obj is None or user_obj == []:
            # not found!
            return json_output(error='User not found!', status=404)
        else:
            new_row = Contacts.objects.create(
                name=name, phone=phone, user_id=user_obj)
            new_row.save()
            qs = Contacts.objects.filter(
                name=name, phone=phone, user_id=user_obj)[0]
            data = {'name': qs.name,
                    'phone': qs.phone,
                    'user_id': user_id,
                    'contact_id': qs.id}
            # created!
            return json_output(info='Contact added', data=data, status=201)


@login_required
@api_view(['GET'])
@parser_classes([FormParser, MultiPartParser])
def all(request, user_id):
    user_obj = Users.objects.get(id=user_id)
    contacts_list = Contacts.objects.filter(user_id=user_obj)
    output_list = []
    for row in contacts_list:
        output_list.append({
            'name': row.name,
            'phone': row.phone,
            'contact_id': row.id,
            'user_id': user_id
        })
    return json_output(data=output_list, info='contacts retrived!')


@login_required
@api_view(['DELETE'])
@parser_classes([FormParser, MultiPartParser])
def delete(request, user_id, contact_id):
    user_obj = Users.objects.get(id=user_id)
    try:
        row = Contacts.objects.get(id=contact_id)
        if row.user_id == user_obj:
            row.delete()
            # OK
            return json_output(info='contact deleted', data={'deleted contact_id': contact_id})
        else:
            # Unauthorized
            return json_output(error='Unauthorized', status=401)
    except ObjectDoesNotExist:
        # Not found
        return json_output(error=f'contact_id was not found!', status=404)


@login_required
@api_view(['PUT'])
@parser_classes([FormParser, MultiPartParser])
def update(request, contact_id, user_id):
    update_list = list(dict(request.data).keys())
    if update_list != []:
        user_obj = Users.objects.get(id=user_id)
        try:
            contact_obj = Contacts.objects.filter(
                id=contact_id, user_id=user_obj)[0]
            if 'new_name' in update_list:
                contact_obj.name = request.data['new_name']
            if 'new_phone' in update_list:
                contact_obj.phone = request.data['new_phone']
            contact_obj.save()
            data = {'name': contact_obj.name,
                    'phone': contact_obj.phone}
            return json_output(info='updated!', data=data)  # OK

        except ObjectDoesNotExist:
            # Not found
            return json_output(error=f'contact_id was not found!', status=404)

    else:
        return json_output(error='Empty request', status=400)  # Bad Request!
