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
                        currentAddress = results[1].formatted_address;
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
function searchNewRadiusNoLocations(){
    $('#search-radius-select-normal').val($('#search-radius-select').val()); 
    retrieveLocations(heartHealthLocateMap.getCenter());
}

function searchNewRadiusNormal(){
    $('#search-radius-select').val($('#search-radius-select-normal').val()); 
    retrieveLocations(heartHealthLocateMap.getCenter());
}

// a variable to hold all the current providers
var currentProviders = new Array();
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
            currentProviders = response.providers;
            if(response.providers.length < 1){
                $('#locations-noresults-alert').removeClass('hidden');
                $('#locations-newradius').addClass('hidden');
            } else {
                $('#locations-newradius').removeClass('hidden');
            }
            showProviders(response.providers);
            $('#loading-spinner').addClass('hidden');
        },
        error: function(data){
            locationsError('An unexpected error has occurred, please try again.');
            $('#loading-spinner').addClass('hidden');
            $('#locations-noresults-alert').addClass('hidden');
            $('#locations-newradius').addClass('hidden');
        },
    });
}

function resetResults(){
    $('#results-container').html('');
    $('#locations-error').addClass('hidden');
    $('#locations-noresults-alert').addClass('hidden');
    $('#locations-newradius').addClass('hidden');
    for(var i = 0; i < locationMarkers.length; i++){
        locationMarkers[i].setMap(null);
    }
    // Clear the array after removing all markers from the map
    locationMarkers.length = 0;
    // Clear the preferred button
    preferredProviderIdx = -1;
}

// A global variable to store the preferred provider index when chosen
var preferredProviderIdx = -1;
function showProviders(providers){
    var htmlResults = '';
    for(var i = 0; i < providers.length; i++){
        var provider = providers[i];
        htmlResults += getContentForProvider(provider, true, true, true, i);
        addLocationMarker(provider.lat, provider.lon);
    }

    // Show the htmlResults
    $('#results-container').html(htmlResults);
    // Setup on click listeners for clicking an address box
    $('#results-container').children().each(function (){
        $(this).addClass('location');
        var currentProviderIdx = $(this).index();
        $(this).click(function (){
            removeSelectedLocation();
            $(this).addClass('selected-location');
            google.maps.event.trigger(locationMarkers[currentProviderIdx], 'click');
        });
        $(this).find('button').click(function(evt) {
            var provider = currentProviders[currentProviderIdx];
            preferredProvider = provider;
            preferredProviderIdx = currentProviderIdx;
            $('#choose-modal-address').html(getContentForProvider(provider, true, true, false, -1));
            var sAddrEncoded = encodeURIComponent(currentAddress);
            var address2 = ''; 
            if(provider.address2) { address2 = provider.address2 + ' '; }
            var dAddrEncoded = encodeURIComponent(provider.address1 + ' ' + address2 + ' ' + provider.city + ' ' +  provider.state + ' ' + provider.zip)
            var directionsUrl = 'http://maps.google.com/maps?saddr=' + sAddrEncoded + '&' + 'daddr=' + dAddrEncoded;
            $('#directions-button').attr('href', directionsUrl);
            $('#chooseModal').modal('show');
        });
    });
    zoomToFitMarkers();
    markPreferredLocation();
}

function markPreferredLocation(){
    for(var i = 0; i < currentProviders.length; i++){
        var provider = currentProviders[i];
        if(preferredProvider.name == provider.name && preferredProvider.address1 == provider.address1 && preferredProvider.address2 == provider.address2 && preferredProvider.city == provider.city && preferredProvider.state == provider.state && preferredProvider.zip == provider.zip){
            preferredProviderIdx = i;
        }
    }

    if(preferredProviderIdx == -1){
        return;
    }
    $('#results-container').children().each(function(){
        $(this).find('button').removeAttr('disabled');
    });
    var addressElement = $('#results-container').children()[preferredProviderIdx]
    $(addressElement).find('button').attr('disabled', 'disabled');
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
        infoWindow.setContent(getContentForProvider(currentProviders[markerNumber], false, false, false, -1));
        infoWindow.open(heartHealthLocateMap, this);
    });
    newMarker.setMap(heartHealthLocateMap);
    locationMarkers.push(newMarker);
}

function savePreferredLocation(){
    $('#btn-save-preferred').button('loading');
    $('#preferred-save-error').addClass('hidden');
    $.ajax({
        url: '/locate/savepreferred/',
        type: "POST",
        data: preferredProvider,
        dataType: "json",
        success: function(data){
            if(data.success){
                $('#btn-save-preferred').button('reset');
                $('#chooseModal').modal('hide');
                markPreferredLocation();
            } else {
                $('#btn-save-preferred').button('reset');
                $('#preferred-save-error').removeClass('hidden');
            }
        },
        error: function(data){
            $('#btn-save-preferred').button('reset');
            $('#preferred-save-error').removeClass('hidden');
        },
    });
}

// Returns an html string with some basic info about a provider, formatted in an <address>
// This function will not inclue the description if you pass false in for includeDescription
// If floatDistance is true, the distance info will be floated right
// If includeButton is true, a select location button will be added as well
// resultNumber is the number in the list of results that this provider is. Pass -1 if this 
// is not being used to generate results for the main list.
function getContentForProvider(provider, includeDescription, floatDistance, includeButton, resultNumber){
        var htmlResult = '';
        htmlResult += '<address id="results-address-' + resultNumber + '"><strong>' + provider.name + '</strong>';
        if(floatDistance){
            htmlResult += '<strong style="float: right;"';
        } else {
            htmlResult += '<br><strong';
        }
        htmlResult += '>' + provider.distance.toFixed(1) + ' Miles Away' + '</strong><br>' +
        provider.address1 + '<br>';
        if(provider.address2){
            htmlResult += provider.address2 + '<br>';
        }
        var formattedZip = provider.zip.substr(0,5);
        htmlResult += provider.city + ' ' + provider.state + ' ' + formattedZip + '<br>'; 
        if(provider.phone){
            var formattedPhone = '(' + provider.phone.substr(0, 3) + ')' + '-' + provider.phone.substr(3, 3) + '-' + provider.phone.substr(6,4)
            htmlResult += formattedPhone + '<br>';
        }
        if(provider.url){
            htmlResult += '<a href="' + provider.url + '" target="_blank">' + provider.urlCaption + '</a>';
        }
        if(includeDescription && provider.description){
            htmlResult += '<br>' + provider.description + '<br>';
        }
        if(includeButton){
            htmlResult += '<button class="btn btn-danger">Set As My Preferred Location</button>';
        }
        htmlResult += '</address>';
        return htmlResult;
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

// A global variable to store the current address
var currentAddress = '';
function searchAddress(){
    resetResults();
    $('#loading-spinner').removeClass('hidden');
    var address = $('#address-search').val();
    currentAddress = address;
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
