from flask import Blueprint, abort, make_response, request, Response
from dotenv import load_dotenv
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model, create_model_from_dict
import os
import requests
from ..db import db
load_dotenv()


bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# create a new goal
@bp.post("")
def create_goal():
    request_body = request.get_json()
    
    try:
        new_goal = create_model_from_dict(Goal, request_body)
    except KeyError as e:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    return {"goal": new_goal.to_dict()}, 201

# get all goals
@bp.get("")
def get_all_goals():
    query = db.select(Goal)

    goals = db.session.scalars(query)

    return [goal.to_dict() for goal in goals]

# get one goal
@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}, 200

# update one goal
@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

# delete one goal
@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# send a list of tasks to a goal
@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    task_ids = request_body.get("task_ids", []) 

    for task_id in task_ids: # add helper function here
        task = validate_model(Task, task_id)
        task.goal_id = goal.id

    db.session.commit()

    return {"id": goal.id, "task_ids": task_ids}, 200

# getting tasks of one goal
@bp.get("/<goal_id>/tasks")
def get_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(), 200