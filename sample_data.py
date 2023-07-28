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
#     Field("status")
# )

sample_items = [
    {
        "artist": "Vincent Van Gogh",
        "type": "painting",
        "time_period": "1850-1900",
        "title": "Starry Night",
        "origin": "Europe",
        "status": "mint"
    },
    {
        "artist": "Johannes Vermeer",
        "type": "painting",
        "time_period": "1650-1700",
        "title": "Girl with a Pearl Earring",
        "origin": "Europe",
        "status": "mint"
    },
    {
        "artist": "Leonardo Da Vinci",
        "type": "painting",
        "time_period": "1500-1550",
        "title": "Mona Lisa",
        "origin": "Europe",
        "status": "mint"
    },
    {
        "artist": "Vincent Van Gogh",
        "type": "painting",
        "time_period": "1850-1900",
        "title": "Starry Night",
        "origin": "Europe",
        "status": "mint"
    },
    {
        "artist": "Alexandros of Antioch",
        "type": "sculpture",
        "time_period": "Ancient",
        "title": "Venus de Milo",
        "origin": "Europe",
        "status": "fair"
    },
    {
        "artist": "Michelangelo",
        "type": "sculpture",
        "time_period": "1500-1550",
        "title": "David",
        "origin": "Europe",
        "status": "good"
    },
    {
        "artist": "Katsushika Hokusai",
        "type": "painting",
        "time_period": "1800-1850",
        "title": "The Great Wave off Kanagawa",
        "origin": "Asia",
        "status": "excellent"
    },
    {
        "artist": "Unknown",
        "type": "artifact",
        "time_period": "Ancient",
        "title": "Mayan Scepter",
        "origin": "South America",
        "status": "damaged"
    },
    {
        "artist": "Banksy",
        "type": "painting",
        "time_period": "2000-",
        "title": "Love is in the Bin",
        "origin": "Europe",
        "status": "damaged"
    },
    {
        "artist": "Grant Wood",
        "type": "painting",
        "time_period": "1900-1950",
        "title": "American Gothic",
        "origin": "North America",
        "status": "excellent"
    },
    {
        "artist": "Andy Warhol",
        "type": "painting",
        "time_period": "1950-2000",
        "title": "Campbell's Soup Cans",
        "origin": "North America",
        "status": "mint"
    },
    {
        "artist": "No. 5",
        "type": "painting",
        "time_period": "1900-1950",
        "title": "Jackson Pollock",
        "origin": "North America",
        "status": "mint"
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
