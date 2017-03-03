# bultin library

# external libraries
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text

app = Sanic()

"""
POST /tasks
GET /tasks
GET /task/<id>
PUT /task/<id>
"""

class Oscar(HTTPMethodView):
    def get(self, request, task):
        return text('I am get method')

    def post(self, request, task):
        return text('I am post method')

    def put(self, request, task):
        return text('I am put method')

class TaskList(HTTPMethodView):
    def post(self, request):
        """
        Create a task out of the post json body.
        """
        return json({
        })


app.add_route(Oscar.as_view(), '/<task>')

if __name__ == '__main__':
    app.run(
        debug=True,
        host="127.0.0.1",
        port=8000
    )
