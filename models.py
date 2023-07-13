"""
This file defines the database models
"""

import datetime
import random
from py4web.utils.populate import FIRST_NAMES, LAST_NAMES, IUP
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_username():
    return auth.current_user.get('username') if auth.current_user else None

def get_user_id():
    return auth.current_user.get('id') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


# Define your table below

db.define_table(
    'gallery',
    Field("owner", "integer", "reference auth_user"),
    Field("collection_items", "list:reference collection_item")
)

db.define_table(
    'collection_item',
    Field("owner", "integer", "reference auth_user"),
    Field("artist"),
    Field("type"),
    Field("creation_date", "date"),
    Field("origin"),
    Field("gallery", "integer", "reference gallery")
)

db.commit()
