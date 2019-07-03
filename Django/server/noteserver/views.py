
import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from noteserver.models import Notebook
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.middleware.csrf import get_token

# Create your views here.

@require_http_methods(["GET", "POST"])
def login_user(request):
    if request.method == "GET":
        response = HttpResponse(json.dumps({'csrf status': 'active', 'csrfchip': get_token(request)}), status=200)
        return response
    else:
        json_data = json.loads(request.body)
        password_in = json_data['password']
        username_in = json_data['username']
        user = authenticate(request, username=username_in, password=password_in)
        if user is not None:
            login(request, user)
            response = HttpResponse('Login Successful. Welcome ' + user.first_name, status=200)
        else:
            response = HttpResponse('Login Failed. Invalid username or password.', status=401)
        return response

@require_POST
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        response = HttpResponse('Logout Successful', status=200)
    else:
        response = HttpResponse('You haven''t been logged in!!!', status=401)
    return response


@require_POST
def signup_user(request):
    json_received = json.loads(request.body)
    if 'username' not in json_received or 'password' not in json_received:
        response = HttpResponse('Not enough data', status=400)
    elif User.objects.filter(username=json_received['username']).exists():
        response = HttpResponse('Email already in use :(', status=409)
    else:
        user = User.objects.create_user(username=json_received['username'], password=json_received['password'])
        user.save()
        response = HttpResponse('Signup was successful :)', status=200)
    return response


@require_POST
def update_notebook(request):
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Folder.objects.filter(name=request.json['folder_name']).exists():
        response = HttpResponse('No folder with said name', status=400)
    elif Note.objects.filter(name=request.json['name'], folder_name=request.get['folder_name'],
                             user=request.user).exists():
        response = HttpResponse('Notebook already exists already', status=409)
    else:
        note = Notebook.objects.create(name=request.json['name'], folder_name=request.json['folder_name'],
                                   data=request.json['data'])
        note.user = request.user
        note.y_m = int(request.json['y_m'])
        note.m_m = int(request.json['m_m'])
        note.d_m = int(request.json['d_m'])
        note.h_m = int(request.json['h_m'])
        note.min_m = int(request.json['min_m'])
        note.s_m = int(request.json['s_m'])
        if 'y_r' in request.json:
            note.y_r = int(request.json['y_r'])
            note.m_r = int(request.json['m_r'])
            note.d_r = int(request.json['d_r'])
            note.h_r = int(request.json['h_r'])
            note.min_r = int(request.json['min_r'])
            note.s_r = int(request.json['s_r'])
        else:
            note.y_r = 0
            note.m_r = 0
            note.d_r = 0
            note.h_r = 0
            note.min_r = 0
            note.s_r = 0
        note.save()
        folder = Folder.objects.filter(folder_name=note.folder_name)
        folder.list_notes = folder.list_notes + "," + note.name
        folder.save()
        response = HttpResponse('Note saved successfully', status=200)
    return response

