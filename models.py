"""
This file defines the database models
"""

from .common import db, Field
from pydal.validators import *

# Define your table below
#
# db.define_table('thing', Field('name'))
#
# always commit your models to avoid problems later


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
