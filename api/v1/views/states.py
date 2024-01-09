#!/usr/bin/python3
"""Handling routes for state."""

from models import storage
from models.state import State
from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieve all states."""
    state_list = []
    state = storage.all("State")
    for data in state.values():
        state_list.append(data.to_dict())


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Create state."""
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
    """Retrieve state by id."""
    obj = storage.get("State", str(state_id))

    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Update state by id."""
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    obj = storage.get("State", str(state_id))
    if obj is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, val)
    obj.save()
    return jsonify(obj.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete state by Id."""
    obj = storage.get("State", str(state_id))

    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return jsonify({})
