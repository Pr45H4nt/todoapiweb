from rest_framework import serializers
from todoapp.models import Task

class TaskSerializer(serializers.ModelSerializer):
    #creating serializer with completed field and user field as readonly
    Completed = serializers.ReadOnlyField()
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user']
        
    
class TaskCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['Title', 'Description','Completed','user']