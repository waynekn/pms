from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response

from pms.utils import camel_case_to_snake_case

from . import serializers
from . import models


class TaskCreateView(generics.CreateAPIView):
    """
    View for creating a new task.

    This view handles POST requests for creating a new task.
    """
    model = models.Task
    serializer_class = serializers.TaskCreationSerializser

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data

        transformed_data = camel_case_to_snake_case(data)

        serializer = self.get_serializer(data=transformed_data)

        if serializer.is_valid():
            task = serializer.save()
            serialized_task = serializers.TaskRetrievalSerializer(task)
            return Response(serialized_task.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
