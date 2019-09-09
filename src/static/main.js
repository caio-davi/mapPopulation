L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    'Imagery © <a href="https://www.openstreetmap.org">OpenStreetMap</a>'
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

function drawCircle(circle) {
  messageContents = {
    data: {
      location: {
        type: "Circle",
        units: "Meters",
        radius: circle.getRadius(),
        coordinates: circle.toGeoJSON().geometry.coordinates
      },
      points: document.getElementById("rasterPointsChk").checked
    }
  };
  var settings = {
    type: "POST",
    url: "/population",
    data: JSON.stringify(messageContents),
    dataType: "json",
    contentType: "application/json"
  };
  $.ajax(settings).done(function(response) {
    console.log(response);
    var population = response.data.population;
    circle.population = population;
    circle.editable = true;
    color = "blue";
    circle.setStyle({
      color: color,
      opacity: 0.8,
      weight: 2,
      fillColor: color,
      fillOpacity: 0.35
    });
    circle.bindPopup(circleInfo(circle));
    for (let i = 0; i < response.data.points.length; i++) {
      var point = L.marker(
        [response.data.points[i][1], response.data.points[i][0]],
        { icon: redCrossIcon }
      );
      point.addTo(rasterPoints);
    }
  });
}

function circleInfo(circle) {
  if (circle._mRadius >= 1000) {
    var mileRadius = (Math.pow(circle._mRadius / 1000, 2) * 3.14).toFixed(2);
    var contents =
      "<b>Coverage Area: </b>" + conversion(mileRadius) + " sq mi<br>";
  } else {
    var mileRadius = (Math.pow(circle._mRadius, 2) * 3.14).toFixed(2);
    var contents =
      "<b>Coverage Area: </b>" + conversion(mileRadius) + " sq ft<br>";
  }
  contents =
    contents +
    "<b>Population: </b>" +
    Number(circle.population).toFixed(2) +
    "<br>";
  return contents;
}

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
