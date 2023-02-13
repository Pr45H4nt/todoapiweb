from django.http import JsonResponse
from rest_framework import generics , permissions
from .serializer import TaskSerializer , TaskCompletedSerializer
from todoapp.models import Task
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class TaskListApi(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated] #only authenticated user should be able to access
    def get_queryset(self):
        return Task.objects.filter(user = self.request.user) # only the current users todos are shown

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskUpdate(generics.RetrieveUpdateDestroyAPIView):
    '''
    task model is filtered by the provided id in the url
    only the current users todos are shown as coded in get_queryset method
    '''
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)


class TaskCompleted(generics.UpdateAPIView):
    serializer_class = TaskCompletedSerializer
    queryset = Task.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)

    def perform_update(self, serializer):
        serializer.instance.Completed = True
        # setting the serializer object's completed field to True
        serializer.save()
        return JsonResponse({'sucess':'Your Task is marked as completed'}, status= 204)

@csrf_exempt #as it is through api csrf_token is not req
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            #the provided json is parsed and stored in data variable as dict
            new_user = User.objects.create_user(username=data['username'], password=data['password'])
            new_user.save()
            #user is created as per the given data
            token = Token.objects.create(user=new_user)
            return JsonResponse({'token':str(token)}, status=201)
            #unique token as per the user is created
        except IntegrityError:
            return JsonResponse({'error':'This Username is already taken'}, status = 400)


@csrf_exempt 
def login(request):
    '''
    shows token of the user
    '''
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'error':'Could not login. Please check username and password'}, status=400)
        else:
            try:
                token = Token.objects.get(user=user)
                #token given if its available
            except:
                token = Token.objects.create(user=user)
                # created token if not already
            return JsonResponse({'token':str(token)}, status=200)