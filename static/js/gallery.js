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
        is_displaying_search: false
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.group_galleries = (galleries, grouped) => {
        let group = []
        for (let i = 0; i < galleries.length; i++){
            group.push(galleries[i])
            if (group.length >= 3){
                grouped.push(group)
                group = []
            }
        }
        if (group.length > 0){
            grouped.push(group)
        }
        console.log(grouped)
    }

    app.get_galleries = () => {
        axios.get(get_galleries_url).then((res) => {
            app.vue.all_galleries = app.enumerate(res.data.all_galleries);
            app.group_galleries(app.vue.all_galleries, app.vue.grouped_galleries);
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
        app.group_galleries(app.vue.search_galleries, app.vue.grouped_search);
    };

    app.clear = () => {
        app.vue.is_displaying_search = false;
        app.vue.search_query = "";
    };

    // This contains all the methods.
    app.methods = {
        open_gallery_details: app.open_gallery_details,
        search: app.search,
        clear: app.clear
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
