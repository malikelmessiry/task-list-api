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

    return {"task": new_task.to_dict()}, 201

# read all tasks
@bp.get("")
def get_all_tasks():
    # create a basic select query without any filtering
    query = db.select(Task)

    tasks = db.session.scalars(query.order_by(Task.id))

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    # ^ can turn into list comprehension:
    # tasks_response = [task.to_dict() for task in tasks]

    return tasks_response

    # # If we have a `title` query parameter, we can add on to the query object
    # title_param = request.args.get("title")
    # if title_param:
    #     # Match the title_param exactly, including capitalization
    #     # query = query.where(Book.title == title_param)

    #     # If we want to allow partial matches, we can use the % wildcard with `like()`
    #     # If `title_param` contains "Great", the code below will match 
    #     # both "The Great Gatsby" and "Great Expectations"
    #     # query = query.where(Book.title.like(f"%{title_param}%"))

    #     # If we want to allow searching case-insensitively, 
    #     # we can use ilike instead of like
    #     query = query.where(Book.title.ilike(f"%{title_param}%"))

    # # If we have other query parameters, we can continue adding to the query. 
    # # As we did above, we must reassign the `query`` variable to capture the new clause we are adding. 
    # # If we don't reassign `query``, we are calling the `where` function but are not saving the resulting filter
    # description_param = request.args.get("description")
    # if description_param:
    #     # In case there are books with similar titles, we can also filter by description
    #     query = query.where(Book.description.ilike(f"%{description_param}%"))

    # books = db.session.scalars(query.order_by(Book.id))
    # # We could also write the line above as:
    # # books = db.session.execute(query).scalars()



# read one task 

# update task

# delete task
