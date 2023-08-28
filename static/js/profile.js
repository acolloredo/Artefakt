// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // GENERAL
        is_gallery_edit: false,
        //////////////////////

        // PROFILE DATA 
        followed_galleries: [],
        owned_galleries: [],
        //////////////////////

        // EDIT GALLERY DATA
        edit_gallery: null,
        edit_gallery_id: 0,
        edit_gallery_idx: 0,
        edit_gallery_name: "",
        edit_gallery_description: "",
        edit_gallery_inventory: [],
        //////////////////////
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.get_followed_galleries = () => {
        axios.get(get_followed_galleries_url).then( (res) => {
            app.vue.followed_galleries = app.enumerate(res.data.followed_galleries);
            console.log(app.vue.followed_galleries)
        });
    }

    app.get_owned_galleries = () => {
        axios.get(get_owned_galleries_url).then( (res) => {
            app.vue.owned_galleries = app.enumerate(res.data.owned_galleries);
        })
    }

    app.goto_gallery_edit = (g_idx) => {
        app.vue.edit_gallery = app.vue.owned_galleries[g_idx]
        app.vue.edit_gallery_id = app.vue.edit_gallery.id
        app.vue.edit_gallery_name = app.vue.edit_gallery.name
        app.vue.edit_gallery_description = app.vue.edit_gallery.description

        axios.get(get_gallery_inventory_url, {
            params: { gallery_id: app.vue.edit_gallery_id },
        }).then((res) => {
            app.vue.edit_gallery_inventory = app.enumerate(res.data.gallery_inventory);
            app.vue.is_gallery_edit = true;
        });
    }

    app.edit_gallery_details = () => {
        axios.post(edit_gallery_details_url, {
             gallery_id: app.vue.edit_gallery_id,
             new_name: app.vue.edit_gallery_name,
             new_descr: app.vue.edit_gallery_description
        }).then(() => {
            document.getElementById('edit_gallery_modal').classList.remove('is-active');
        }) 
    }

    // This contains all the methods.
    app.methods = {
        goto_gallery_edit: app.goto_gallery_edit,
        edit_gallery_details: app.edit_gallery_details
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        app.get_followed_galleries()
        app.get_owned_galleries()
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
