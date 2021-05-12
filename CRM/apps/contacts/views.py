import json
from .models import Contacts
from apps.user.models import Users
from CRM.utility import json_output, pass_pop, login_required
from CRM.settings import SECRET_KEY
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import parser_classes, api_view
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize


@login_required
@api_view(['POST'])
def add(request, user_id):
    attrs = request.data.keys()
    FirstName = request.data['FirstName']
    LastName = request.data['LastName']
    Email = request.data['Email']
    PhoneNumber = request.data['PhoneNumber']
    user_obj = Users.objects.get(id=user_id)
    contact_row = Contacts.objects.create(FirstName=FirstName,
                                          LastName=LastName,
                                          Email=Email,
                                          PhoneNumber=PhoneNumber,
                                          user_id=user_obj)
    contact_row.save()
    data = {'id':contact_row.id}
    for attr in attrs:
        data = {**data , f'{attr}':getattr(contact_row, attr)}
    return json_output(info='Contact added', data=data, status=201)


@login_required
@api_view(['GET'])
def all(request, user_id):
    user_obj = Users.objects.get(id=user_id)
    contacts_list = Contacts.objects.filter(user_id=user_obj)
    output_list = []
    for row in contacts_list:
        output_list.append({
            'FirstName': row.FirstName,
            'LastName': row.LastName,
            'Email': row.Email,
            'PhoneNumber': row.PhoneNumber,
            'contact_id': row.id,
            'user_id': user_id
        })
    return json_output(data=output_list, info='contacts retrived!')


@login_required
@api_view(['DELETE'])
def delete(request, user_id, contact_id):
    user_obj = Users.objects.get(id=user_id)
    try:
        row = Contacts.objects.get(id=contact_id)
        if row.user_id == user_obj:
            row.delete()
            # OK
            return json_output(info='contact deleted',
                               data={'deleted contact_id': contact_id}
                               )
        else:
            # Unauthorized
            return json_output(error='Unauthorized', status=401)
    except ObjectDoesNotExist:
        # Not found
        return json_output(error=f'contact_id was not found!', status=404)


@login_required
@api_view(['PUT'])
def update(request, contact_id, user_id):
    update_list = request.data.keys()
    if update_list != []:
        user_obj = Users.objects.get(id=user_id)
        try:
            contact_obj = Contacts.objects.get(id=contact_id,
                                                  user_id=user_obj)
            valid_fields = ['FirstName','LastName',
                            'Email','PhoneNumber']
            for item in update_list:
                if item not in valid_fields:
                    return json_output(error=f'invalid fields for {item}. valid fields are: {valid_fields}',
                                       status=400) # Bad request!
                setattr(contact_obj, item, request.data[item])
                contact_obj.save()
    
            data = {'id':contact_obj.id}
            for attr in valid_fields:
                data = {**data , f'{attr}':getattr(contact_obj, attr)}
            return json_output(info='updated!', data=data)  # OK
        
        except ObjectDoesNotExist:
            # Not found
            return json_output(error=f'contact_id was not found!', status=404)
    else:
        return json_output(error='Empty request', status=400)  # Bad Request!
