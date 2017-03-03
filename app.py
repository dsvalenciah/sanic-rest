# bultin library

# external libraries
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json
from uuid import uuid4

app = Sanic()

"""
POST /tasks
GET /tasks
GET /task/<id>
PUT /task/<id>
"""


DATOS = {}


class TaskList(HTTPMethodView):

    def post(self, request):
        """
        Create a task out of the post json body.
        """
        print(request.json)
        host = request.headers.get('Host')
        uid = uuid4().hex
        task = {
            'id': uid,
            'title': 'Comprar leche',
            'done': False,
            'url': f'http://{host}/tasks/{uid}'
        }
        DATOS.update({uid: task})
        return json(task)

    def get(self, request):
        """
        Lists all the tasks available, could support pagination.
        """
        return json({
            'data': DATOS,
        })


class Task(HTTPMethodView):

    def get(self, request, task):
        """
        Shows the details of an individual task.
        """
        task = DATOS.get(task)
        if task is None:
            return json({
                'error': {
                    'code': 'TASK_NOT_FOUND',
                    'message': 'That task was not found',
                }
            }, status=404)
        return json(task)

    def put(self, request, task):
        task = DATOS.get(task)
        if task is None:
            return json({
                'error': {
                    'code': 'TASK_NOT_FOUND',
                    'message': 'That task was not found',
                }
            }, status=404)
        print(request.json)
        task.update({
            'done': True
        })
        DATOS.update({task['id']: task})
        return json(task)


app.add_route(TaskList.as_view(), '/tasks')
app.add_route(Task.as_view(), '/tasks/<task>')

if __name__ == '__main__':
    app.run(
        debug=True,
        host="127.0.0.1",
        port=8000
    )
