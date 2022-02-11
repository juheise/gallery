function BrowseParams() {

    const params = new Proxy(new URLSearchParams(window.location.search), {
        get: (searchParams, prop) => searchParams.get(prop),
    });

    const intValue = function(value, defaultValue) {
        const n = parseInt(value);
        if (isNaN(n)) {
            return defaultValue;
        }
        return n;
    }

    const strValue = function(value, defaultValue) {
        if (value === null) {
            return defaultValue;
        }
        return value.toString();
    }

    return {
        offset: intValue(params.offset, 0),
        limit: intValue(params.limit, 100),
        order_by: strValue(params.order_by, "shot_datetime"),
        order: strValue(params.order, "desc"),
        start_date: strValue(params.start_date, ""),
        end_date: strValue(params.end_date, ""),

        toQueryString: function() {
            let p = new URLSearchParams();
            p.set("offset", this.offset);
            p.set("limit", this.limit);
            p.set("order_by", this.order_by);
            p.set("order", this.order);
            p.set("start_date", this.start_date);
            p.set("end_date", this.end_date);
            return p.toString();
        }
    }
}

function applyDateFilter() {
    let params = new BrowseParams();
    params.start_date = document.getElementById("start_date").value;
    params.end_date = document.getElementById("end_date").value;
    params.offset = 0;
    window.location.search = params.toQueryString();
}

function nextPage() {
    let params = new BrowseParams();
    params.offset += params.limit;
    window.location.search = params.toQueryString();
}

function prevPage() {
    let params = new BrowseParams();
    params.offset = Math.max(params.offset - params.limit, 0);
    window.location.search = params.toQueryString();
}

function orderDateAsc() {
    let params = new BrowseParams();
    params.order_by = "shot_datetime";
    params.order = "asc";
    params.offset = 0;
    window.location.search = params.toQueryString();
}

function orderDateDesc() {
    let params = new BrowseParams();
    params.order_by = "shot_datetime";
    params.order = "desc";
    params.offset = 0;
    window.location.search = params.toQueryString();
}
