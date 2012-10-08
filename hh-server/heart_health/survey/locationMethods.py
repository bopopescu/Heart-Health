import urllib
import urllib2
import simplejson as json

SURESCRIPTS_API_KEY = "3a0a572b-4f5d-47a2-9a75-819888576454"
SURESCRIPTS_URL = "https://millionhearts.surescripts.net/test/Provider/Find"

def getScreeningLocations(latitude, longitude, radius):
    params = {'apikey': SURESCRIPTS_API_KEY, 'lat': latitude, 'lon': longitude, 'radius': radius}
    encoded_args = urllib.urlencode(params)
    response = json.loads(urllib2.urlopen(SURESCRIPTS_URL, encoded_args).read())
    return response['providers']
