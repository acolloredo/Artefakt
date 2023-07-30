// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // ITEM DATA
        all_items: [],
        grouped_items: [],
        //////////////////////

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

        // ITEM SEARCH DATA
        search_query: "",
        search_items: [],
        grouped_search: [],
        is_displaying_search: false,
        ///////////////////////////
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.group_items = (items) => {
        let group = []
        let grouped = []
        for (let i = 0; i < items.length; i++){
            group.push(items[i])
            if (group.length >= 3){
                grouped.push(group)
                group = []
            }
        }
        if (group.length > 0){
            grouped.push(group)
        }
        return grouped
    }

    app.get_items = () => {
        axios.get(get_items_url).then((res) => {
            app.vue.all_items = app.enumerate(res.data.all_items);
            app.vue.grouped_items = app.group_items(app.vue.all_items);
        });
    };

    app.open_item_details = (i_idx) => {
        app.vue.curr_item = app.vue.all_items[i_idx]
        app.vue.curr_item_id = app.vue.curr_item.id
        app.vue.curr_item_title = app.vue.curr_item.title
        app.vue.curr_item_artist = app.vue.curr_item.artist
        app.vue.curr_item_type = app.vue.curr_item.type
        app.vue.curr_item_origin = app.vue.curr_item.origin
        app.vue.curr_item_time_period = app.vue.curr_item.time_period
        app.vue.curr_item_status = app.vue.curr_item.status
        document.getElementById("item_view_modal").classList.add("is-active");
    }

    app.search = () => {
        app.vue.search_items = [];
        app.vue.grouped_search = [];
        app.vue.is_displaying_search = true;

        if (app.vue.search_query == "") {
            app.vue.is_displaying_search = false;
            return;
        }

        for (i of app.vue.all_items) {
            if (i.title.toLowerCase().startsWith(app.vue.search_query.toLowerCase()) ||
                i.artist.toLowerCase().startsWith(app.vue.search_query.toLowerCase())) {
                app.vue.search_items.push(i);
            }
        }
        app.vue.grouped_search = app.group_items(app.vue.search_items);
    };

    app.clear = () => {
        app.vue.is_displaying_search = false;
        app.vue.search_query = "";
    };

    // This contains all the methods.
    app.methods = {
        open_item_details: app.open_item_details,
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
        app.get_items();
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
