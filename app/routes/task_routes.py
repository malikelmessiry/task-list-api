from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from .route_utilities import validate_model, create_model_from_dict
from ..db import db

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# create a new task
@bp.post("")
def create_task():
    request_body = request.get_json()

    try:
        new_task = create_model_from_dict(Task, request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
        
    return new_task.to_dict(), 201


# read all tasks

# read one task 

# update task

# delete task
