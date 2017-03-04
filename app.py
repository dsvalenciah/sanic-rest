# bultin library
from uuid import uuid4

# external libraries
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json

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
        title = request.json.get('title')

        if not title:
            return json({
                'error': {
                    'code': 'TITLE_REQUIRED',
                    'message': 'The title field is required',
                }
            }, status=400)

        uid = uuid4().hex
        task = {
            'title': title,
            'id': uid,
            'done': False,
        }
        DATOS.update({uid: task})
        return json(task, status=201)

    def get(self, request):
        """
        Lists all the tasks available, could support pagination.
        """
        return json({
            'data': DATOS,
        })

    def options(self, request):
        return json({})


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
            'title': request.json.get('title', task['title']),
            'done': request.json.get('done', task['done']),
        })
        DATOS.update({task['id']: task})
        return json(task, status=201)

    def delete(self, request, task):
        """
        Delete a task from the database.
        """
        return json({})

    def options(self, request, task):
        return json({})


app.add_route(TaskList.as_view(), '/tasks')
app.add_route(Task.as_view(), '/tasks/<task>')


@app.middleware('response')
async def cross_site_resource_sharing(request, response):
    allowed_methods = 'GET,POST,PUT,DELETE,OPTIONS'
    # response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = allowed_methods
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'


if __name__ == '__main__':
    app.run(
        debug=True,
        host="127.0.0.1",
        port=8000
    )
