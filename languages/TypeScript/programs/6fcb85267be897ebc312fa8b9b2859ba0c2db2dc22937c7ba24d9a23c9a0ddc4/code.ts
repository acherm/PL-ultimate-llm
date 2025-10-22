import express from 'express';
import bodyParser from 'body-parser';

const app = express();
const port = 3000;

app.use(bodyParser.json());

let todos: { id: number; task: string; completed: boolean }[] = [];

app.get('/todos', (req, res) => {
  res.json(todos);
});

app.post('/todos', (req, res) => {
  const newTodo = { id: todos.length + 1, task: req.body.task, completed: false };
  todos.push(newTodo);
  res.status(201).json(newTodo);
});

app.put('/todos/:id', (req, res) => {
  const todo = todos.find(t => t.id === parseInt(req.params.id));
  if (!todo) return res.status(404).send('Todo not found');
  todo.completed = req.body.completed;
  res.json(todo);
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});