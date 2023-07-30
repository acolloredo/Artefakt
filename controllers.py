"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from py4web.utils.factories import Inject
from .models import get_user_email

url_signer = URLSigner(session)


@action('index')
@action.uses('index.html', db, auth)
def index():
    return dict(
    )


@action('gallery')
@action.uses('gallery.html', db, auth, url_signer)
def gallery():
    return dict(
        get_galleries_url=URL('get_galleries', signer=url_signer),
        get_items_from_gallery_url=URL(
            'get_items_from_gallery', signer=url_signer),
    )


@action('item')
@action.uses('item.html', db, auth, url_signer)
def item():
    return dict(
        get_items_url=URL('get_items', signer=url_signer),
        get_items_from_gallery_url=URL(
            'get_items_from_gallery', signer=url_signer),
        gallery_id=0
    )


@action('item/<gallery_id:int>')
@action.uses('item.html', db, auth)
def item_from_gallery(gallery_id=None):
    print(
        f"******************ITEM FROM GALLERY YAY {gallery_id}****************************")
    if gallery_id is None:
        return item()
    else:
        return dict(
            get_items_url=URL('get_items', signer=url_signer),
            get_items_from_gallery_url=URL(
                'get_items_from_gallery', signer=url_signer),
            gallery_id=gallery_id
        )


@action('get_galleries')
@action.uses(db, auth, url_signer, auth.user)
def get_galleries():
    all_galleries = db(db.gallery).select().as_list()
    return dict(all_galleries=all_galleries)


@action('get_items')
@action.uses(db, auth, url_signer, auth.user)
def get_items():
    all_items = db(db.collection_item).select().as_list()
    return dict(all_items=all_items)


@action('get_items_from_gallery')
@action.uses(db, auth, url_signer, auth.user)
def get_items_from_gallery():
    gallery_inventory_ids = (
        db(db.gallery.id == request.params.get("gallery_id"))
        .select(db.gallery.collection_items)
        .as_list()[0]["collection_items"]
    )

    gallery_inventory = db(db.collection_item.id.belongs(
        gallery_inventory_ids)).select().as_list()

    return dict(gallery_inventory=gallery_inventory)
