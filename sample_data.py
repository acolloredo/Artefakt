from .common import db, Field, auth

# db.define_table(
#     'gallery',
#     Field("owner", "integer", "reference auth_user"),
#     Field("name"),
#     Field("collection_items", "list:reference collection_item")
# )

# db.define_table(
#     'collection_item',
#     Field("owner", "integer", "reference auth_user"),
#     Field("artist"),
#     Field("type"),
#     Field("time_period"),
#     Field("title"),
#     Field("origin"),
#     Field("condition"),
#     Field("status")
# )

sample_items = [
    {
        "artist": "Vincent Van Gogh",
        "type": "painting",
        "time_period": "1850-1900",
        "title": "Starry Night",
        "origin": "Europe",
        "condition": "mint",
        "status": "on display",
        "location": "room 302"
    },
    {
        "artist": "Johannes Vermeer",
        "type": "painting",
        "time_period": "1650-1700",
        "title": "Girl with a Pearl Earring",
        "origin": "Europe",
        "condition": "mint",
        "status": "on display",
        "location": "room 302"
    },
    {
        "artist": "Leonardo Da Vinci",
        "type": "painting",
        "time_period": "1500-1550",
        "title": "Mona Lisa",
        "origin": "Europe",
        "condition": "mint",
        "status": "on display",
        "location": "room 302"
    },
    {
        "artist": "Vincent Van Gogh",
        "type": "painting",
        "time_period": "1850-1900",
        "title": "Vase with Fifteen Sunflowers",
        "origin": "Europe",
        "condition": "mint",
        "status": "on display",
        "location": "room 302"
    },
    {
        "artist": "Alexandros of Antioch",
        "type": "sculpture",
        "time_period": "Ancient",
        "title": "Venus de Milo",
        "origin": "Europe",
        "condition": "fair",
        "status": "storage",
        "location": "n/a"
    },
    {
        "artist": "Michelangelo",
        "type": "sculpture",
        "time_period": "1500-1550",
        "title": "David",
        "origin": "Europe",
        "condition": "good",
        "status": "storage",
        "location": "n/a"
    },
    {
        "artist": "Katsushika Hokusai",
        "type": "painting",
        "time_period": "1800-1850",
        "title": "The Great Wave off Kanagawa",
        "origin": "Asia",
        "condition": "excellent",
        "status": "on display",
        "location": "room 10"
    },
    {
        "artist": "Unknown",
        "type": "artifact",
        "time_period": "Ancient",
        "title": "Mayan Scepter",
        "origin": "South America",
        "condition": "damaged",
        "status": "on display",
        "location": "room 333"
    },
    {
        "artist": "Banksy",
        "type": "painting",
        "time_period": "2000-",
        "title": "Love is in the Bin",
        "origin": "Europe",
        "condition": "damaged",
        "status": "on display",
        "location": "room 302"
    },
    {
        "artist": "Grant Wood",
        "type": "painting",
        "time_period": "1900-1950",
        "title": "American Gothic",
        "origin": "North America",
        "condition": "excellent",
        "status": "on display",
        "location": "room 104"
    },
    {
        "artist": "Andy Warhol",
        "type": "painting",
        "time_period": "1950-2000",
        "title": "Campbell's Soup Cans",
        "origin": "North America",
        "condition": "mint",
        "status": "on display",
        "location": "room 2"
    },
    {
        "artist": "Jackson Pollock",
        "type": "painting",
        "time_period": "1900-1950",
        "title": "No. 5",
        "origin": "North America",
        "condition": "mint",
        "status": "storage",
        "location": "n/a"
    }
]

sample_galleries = [
    {
        "name": "Colloredo Collections",
        "description": "Colloredo Collections is a curated vintage and design store based in Austria and the Czech Republic, hosting a variety of weird and wonderful collectibles."
    },
    {
        "name": "Santa Cruz Gallery",
        "description": "Boasting a litany of unique pieces from around the globe, the Santa Cruz Gallery is sure to have something to catch anyone's eye!"
    },
    {
        "name": "Hydra Slaughterhouse",
        "description": "Located just 2 hours from Athens on the island of Hydra, the Slaughterhouse is certainly a fascinating exhibition to keep your eye on, with new exhibitions from a wide range of artists rotating yearly"
    },
    {
        "name": "Oblarn Oddities",
        "description": "Currently out of stock -- Please follow to make sure to be notified when we acquire new inventory!"
    }
]


def add_test_user():
    db(db.auth_user.email.startswith("_")).delete()

    test_user = dict(
        email="_johndoe" + "@ucsc.edu",
        first_name="John",
        last_name="Doe",
        password="1111",
    )

    test_user_id = auth.register(test_user, send=False)
    db.commit()
    return test_user_id


def add_items_for_testing():
    db(db.collection_item).delete()

    item_ids = []
    uid = (
        db(db.auth_user.email.startswith("_johndoe@ucsc.edu")).select("id").first()
    )

    for i in sample_items:
        id = db.collection_item.insert(
            owner=uid,
            artist=i["artist"],
            type=i["type"],
            time_period=i["time_period"],
            title=i["title"],
            origin=i["origin"],
            condition=i["condition"],
            status=i["status"]
        )
        item_ids.append(id)

    db.commit()
    return item_ids


def add_galleries_for_testing(item_ids):
    db(db.gallery).delete()

    item_subsets = [item_ids[:4], item_ids[4:8], item_ids[8:], []]
    uid = (
        db(db.auth_user.email.startswith("_johndoe@ucsc.edu")).select("id").first()
    )

    for idx, g in enumerate(sample_galleries):
        db.gallery.insert(
            owner=uid,
            name=g["name"],
            description=g["description"],
            collection_items=item_subsets[idx]
        )

    db.commit()
    return


def add_test_data():
    uid = add_test_user()
    item_ids = add_items_for_testing()
    add_galleries_for_testing(item_ids)
    db.commit()
