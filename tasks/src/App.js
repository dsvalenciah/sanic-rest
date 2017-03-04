import React, { Component } from 'react';
import './App.css';
import request from 'superagent';
import _ from 'lodash';


class TaskInput extends Component {

  constructor(props) {
    super(props);
    this.state = {
      title: ''
    }
  }

  render() {
    return (
      <form onSubmit={this.onSubmit.bind(this)}>
        <input
          type="text"
          value={this.state.title}
          onChange={e => this.setState({title: e.target.value})}
        />
        <input type='submit' value='Create task' />
      </form>
    )
  }

  onSubmit(event) {
    event.preventDefault();
    request('POST', 'http://localhost:8000/tasks/')
      .send(this.state)
      .set('Content-Type', 'application/json')
      .set('Accept', 'application/json')
      .then(res => {
        console.log(res);
        this.props.onCreated();
      }, err => {
        console.log(err);
      });
  }

}

class TaskList extends Component {

  render() {
    return (
      <ul>
        { _.map(this.props.tasks, task => (
          <li
            key={task.id}
            style={{
              textDecoration: task.done ? 'line-through' : 'initial',
            }}
            onClick={() => this.completeTask(task)}
          >
            { task.title }
          </li>
        )) }
      </ul>
    )
  }

  completeTask(task) {
    request('PUT', `http://localhost:8000/tasks/${task.id}`)
      .send({done: !task.done})
      .set('Content-Type', 'application/json')
      .set('Accept', 'application/json')
      .then(res => {
        console.log(res);
        this.props.onUpdate();
      }, err => {
        console.log(err);
      });
  }

}

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      tasks: []
    }
  }

  render() {
    return (
      <div className="App">
        <TaskInput
          onCreated={() => this.fetchTasks()}
        />
        <TaskList
          tasks={this.state.tasks}
          onUpdate={() => this.fetchTasks()}
        />
      </div>
    );
  }

  fetchTasks() {
    request('GET', 'http://localhost:8000/tasks/')
      .set('Content-Type', 'application/json')
      .set('Accept', 'application/json')
      .then(res => {
        console.log(res);
        this.setState({tasks: res.body.data});
      }, err => {
        console.log(err);
      });
  }

  componentDidMount() {
    this.fetchTasks();
  }
}

export default App;
