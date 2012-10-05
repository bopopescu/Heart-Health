// Load the Google Maps API asynchronously
var map;
function initialize() {
    var mapOptions = {
      zoom: 4,
      center: new google.maps.LatLng(39.930801,-97.328796),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
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
            var currentLatLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            setAndSearchLocation(currentLatLng);

            var geocoder = new google.maps.Geocoder();
            geocoder.geocode({'latLng': latLng}, function(results, status) {
              if (status == google.maps.GeocoderStatus.OK) {
                  if (results[1]) {
                        $('#address-search').val(results[1].formatted_address);
                  }
              }
            });
        });
    }
}

// Takes a LatLng object and centers the map around it + searches and displays locations
function setAndSearchLocation(latLng){
        map.setCenter(latLng);
        map.setZoom(14);
        var marker = new google.maps.Marker({
                position: latLng,
                map: map,
                icon: greenMarkerPath,
                title: "You are here!"
        });
        marker.setMap(map);

        
    
}

function searchAddress(){
    var address = $('#address-search').val();
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': address}, function(results, status) {
          if (status == google.maps.GeocoderStatus.OK) {
              if(results[0]){
                 setAndSearchLocation(results[0].geometry.location);
              }
          }
    });
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
