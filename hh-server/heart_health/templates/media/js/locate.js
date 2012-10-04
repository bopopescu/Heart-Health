// Load the Google Maps API asynchronously

function initialize() {
    var mapOptions = {
      zoom: 8,
      center: new google.maps.LatLng(-34.397, 150.644),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    setLocationIfAvailable(map);
}

function loadScript() {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyDRsF1gfVQH0PkKP4xmg_EFpdV7kya-RfY&sensor=true&callback=initialize";
    document.body.appendChild(script);
}

window.onload = loadScript;

function setLocationIfAvailable(map){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(function(position){
            map.setCenter(new google.maps.LatLng(position.coords.latitude, position.coords.longitude));
        });
    }
}

function searchAddress(){

}

// Pressing the enter key on the input should search the address
$('#address-search').keyup(function(event){
        if(event.keyCode == 13){
            event.preventDefault();
            searchAddress();
            return false;
        }
});

$('#address-search-form').submit(function(){
    return false;
});
