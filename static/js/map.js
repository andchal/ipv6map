var ajax = {};
ajax.x = function () {
    if (typeof XMLHttpRequest !== 'undefined') {
        return new XMLHttpRequest();
    }
    var versions = [
        "MSXML2.XmlHttp.6.0",
        "MSXML2.XmlHttp.5.0",
        "MSXML2.XmlHttp.4.0",
        "MSXML2.XmlHttp.3.0",
        "MSXML2.XmlHttp.2.0",
        "Microsoft.XmlHttp"
    ];

    var xhr;
    for (var i = 0; i < versions.length; i++) {
        try {
            xhr = new ActiveXObject(versions[i]);
            break;
        } catch (e) {
        }
    }
    return xhr;
};

ajax.send = function (url, callback, method, data, async) {
    if (async === undefined) {
        async = true;
    }
    var x = ajax.x();
    x.open(method, url, async);
    x.onreadystatechange = function () {
        if (x.readyState == 4) {
            callback(x.responseText)
        }
    };
    if (method == 'POST') {
        x.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    }
    x.send(data)
};

ajax.get = function (url, data, callback, async) {
    var query = [];
    for (var key in data) {
        query.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
    }
    ajax.send(url + (query.length ? '?' + query.join('&') : ''), callback, 'GET', null, async)
};

var map = L.map('map').setView([35.808347191214935, -78.69918823242188], 10);

var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors | &copy; maxmind',
}).addTo(map);

var url = "http://localhost:5000/ipv6/api/v1.0/locations";

var fmtBBox = function(bbox) {
    return {
        "lowerx": bbox._southWest.lng,
        "lowery": bbox._southWest.lat,
        "upperx": bbox._northEast.lng,
        "uppery": bbox._northEast.lat
    }
};

var reloadHeatMap = function(event) {
    try {
        ajax.get(url, fmtBBox(map.getBounds()), function(points) { heat.setLatLngs(JSON.parse(points)) }, true);
    } catch(e) {
    };
};

var points;
try {
    ajax.get(url, fmtBBox(map.getBounds()), function(result) {points=JSON.parse(result)}, false);
} catch(e) {
};

var heat = L.heatLayer(points, {radius: 55, blur: 20}).addTo(map);

map.on({
    moveend: reloadHeatMap,
    }
);