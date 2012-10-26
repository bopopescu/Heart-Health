from django.core.management.base import BaseCommand, CommandError
from geopy import geocoders
import simplejson as json
from survey.models import Location
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    This command (addLocations) takes in a single argument, the filename of the json file to add.
    This will go through the array of providers in the json array and add them to location objects that will be committed to the DB
    with the flag 'is_result' set to true. All of these locations will be included in the results given in /locate/.
    """

    def handle(self, *args, **options):
        addLocationsToDB(args[0])

def addLocationsToDB(filename):
    json_data = open(filename).read()
    data = json.loads(json_data)
    
    providers = data['providers']
    
    for provider in providers:
        if provider['address2']:
            address2_string = provider['address2']
        else:
            address2_string = ''

        try:
            location = Location.objects.get(name=provider['name'], address1=provider['address1'], address2=address2_string, city=provider['city'], state=provider['state'], zip_code=provider['zip']) 
        except Location.DoesNotExist:
            location = Location()

        location.name = provider['name']
        location.address1 = provider['address1']
        if provider['address2']:
            location.address2 = provider['address2']
        location.city = provider['city']
        location.state = provider['state']
        location.zip_code = provider['zip']
        if provider['crossStreet']:
            location.cross_street = provider['crossStreet']
        location.phone = provider['phone']
        location.url = provider['url']
        if provider['urlCaption']:
            location.url_caption = provider['urlCaption']
        if provider['description']:
            location.description = provider['description']
        location.is_result = True 

        if not ('lat' in provider and 'lon' in provider):
            geocoder =  geocoders.Google()
            provider_loc_string = provider['address1'] + ' '
            if provider['address2']:
                provider_loc_string += provider['address2'] + ' '
            provider_loc_string += provider['city'] + ' ' + provider['zip']
            try:
                place, (lat, lng) = geocoder.geocode(provider_loc_string)
                location.latitude = lat
                location.longitude = lng
            except Exception as exception:
                logger.error('Location: ' + location.name + ' failed to be geocoded. Skipping this location. Error is: ' + str(exception))
                continue
        else:
            location.latitude = provider['lat']
            location.longitude = provider['lon']

        location.save()

