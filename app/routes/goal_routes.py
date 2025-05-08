from flask import Blueprint, abort, make_response, request, Response
from dotenv import load_dotenv
from app.models.goal import Goal
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