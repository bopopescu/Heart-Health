import urllib
import urllib2
import simplejson as json
from survey.models import Location

SURESCRIPTS_API_KEY = "3a0a572b-4f5d-47a2-9a75-819888576454"
SURESCRIPTS_URL = "https://millionhearts.surescripts.net/test/Provider/Find"

def getScreeningLocations(latitude, longitude, radius):
    params = {'apikey': SURESCRIPTS_API_KEY, 'lat': latitude, 'lon': longitude, 'radius': radius}
    encoded_args = urllib.urlencode(params)
    response = json.loads(urllib2.urlopen(SURESCRIPTS_URL, encoded_args).read())

    #local_locations = Location.objects.raw(string.format("SELECT *, ( 3959 * acos( cos( radians(%f) ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians(%f) ) + sin( radians(%f) ) * sin( radians( lat ) ) ) ) AS distance FROM markers HAVING distance < %f ORDER BY distance LIMIT 0 , 10;", latitude, longitude, latitude, highest_radius))

    return response['providers']
