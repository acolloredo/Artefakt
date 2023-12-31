"""
This file defines the database models
"""

import datetime
import random
from py4web.utils.populate import FIRST_NAMES, LAST_NAMES, IUP
from .common import db, Field, auth
from pydal.validators import *
from pydal.tools.tags import Tags
from .sample_data import add_test_data


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
    Field("owner", "integer", "reference auth_user",
          default=lambda: get_user_id()),
    Field("name"),
    Field("description"),
    Field("collection_items", "list:reference collection_item")
)

db.define_table(
    'collection_item',
    Field("owner", "integer", "reference auth_user",
          default=lambda: get_user_id()),
    Field("artist"),
    Field("type"),
    Field("time_period"),
    Field("title"),
    Field("origin"),
    Field("condition"),
    Field("status"),
    Field("location")
)

db.define_table(
    'inventory',
    Field("user_id", "integer", "reference auth_user",
          default=lambda: get_user_id()),
    Field("followed_galleries", "list:reference gallery", default=lambda: list()),
    Field("watchlist", "list:reference collection_item", default=lambda: list()),
)

# followed_galleries = Tags(db.auth_user, "followed_galleries")
# watchlist = Tags(db.auth_user, "watchlist")

# add_test_data()

db.commit()
