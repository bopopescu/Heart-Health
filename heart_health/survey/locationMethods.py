import urllib
import urllib2
import simplejson as json
import string
import logging
from survey.models import Location

SURESCRIPTS_API_KEY = "3a0a572b-4f5d-47a2-9a75-819888576454"
SURESCRIPTS_URL = "https://millionhearts.surescripts.net/test/Provider/Find"
logger = logging.getLogger(__name__)

def getScreeningLocations(latitude, longitude, radius):
    """
    Finds all screening locations within the given radius from the given lat and long, combining results from both the Surescripts API with
    the locations stored in the application database (that have been imported from flat files)
    """
    params = {'apikey': SURESCRIPTS_API_KEY, 'lat': latitude, 'lon': longitude, 'radius': radius}
    encoded_args = urllib.urlencode(params)
    response = json.loads(urllib2.urlopen(SURESCRIPTS_URL, encoded_args).read())
    providers = response['providers']
        
    if len(response['errors']) > 1:
         logger.error('Error while getting surescripts results: ' + json.dumps(response['errors'])) 

    # Find the highest radius in the results returned by SureScripts
    highest_radius = 0
    for provider in providers:
        if provider['distance'] > highest_radius:
            highest_radius = provider['distance']
    if highest_radius == 0:
        highest_radius = radius

    # Find all locations in the local db that are within the radius
    local_locations = Location.objects.raw("SELECT *, ( 3959 * acos( cos( radians(%s) ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians(%s) ) + sin( radians(%s) ) * sin( radians( latitude ) ) ) ) AS distance FROM survey_location WHERE is_result IS TRUE HAVING distance < %s ORDER BY distance LIMIT 0 , 10;", [latitude, longitude, latitude, highest_radius])

    for location in local_locations:
        providers.append(location_to_provider_dict(location)) 

    providers.sort(key=get_distance)
    return providers[0:10]

def get_distance(provider):
    """
    For a provider dictionary, return the distance
    """
    return provider['distance']

def location_to_provider_dict(location):
   """
   For a location model object instance,
   create a provider dictionary that contains the same information
   """
   provider = {}
   provider['lat'] = location.latitude
   provider['lon'] = location.longitude
   provider['name'] = location.name
   provider['address1'] = location.address1
   provider['address2'] = location.address2
   provider['city'] = location.city
   provider['state'] = location.state
   provider['zip'] = location.zip_code
   provider['phone'] = location.phone
   provider['url'] = location.url
   provider['urlCaption'] = location.url_caption
   provider['crossStreet'] = location.cross_street
   provider['description'] = location.description
   provider['distance'] = location.distance
   return provider 

def get_and_save_location_from_provider_dict(provider):
    address2_string = ''
    if provider['address2']:
       address2_string = provider['address2']
    try:
        location = Location.objects.get(name=provider['name'], address1=provider['address1'], address2=address2_string, city=provider['city'], state=provider['state'], zip_code=provider['zip']) 
    except Location.DoesNotExist:
        location = Location()

    location.latitude = provider['lat']
    location.longitude = provider['lon']
    location.name = provider['name']
    location.address1 = provider['address1']
    location.address2 = provider['address2']
    location.city = provider['city']
    location.state = provider['state']
    location.zip_code = provider['zip']
    location.phone = provider['phone']
    location.url = provider['url']
    location.url_caption = provider['urlCaption']
    location.cross_street = provider['crossStreet']
    location.description = provider['description']

    location.save()
    return location

