from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sqlite.db"
db = SQLAlchemy(app)

app.app_context().push()


class ToDoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    summary = db.Column(db.String(500))


# db.create_all()

# class HelloWorld(Resource):
#     def get(self):
#         return {'data': 'Hello, World!'}
#
#
# class HelloName(Resource):
#     def get(self, name):
#         return {'data': f'Hello,{name}'}


# api.add_resource(HelloWorld, '/helloworld')
# api.add_resource(HelloName, '/helloworld/<string:name>')

# todos = {
#     1: {"task": "Learnt to make api using flask",
#         "summary": "Program to create rest api in python using flask and flask RESTful"},
#     2: {"task": "Task 2",
#         "summary": "summary for task 2"},
#     3: {"task": "Task 3",
#         "summary": "summary for task 3"}
# }

resource_fields = {
    "id": fields.Integer,
    "task": fields.String,
    "summary": fields.String
}


task_post_args = reqparse.RequestParser()
task_post_args.add_argument("task", type=str, help="Task is required", required=True)
task_post_args.add_argument("summary", type=str, help="Summary is required", required=True)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("task", type=str)
task_put_args.add_argument("summary", type=str)


class ToDo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        # return todos[todo_id]
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, message="Task not found in To do List")
        return task

    @marshal_with(resource_fields)
    def post(self, todo_id):
        args = task_post_args.parse_args()
        # if todo_id not in todos:
        #     abort(409, "Task Id already exists")
        # todos[todo_id] = {"task": args["task"], "summary": args["summary"]}
        # return todos[todo_id]
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if task:
            abort(409, message="Task Id already exists")

        todo = ToDoModel(id=todo_id, task=args["task"], summary=args["summary"])
        db.session.add(todo)
        db.session.commit()
        return todo, 201

    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = task_put_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, message="Task not in To do List, couldn't update")
        if args["task"]:
            task.task = args["task"]
        if args["summary"]:
            task.summary = args["summary"]
        db.session.commit()
        return task

    def delete(self, todo_id):
        task = ToDoModel.query.filter_by(id=todo_id).first()
        db.session.delete(task)
        db.session.commit()
        return 'Task deleted from To Do list', 204


class ToDoList(Resource):
    def get(self):
        tasks = ToDoModel.query.all()
        todos = {}
        for task in tasks:
            todos[task.id] = {"task": task.task, "summary": task.summary}
        return todos


api.add_resource(ToDo, '/todo/api/<int:todo_id>')
api.add_resource(ToDoList, '/todo/api/all')

# get localhost:5000/helloworld
# Hello, World!
# get localhost:5000/helloworld/Akshata
# Hello, Akshata

if __name__ == '__main__':
    app.run(debug=True)
