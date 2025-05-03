from flask import Blueprint, abort, make_response, request, Response
from dotenv import load_dotenv
from app.models.task import Task
from .route_utilities import validate_model, create_model_from_dict
from datetime import datetime, timezone
import os
import requests
from ..db import db
load_dotenv()

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# create a new task
@bp.post("")
def create_task():
    request_body = request.get_json()

    try:
        new_task = create_model_from_dict(Task, request_body)

    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    return {"task": new_task.to_dict()}, 201

# read all tasks
@bp.get("")
def get_all_tasks():
    # create a basic select query without any filtering
    query = db.select(Task)

    sort = request.args.get("sort")

    if sort == "asc":
        query = query.order_by(Task.title.asc())
    elif sort == "desc":
        query = query.order_by(Task.title.desc())

    tasks = db.session.scalars(query)

    tasks_response = [task.to_dict() for task in tasks]

    return tasks_response


    #if you want to search by title or description:
    # if title_param:
    #     query = query.where(Task.title.ilike(f"%{title_param}%"))

    # tasks = db.session.scalars(query.order_by(Task.title))
    # # # We could also write the line above as:
    # # # books = db.session.execute(query).scalars()
    
    # # If we have other query parameters, we can continue adding to the query. 
    # # As we did above, we must reassign the `query`` variable to capture the new clause we are adding. 
    # # If we don't reassign `query``, we are calling the `where` function but are not saving the resulting filter
    # description_param = request.args.get("description")
    # if description_param:
    #     # In case there are books with similar titles, we can also filter by description
    #     query = query.where(Book.description.ilike(f"%{description_param}%"))

    # tasks = db.session.scalars(query.order_by(Task.id))

    

# read one task 
@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}, 200

# update task
@bp.put("/<task_id>")
def update_one_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

# delete task
@bp.delete("/<task_id>")
def delete_one_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now(timezone.utc)

    db.session.commit()

    # send slack message
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = os.environ.get("SLACK_CHANNEL")

    if slack_token and slack_channel:
        slack_message = {
            "channel": slack_channel,
            "text": f"Someone just completed the task {task.title}"
        }

        headers = {
            "Authorization": f"Bearer {slack_token}",
            "Content-Type": "application/json"
        }

        # sends request to slack
        slack_response = requests.post("https://slack.com/api/chat.postMessage", json=slack_message, headers=headers)

        # #optional error handling
        # if not slack_response.ok:
        #     print("Slack API error": slack_response.status_code, slack_response.text)

        # can refactor here into a helper function for the slack message

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return Response(status=204, mimetype="application/json")

