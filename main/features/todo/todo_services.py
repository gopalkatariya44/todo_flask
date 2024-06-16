from main import db
from main.features.todo.todo_models import Todo


class TodoServices:
    @staticmethod
    def todo_list(user_id, title=None, description=None, is_complete=None, start_date=None, end_date=None):
        query = Todo.query.filter(Todo.user_id == user_id)

        if title:
            query = query.filter(Todo.title.ilike(f"%{title}%"))

        if description:
            query = query.filter(Todo.description.ilike(f"%{description}%"))

        if is_complete is not None:
            query = query.filter(Todo.is_complete == is_complete)

        if start_date:
            query = query.filter(Todo.date_time >= start_date)

        if end_date:
            query = query.filter(Todo.date_time <= end_date)

        return query.all()

    @staticmethod
    def create_todo(todo):
        db.session.add(todo)
        db.session.commit()

    @staticmethod
    def get_todo(todo_id):
        return Todo.query.filter_by(id=todo_id).first()

    @staticmethod
    def update_todo(todo):
        db.session.merge(todo)
        db.session.commit()

    @staticmethod
    def delete_todo(todo_id):
        todo = TodoServices.get_todo(todo_id)
        db.session.delete(todo)
        db.session.commit()

    @staticmethod
    def update_is_complete(todo_id):
        todo = TodoServices.get_todo(todo_id)
        todo.is_complete = False if todo.is_complete else True
        db.session.merge(todo)
        db.session.commit()
