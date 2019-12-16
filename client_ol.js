// Centrage de la carte sur Montpellier
// La base Open Street Map est utilisée pour récupérer les "tuiles"
var map = new ol.Map({
target: 'map',
layers: [new ol.layer.Tile({source: new ol.source.OSM()})],
view: new ol.View({
center: ol.proj.fromLonLat([3.876716,43.61]),
zoom: 14
})
});
// Création d’un marqueur qui s’affiche via l’image créée dans la page HTML
let marker = document.getElementById('marker');
map.addOverlay(new ol.Overlay({
position: ol.proj.fromLonLat([3.8766716,43.6141]),
positioning: 'center-center',
element: marker
}));
// Création d’un message (cela pourrait etre une popup) quand le marqueur est sélectionné
let popup = document.getElementById('popup');
map.addOverlay(new ol.Overlay({
positioning: 'center-center',
offset : [20, -25],
position: ol.proj.fromLonLat([3.8766716,43.6141]),
element: popup
}));
// Affichage / désaffichage du message
marker.addEventListener('click', function(evt) {
(popup.style.display == "none" ? popup.style.display = "block" :
popup.style.display = "none")
});