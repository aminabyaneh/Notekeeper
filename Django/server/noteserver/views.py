import threading
import time
import json

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from noteserver.models import Notebook
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.middleware.csrf import get_token
from django.core.mail import send_mail

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
def create_notebook(request):
    json_received = json.loads(request.body)
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in :(', status=403)
    elif Notebook.objects.filter(name=json_received['name'], user=request.user).exists():
        response = HttpResponse('Notebook already exists :(', status=409)
    else:
        notebook = Notebook.objects.create(name=json_received['name'], data=json_received['data'])
        notebook.user = request.user
        notebook.save()
        response = HttpResponse('Notebook created successfully :)', status=200)
    return response

@require_POST
def update_notebook(request):
    json_received = json.loads(request.body)
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in :(', status=403)
    elif not Notebook.objects.filter(name=json_received['name'], user=request.user).exists():
        response = HttpResponse('Notebook does not exist :(', status=409)
    else:
        notebook = Notebook.objects.filter(name=json_received['name'], user=request.user).first()
        notebook.data = json_received['data']
        notebook.save()
        response = HttpResponse('Notebook updated successfully :)', status=200)
    return response

@require_GET
def get_notebook(request):
    json_received = json.loads(request.body)
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in :(', status=403)
    elif not Notebook.objects.filter(name=json_received['name'], user=request.user).exists():
        response = HttpResponse('Note book does not exist :(', status=404)
    else:
        notebook = Notebook.objects.filter(name=json_received['name'], user=request.user).first()
        response = HttpResponse(json.dumps(model_to_dict(notebook)), status=200)
    return response

@require_POST
def set_timer(request):
    if request.user.is_authenticated:
        json_received = json.loads(request.body)
        # email after mentioned time
        threading.Thread(target=send_reminder, args=(json_received['username'],
                                                     json_received['name'], 
                                                     json_received['data'],)).start()
        response = HttpResponse('Reminder set successfuly :)', status=200)
    else:
        response = HttpResponse('You are not logged in :(', status=401)
    return response

def send_reminder(email, name, data):
        timeout = float(data)
        while time.time() < timeout:
            time.sleep(1)
            continue
        res = send_mail("Reminder", "Hi!\nyou have a reminder for note " + name, "aminabyaneh@gmail.com", [email])

