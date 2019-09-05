L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    'Imagery © <a href="https://www.openstreetmap.org">OpenStreetMap</a>',
  maxZoom: 18
}).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var rasterPoints = new L.FeatureGroup();
rasterPoints.addTo(drawnItems);

var drawControl = new L.Control.Draw({
  draw: {
    polyline: false,
    polygon: false,
    marker: false,
    rectangle: false,
    circle: {
      metric: false
    }
  },
  edit: {
    featureGroup: drawnItems,
    edit: false
  }
});
map.addControl(drawControl);

map.on("draw:created", function(e) {
  var type = e.layerType;
  circle = e.layer;
  drawnItems.addLayer(circle);
  drawCircle(circle);
});

map.on("draw:edited", function(e) {
  drawCircle(circle);
});

function drawCircle(circle) {}

function clearRasterPoints() {
  map.removeLayer(rasterPoints);
}

function coordsToLgdLat(coords) {
  return [coords[1], coords[0]];
}

function conversion(value) {
  var miles = (value / 1.61).toFixed(2);
  return miles;
}

Number.prototype.pad = function(size) {
  var s = String(this);
  while (s.length < (size || 2)) {
    s = "0" + s;
  }
  return s;
};
