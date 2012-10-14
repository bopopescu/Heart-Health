// Load the Google Maps API asynchronously
var heartHealthLocateMap;
var infoWindow;
function initialize() {
    var mapOptions = {
      zoom: 4,
      center: new google.maps.LatLng(39.930801,-97.328796),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    heartHealthLocateMap = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    infoWindow = new google.maps.InfoWindow({
        maxWidth: 200
    });
    setLocationIfAvailable();
}

function loadScript() {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyDRsF1gfVQH0PkKP4xmg_EFpdV7kya-RfY&sensor=true&callback=initialize";
    document.body.appendChild(script);
}

window.onload = loadScript;

function setLocationIfAvailable(){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(function(position){
            var currentLatLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            setAndSearchLocation(currentLatLng);

            var geocoder = new google.maps.Geocoder();
            geocoder.geocode({'latLng': currentLatLng}, function(results, status) {
              if (status == google.maps.GeocoderStatus.OK) {
                  if (results[1]) {
                        $('#address-search').val(results[1].formatted_address);
                        $('#search-alert').addClass('hidden');
                  } else {
                        searchError('Unable to find your location. Please try again.');
                  }
              } else {
                  searchError('An unexpected error has occurred. Please try again.');
              }
            });
        }, function(error){
            if(error.code == 1){
                searchError('Permission was denied to find your location.');
            } else {
                searchError('Unable to find your location. Please try again.');
            }
        });
    } else {
        searchError('Your browser doesn\'t support geolocation.');
    }
}

var myLocationMarker;
// Takes a LatLng object and centers the map around it + searches and displays locations
function setAndSearchLocation(latLng){
        heartHealthLocateMap.setCenter(latLng);
        heartHealthLocateMap.setZoom(14);
        if(!myLocationMarker){
            myLocationMarker = new google.maps.Marker({
                    position: latLng,
                    map: heartHealthLocateMap,
                    icon: greenMarkerPath,
                    title: "You are here!"
            });
            myLocationMarker.setAnimation(google.maps.Animation.DROP);
            myLocationMarker.setMap(heartHealthLocateMap);
        } else {
            myLocationMarker.setPosition(latLng);
        }

        retrieveLocations(latLng);
}

// Searches again using the location that the map has already been centered around
function searchNewRadius(){
    retrieveLocations(heartHealthLocateMap.getCenter());
}

// Retrieve locations from the server and display them
function retrieveLocations(latLng){
    resetResults();
    $('#loading-spinner').removeClass('hidden');
    $.ajax({
        url: '/locate/get/',
        type: "GET",
        data: 'lat=' + latLng.lat() + '&lon=' + latLng.lng() + '&radius=' + $('#search-radius-select').val(),
        success: function(data){
            response = JSON.parse(data);
            if(response.providers.length < 1){
                $('#locations-noresults-alert').removeClass('hidden');
            }
            showProviders(response.providers);
            $('#loading-spinner').addClass('hidden');
        },
        error: function(data){
            locationsError('An unexpected error has occurred, please try again.');
            $('#loading-spinner').addClass('hidden');
        },
    });
}

function resetResults(){
    $('#results-container').html('');
    $('#locations-error').addClass('hidden');
    $('#locations-noresults-alert').addClass('hidden');
    for(var i = 0; i < locationMarkers.length; i++){
        locationMarkers[i].setMap(null);
    }
    // Clear the array after removing all markers from the map
    locationMarkers.length = 0;
}

function showProviders(providers){
    var htmlResults = '';
    for(var i = 0; i < providers.length; i++){
        var provider = providers[i];
        htmlResults += '<address id="results-address-' + i + '" class="location"><strong>' + provider.name +
            '</strong><strong style="float: right;">' + provider.distance.toFixed(1) + ' Miles Away' + '</strong><br>' +
            provider.address1 + '<br>';
        if(provider.address2){
            htmlResults += provider.address2 + '<br>';
        }
        var formattedZip = provider.zip.substr(0,5) + '-' + provider.zip.substr(5,4);
        htmlResults += provider.city + ' ' + provider.state + ' ' + formattedZip + '<br>'; 
        if(provider.url){
            htmlResults += '<a href="' + provider.url + '" target="_blank">' + provider.urlCaption + '</a><br>';
        }
        if(provider.phone){
            var formattedPhone = provider.phone.substr(0, 3) + '-' + provider.phone.substr(3, 3) + '-' + provider.phone.substr(6,4)
            htmlResults += formattedPhone + '<br>';
        }
        if(provider.description){
            htmlResults += provider.description + '<br>';
        }
        htmlResults += '</address>';
        addLocationMarker(provider.lat, provider.lon);
    }

    // Show the htmlResults
    $('#results-container').html(htmlResults);
    // Setup on click listeners for clicking an address box
    $('#results-container').children().each(function (){
        $(this).click(function (){
            removeSelectedLocation();
            $(this).addClass('selected-location');
            google.maps.event.trigger(locationMarkers[$(this).index()], 'click');
        });
    });
    zoomToFitMarkers();
}

var locationMarkers = new Array();
function addLocationMarker(lat,lng){
    var latLng = new google.maps.LatLng(lat,lng);
    newMarker = new google.maps.Marker({
            position: latLng,
            map: heartHealthLocateMap,
    });
    newMarker.setAnimation(google.maps.Animation.DROP);
    var markerNumber = locationMarkers.length;
    google.maps.event.addListener(newMarker, 'click', function(){
        removeSelectedLocation();
        infoWindow.close();
        $('#results-address-' + markerNumber).addClass('selected-location');
        infoWindow.setContent($('#results-address-' + markerNumber).html());
        infoWindow.open(heartHealthLocateMap, this);
    });
    newMarker.setMap(heartHealthLocateMap);
    locationMarkers.push(newMarker);
}

function removeSelectedLocation(){
    $('#results-container').children().each(function (){
        $(this).removeClass('selected-location');
    });
}

function zoomToFitMarkers(){
    // If there aren't any location markers, don't do this step
    if(locationMarkers.length == 0){
        return;
    }
    //  Create a new viewpoint bound
    var bounds = new google.maps.LatLngBounds();
    //  Go through each...
    for (var i = 0; i < locationMarkers.length; i++) {
        // Increase the bounds to take this point
        bounds.extend(locationMarkers[i].getPosition());
    }
    bounds.extend(myLocationMarker.getPosition())
    //  Fit these bounds to the map
    heartHealthLocateMap.fitBounds(bounds);
}

function searchAddress(){
    resetResults();
    $('#loading-spinner').removeClass('hidden');
    var address = $('#address-search').val();
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': address}, function(results, status) {
          if (status == google.maps.GeocoderStatus.OK) {
              if(results[0]){
                 setAndSearchLocation(results[0].geometry.location);
                 $('#search-alert').addClass('hidden');
              } else {
                  searchError('An unexpected error has occurred. Please try again.');
                  $('#loading-spinner').addClass('hidden');
              }
          } else if (status == google.maps.GeocoderStatus.ZERO_RESULTS) {
              searchError('No location was found for the address you entered.');
              $('#loading-spinner').addClass('hidden');
          } else {
              searchError('An unexpected error has occurred. Please try again.');
              $('#loading-spinner').addClass('hidden');
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

function searchError(message){
    $('#search-alert-text').text(message);
    $('#search-alert').removeClass('hidden');
}

function locationsError(message){
    $('#locations-error-text').text(message);
    $('#locations-error').removeClass('hidden');
}

$('#address-search-form').submit(function(){
    return false;
});
