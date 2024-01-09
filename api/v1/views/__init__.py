#!/usr/bin/python3
"""Initialization of views module."""
from flask import Blueprint

# Create a Blueprint for the API views with the name 'app_views' and a URL prefix '/api/v1'
app_views = Blueprint('/api/v1', __name__, url_prefix='/api/v1')

# Import views from index, states, and cities submodules
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
