
var map = L.map('map').setView([latitude,longitude], 5);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibGluYnVnIiwiYSI6ImNpamRmZGkycDAwODR1Nmpic2U0c3UwMWgifQ.f5AsfaIZ7zIztXD2J8_a-g', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'linbug.ommeomk5',
    accessToken: 'pk.eyJ1IjoibGluYnVnIiwiYSI6ImNpamRmZGkycDAwODR1Nmpic2U0c3UwMWgifQ.f5AsfaIZ7zIztXD2J8_a-g'
}).addTo(map);

var marker = L.marker([latitude,longitude]).addTo(map);
