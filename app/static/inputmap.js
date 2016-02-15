var cities = [
        [-12.04,-77.04],
        [-33.87, 151.20],
        [-1.28, 36.81],
        [1.29, 103.85],
        [-0.18, -78.46],
        [2.20,102.24],
        [-26.20,28.03]
    ];

var city = cities[Math.floor(Math.random()*cities.length)]; //randomly picks a city from cities array

var latitude = city[0]
    longitude = city[1]
    southWest = L.latLng(-35, -180),
    northEast = L.latLng(35, 180),
    bounds = L.latLngBounds(southWest, northEast);

var inputmap = L.map('inputmap', {maxBounds:bounds}).setView([latitude, longitude ], 8);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibGluYnVnIiwiYSI6ImNpamRmZGkycDAwODR1Nmpic2U0c3UwMWgifQ.f5AsfaIZ7zIztXD2J8_a-g', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 8,
    id: 'linbug.ommeomk5',
    accessToken: 'pk.eyJ1IjoibGluYnVnIiwiYSI6ImNpamRmZGkycDAwODR1Nmpic2U0c3UwMWgifQ.f5AsfaIZ7zIztXD2J8_a-g'
}).addTo(inputmap);

marker = L.marker([latitude,longitude]).addTo(inputmap);

document.getElementById('latitude').value = latitude
document.getElementById('longitude').value = longitude

inputmap.on('click', function(e){
    latitude = Math.round(e.latlng.lat*100)/100
    longitude = Math.round(e.latlng.lng*100)/100
    document.getElementById('latitude').value = latitude
    document.getElementById('longitude').value = longitude
    marker.setLatLng(e.latlng);

});
