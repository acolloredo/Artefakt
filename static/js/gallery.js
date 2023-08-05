// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // GALLERY DATA
        all_galleries: [],
        grouped_galleries: [],
        //////////////////////

        // EXPANDED GALLERY DATA
        curr_gallery: null,
        curr_gallery_id: 0,
        curr_gallery_name: "",
        curr_gallery_description: "",
        ////////////////////////////

        // GALLERY SEARCH DATA
        search_query: "",
        search_galleries: [],
        grouped_search: [],
        is_displaying_search: false,
        ///////////////////////////

        // GALLERY PREVIEW DATA
        is_gallery_preview: false,
        gallery_id: 0,
        gallery_display_name: "",
        gallery_inventory: [],
        grouped_gallery_inventory: [],
        /////////////////////////////

        // EXPANDED ITEM DATA
        curr_item: null,
        curr_item_id: 0,
        curr_item_title: "",
        curr_item_artist: "",
        curr_item_type: "",
        curr_item_origin: "",
        curr_item_time_period: "",
        curr_item_status: "",
        ////////////////////////////
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.group_arr = (arr) => {
        console.log("grouping")
        let group = []
        let grouped = []
        for (let i = 0; i < arr.length; i++){
            group.push(arr[i])
            if (group.length >= 3){
                grouped.push(group)
                group = []
            }
        }
        if (group.length > 0){
            grouped.push(group)
        }
        console.log(grouped)
        return grouped
    }

    app.get_galleries = () => {
        axios.get(get_galleries_url).then((res) => {
            app.vue.all_galleries = app.enumerate(res.data.all_galleries);
            app.vue.grouped_galleries = app.group_arr(app.vue.all_galleries);
        });
    };

    app.open_gallery_details = (g_idx) => {
        app.vue.curr_gallery = app.vue.all_galleries[g_idx]
        app.vue.curr_gallery_id = app.vue.curr_gallery.id
        app.vue.curr_gallery_name = app.vue.curr_gallery.name
        app.vue.curr_gallery_description = app.vue.curr_gallery.description
        document.getElementById("gallery_view_modal").classList.add("is-active");
    }

    app.search = () => {
        app.vue.search_galleries = [];
        app.vue.grouped_search = [];
        app.vue.is_displaying_search = true;

        if (app.vue.search_query == "") {
            app.vue.is_displaying_search = false;
            return;
        }

        for (g of app.vue.all_galleries) {
            if (g.name.toLowerCase().startsWith(app.vue.search_query.toLowerCase())) {
                app.vue.search_galleries.push(g);
            }
        }
        app.vue.grouped_search = app.group_arr(app.vue.search_galleries);
    };

    app.get_items_from_gallery = (gallery_id, gallery_name) => {
        console.log("Gallery ID: ", gallery_id)
        console.log("Gallery Name: ", gallery_name)
        app.vue.gallery_id = gallery_id
        app.vue.gallery_display_name = gallery_name
        axios.get(get_items_from_gallery_url, {
            params: { gallery_id: app.vue.gallery_id },
        }).then((res) => {
            app.vue.gallery_inventory = app.enumerate(res.data.gallery_inventory);
            app.vue.grouped_gallery_inventory = app.group_arr(app.vue.gallery_inventory);
            app.vue.is_gallery_preview = true
        });
    };

    app.open_item_details = (i_idx) => {
        app.vue.curr_item = app.vue.gallery_inventory[i_idx]
        app.vue.curr_item_id = app.vue.curr_item.id
        app.vue.curr_item_title = app.vue.curr_item.title
        app.vue.curr_item_artist = app.vue.curr_item.artist
        app.vue.curr_item_type = app.vue.curr_item.type
        app.vue.curr_item_origin = app.vue.curr_item.origin
        app.vue.curr_item_time_period = app.vue.curr_item.time_period
        app.vue.curr_item_status = app.vue.curr_item.status
        document.getElementById("item_view_modal").classList.add("is-active");
    }

    app.clear = () => {
        app.vue.is_displaying_search = false;
        app.vue.search_query = "";
    };

    app.back_to_browse = () => {
        app.vue.is_gallery_preview = false
        app.vue.gallery_id = 0
        app.vue.gallery_display_name = ""
        app.vue.gallery_inventory = []
        app.vue.grouped_gallery_inventory = []

        app.vue.search_query = ""
        app.vue.is_displaying_search = false
    }

    // This contains all the methods.
    app.methods = {
        open_gallery_details: app.open_gallery_details,
        search: app.search,
        clear: app.clear,
        open_item_details: app.open_item_details,
        get_items_from_gallery: app.get_items_from_gallery,
        back_to_browse: app.back_to_browse
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        app.get_galleries();
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
