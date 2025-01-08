from rest_framework import serializers
from . import models


class TaskRetrievalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Task
        exclude = ['project']
