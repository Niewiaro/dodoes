from uuid import uuid4

import pytest

from src.entities.todo import Todo
from src.exceptions import TodoNotFoundError
from src.todos import service as todos_service
from src.todos.model import TodoCreate


class TestTodosService:
    def test_create_todo(self, db_session, test_token_data) -> None:
        todo_create = TodoCreate(
            description="New Description"
        )

        new_todo = todos_service.create_todo(test_token_data, db_session, todo_create)
        assert new_todo.description == "New Description"
        assert new_todo.user_id == test_token_data.get_uuid()
        assert not new_todo.is_completed

    def test_get_todos(self, db_session, test_token_data, test_todo) -> None:
        test_todo.user_id = test_token_data.get_uuid()
        db_session.add(test_todo)
        db_session.commit()

        todos = todos_service.get_todos(test_token_data, db_session)
        assert len(todos) == 1
        assert todos[0].id == test_todo.id

    def test_get_todos_empty(self, db_session, test_token_data) -> None:
        todos = todos_service.get_todos(test_token_data, db_session)
        assert len(todos) == 0

    def test_get_todos_fill_all(self, db_session, test_token_data, test_todo_fill_all) -> None:
        test_todo_fill_all.user_id = test_token_data.get_uuid()
        db_session.add(test_todo_fill_all)
        db_session.commit()

        todos = todos_service.get_todos(test_token_data, db_session)
        assert len(todos) == 1
        assert todos[0].id == test_todo_fill_all.id
        assert todos[0].description == test_todo_fill_all.description
        assert todos[0].due_date == test_todo_fill_all.due_date
        assert todos[0].starts_at == test_todo_fill_all.starts_at
        assert todos[0].is_completed == test_todo_fill_all.is_completed
        assert todos[0].priority == test_todo_fill_all.priority

    def test_get_todo_by_id(self, db_session, test_token_data, test_todo) -> None:
        test_todo.user_id = test_token_data.get_uuid()
        db_session.add(test_todo)
        db_session.commit()

        todo = todos_service.get_todo_by_id(test_token_data, db_session, test_todo.id)
        assert todo.id == test_todo.id

        with pytest.raises(TodoNotFoundError):
            todos_service.get_todo_by_id(test_token_data, db_session, uuid4())

    def test_update_todo(self, db_session, test_token_data, test_todo) -> None:
        test_todo.user_id = test_token_data.get_uuid()
        db_session.add(test_todo)
        db_session.commit()

        updated_description = "Updated Description"
        todo_update = TodoCreate(description=updated_description)
        updated_todo = todos_service.update_todo(
            test_token_data,
            db_session,
            test_todo.id,
            todo_update
        )
        assert updated_todo.description == updated_description
        assert updated_todo.id == test_todo.id

        with pytest.raises(TodoNotFoundError):
            todos_service.update_todo(
                test_token_data,
                db_session,
                uuid4(),
                TodoCreate(description="Should Fail")
            )

    def test_complete_todo(self, db_session, test_token_data, test_todo) -> None:
        test_todo.user_id = test_token_data.get_uuid()
        db_session.add(test_todo)
        db_session.commit()

        completed_todo = todos_service.complete_todo(test_token_data, db_session, test_todo.id)
        assert completed_todo.is_completed
        assert completed_todo.completed_at is not None

    def test_delete_todo(self, db_session, test_token_data, test_todo) -> None:
        test_todo.user_id = test_token_data.get_uuid()
        db_session.add(test_todo)
        db_session.commit()

        todos_service.delete_todo(test_token_data, db_session, test_todo.id)
        assert db_session.query(Todo).filter_by(id=test_todo.id).first() is None
