from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response

from apps.tasks import models


class TaskStatusUpdateView(generics.UpdateAPIView):
    """
    Handles updating of a task status.

    This view expects a POST request with a status key whose value
    is potentially the new task status.
    """

    def put(self, request: Request, *args, **kwargs) -> Response:
        new_status = request.data.get('status')
        task_id = kwargs.get('task_id')

        if not hasattr(models.Task, new_status):
            return Response({"detail": "Invalid status choice. Status must either be \
                             'IN_PROGRESS', 'ON_HOLD' or 'DONE"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = models.Task.objects.get(pk=task_id)
        except models.Task.DoesNotExist:
            return Response({"detail": "Could not get task"}, status=status.HTTP_404_NOT_FOUND)

        task.status = new_status

        task.save()

        return Response(status=status.HTTP_200_OK)
