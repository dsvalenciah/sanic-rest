import json

from app import app


def test_post_to_tasks_fail_if_no_title_given():
    req, res = app.test_client.post('/tasks', data='{}')
    assert res.status == 400


def test_post_to_tasks_succeds_if_title_given():
    req, res = app.test_client.post('/tasks', data='{"title":"Hola"}')
    assert res.status == 201


def test_post_to_tasks_fail_if_titleisempty():
    req, res = app.test_client.post('/tasks', data='{"title":""}')
    assert res.status == 400


def test_done_should_be_false_on_create():
    req, res = app.test_client.post('/tasks', data='{"title":"Hola"}')
    task = json.loads(res.body)
    assert not task['done']


def test_title_should_be_set_as_the_users():
    req, res = app.test_client.post('/tasks', data='{"title":"Hola"}')
    task = json.loads(res.body)
    assert task['title'] == 'Hola'
