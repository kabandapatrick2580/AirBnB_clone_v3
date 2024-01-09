#!/usr/bin/python3
"""Handling routes for state."""

from models import storage
from models.state import State
from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """Retrieve all states."""
    state_list = []
    state_objects = storage.all("State")
    for state_instance in state_objects.values():
        state_list.append(state_instance.to_dict())


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_new_state():
    """Create a new state."""
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')
    state = State(**state_json)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieve a state by its ID."""
    state_obj = storage.get("State", str(state_id))

    if state_obj is None:
        abort(404)
    return jsonify(state_obj.to_dict())


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state_by_id(state_id):
    """Update a state by its ID."""
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    state_obj = storage.get("State", str(state_id))
    if state_obj is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, val)
    state_obj.save()
    return jsonify(state_obj.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """Delete a state by its ID."""
    state_obj = storage.get("State", str(state_id))

    if state_obj is None:
        abort(404)

    storage.delete(state_obj)
    storage.save()

    return jsonify({})
