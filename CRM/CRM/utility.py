from django.http import JsonResponse
from functools import wraps
from CRM.settings import SECRET_KEY
from apps.user.models import Users
from jwt import DecodeError
from django.core import serializers
import jwt


def json_output(data='', error='', info='', status=200):
    output_dic = {'data': data,
                  'error': error,
                  'info': info}
    return JsonResponse(data=output_dic, safe=True, status=status)


def login_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        token = request.headers['JWT']
        if token:
            try:
                payload = jwt.decode(token, key=SECRET_KEY,
                                     algorithms=["HS256"])
                user_id = int(payload['user_id'])
                rows = Users.objects.filter(id=user_id)
                if len(rows) > 0:
                    return func(request, user_id=rows[0].id, *args, **kwargs)
                else:
                    # not found!
                    return json_output(error='User not found!', status=404)
            except DecodeError as e:
                # forbidden!
                return json_output(error=f'Token invalid,  {e}', status=403)
        else:
            # unauthorized!
            return json_output(error='Please login!', status=401)
    return wrap


def pass_pop(row):
    user_id = row.id
    email = row.email
    client_name = row.client_name
    return {'user_id': user_id,
            'email': email,
            'client_name': client_name}
