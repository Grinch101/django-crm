import jwt
import json
import datetime as dt
from .models import Users
from CRM.utility import json_output, pass_pop, login_required
from CRM.settings import SECRET_KEY
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.decorators import api_view, parser_classes


@api_view(['POST'])
def signup(request):
    email = request.data['inputEmail']
    passkey = request.data['inputPassword']
    client_name = request.data['client_name']
    if all([email, passkey, client_name]):
        rows = Users.objects.filter(email=email)
        if len(rows) > 0:
            # Not Acceptable
            return json_output(error='signup failed, email in use!', status=409) # Conflict!
        else:
            row = Users(email=email, passkey=passkey, client_name=client_name)
            row.save()
            user_id = Users.objects.filter(email=email, passkey=passkey,
                                           client_name=client_name)[0].id
            # OK
            return json_output(info='user added!', data={'user_id': user_id}, status=201) # OK
    else:
        # Bad Request
        return json_output(error='incomplete request', status=400) # Bad Request!


@api_view(['POST'])
def login(request, format=None):
    email = request.data['inputEmail']
    passkey = request.data['inputPassword']
    rows = Users.objects.filter(email=email)
    if len(rows) > 0:
        if rows[0].passkey == passkey:
            # Generate TOKEN
            TEP = dt.timedelta(weeks=4)  # TEP: TOKEN EXPIRATION PERIOD
            TOKEN = jwt.encode(payload={'user_id': rows[0].id,
                                        'exp': dt.datetime.utcnow() + TEP},
                               key=SECRET_KEY,
                               algorithm="HS256")
            return json_output(info='Logged in, token generated',
                               data=TOKEN)  # OK
        else:
            return json_output(error='Wrong Email or Password! please retry!',
                               status=401)  # Unauthorized
    else:
        return json_output(error='Email Not Found, please sign up!',
                           status=404)  # Not Found


@login_required
@api_view(['GET'])
def current_user(request, user_id):
    row = Users.objects.get(id=user_id).id
    data = pass_pop(row)
    return json_output(info='user retrived!', data=data) # OK


@login_required
@api_view(['PUT'])
def user_update(request, user_id):
    update_list = list(dict(request.data).keys())
    if update_list != []:
        user_obj = Users.objects.get(id=user_id)
        if 'client_name' in update_list:
            user_obj.client_name = request.data['client_name']

        if 'email' in update_list:
            user_obj.email = request.data['email']

        if 'passkey' in update_list:
            user_obj.passkey = request.data['passkey']

        user_obj.save()
        row = Users.objects.get(id=user_obj.id)
        data = pass_pop(row)
        
        return json_output(info='updated!', data=data) # OK

    else:
        return json_output(error='Empty request', status=400)  # Bad Request!
