console.log("Dans le JS");


$.getJSON("http://localhost:5000/json"+window.location.pathname, function(data) {
// data est la liste renvoyée par le serveur
markersPI = []; // Liste des marqueurs
popupsPI = [];
// Liste des popups
nbPI = 0; // nombre de points d’intéret pris en charge
$.each(data, function(indice, liste) {

//
//
//
//Liste contient les infos du PI :

//liste[0] : nom
//erreur en dessous yavais liste[1} et liste[2}
//liste[1] : latitude
//liste[2] : longitude

// La liste <ul> pis est complétée
let html = "<li>"+liste[0]+" ("+liste[1]+":"+liste[2]+")</li>";
$("#pis").append(html); // syntaxe JQuery pour sélectionner la liste pis
// et y intégrer les informations concernant le point d’intéret
// Un marqueur est créé pour chaque point d’intéret
markersPI.push(document.getElementById('marker').cloneNode());
markersPI[nbPI].id = nbPI;
map.addOverlay(new ol.Overlay({
position: ol.proj.fromLonLat([liste[2],liste[1]]),
positioning: 'center-center',
element: markersPI[nbPI]
}));
// Une popup est créée pour chaque point d’intéret
popupsPI.push(document.getElementById('popup').cloneNode());
popupsPI[nbPI].innerHTML = ""+liste[0];
popupsPI[nbPI].id = "popup"+nbPI;
popupsPI[nbPI].style.color = "black";
map.addOverlay(new ol.Overlay({
positioning: 'center-center',
offset : [20, -25],
position: ol.proj.fromLonLat([liste[2],liste[1]]),
element: popupsPI[nbPI]
}));
// On associe à chaque marqueur un gestionnaire d’événements :
// quand l’utilisateur clique sur le marqueur soit la popup est affichée, soit elle est désaffichée
markersPI[nbPI].addEventListener('click', function(evt) {
let popup = document.getElementById("popup"+evt.target.id);
(popup.style.display == "none" ? popup.style.display = "block" :
popup.style.display = "none")
});
nbPI++;
});
});


console.log("Dans le JS2");

//La double liste deroulante. 
$('#rei').change(function(){
    //on enleve les elements de la deuxieme liste
    $('#asuka').children('option').remove();
    //on enleve le bouton valider
    $('#nausicaa').remove();

    console.log("inside");
    //la valeur selectionne par defaut, on a mis un selected dans le html
    var valueSelected = this.value;
    console.log("kimii");
    console.log(valueSelected);
    //on appelle le backend pour avoir la liste des categories et on ajoute les options de la deuxieme liste
	$.getJSON("http://localhost:5000/jsonn/PI/"+valueSelected, function(data) {
	$.each(data, function(indice, liste) {
	let htmll = "<option value=\""+liste[0]+"\" >"+liste[0]+"</option>";
	$("#asuka").append(htmll);

	});
	});   
    //on ajoute le bouton valider
    let htmllz = '<input id="nausicaa" type="submit" value="Valider">';
    $("#zzzz").append(htmllz);
});

//on pourrait faire le premier change nous meme en cliquant mais on peux le faire comme ceci.
$('#rei').trigger("change");