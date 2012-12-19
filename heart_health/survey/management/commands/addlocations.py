from django.core.management.base import BaseCommand, CommandError
from geopy import geocoders
import simplejson as json
from survey.models import Location
import csv
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    This command (addLocations) takes in a single argument, the filename of the json file to add.
    This will go through the array of providers in the json array and add them to location objects that will be committed to the DB
    with the flag 'is_result' set to true. All of these locations will be included in the results given in /locate/.
    """

    def handle(self, *args, **options):
        if args[0] == 'json':
            addLocationsToDB_json(args[1])
        if args[0] == 'csv':
            add_locations_to_db_csv(args[1])
        if args[0] == 'delete':
            delete_saved_locations()

def delete_saved_locations():
    Location.objects.all().delete()

def addLocationsToDB_json(filename):
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

def add_locations_to_db_csv(filename):
    with open(filename, 'rb') as locations_file:
        csv_reader = csv.reader(locations_file)
        
        is_first_row = True 
        for provider in csv_reader:
            if is_first_row:
                is_first_row = False
                continue

            if provider[2]:
                address2_string = str(provider[2])
            else:
                address2_string = ''

            try:
                location = Location.objects.get(name=str(provider[0]), address1=str(provider[1]), address2=address2_string, city=str(provider[3]), state=str(provider[4]), zip_code=str(provider[5])) 
            except Location.DoesNotExist:
                location = Location()

            location.name = str(provider[0])
            location.address1 = str(provider[1])
            if provider[2]:
                location.address2 = str(provider[2])
            location.city = str(provider[3])
            location.state = str(provider[4])
            location.zip_code = str(provider[5])
            if provider[6]:
                location.cross_street = str(provider[6])
            location.phone = str(provider[9])
            location.url = str(provider[7])
            if provider[8]:
                location.url_caption = str(provider[8])
            if provider[10]:
                location.description = str(provider[10])
            location.is_result = True 

            if not provider[11] or not provider[12]:
                geocoder =  geocoders.Google()
                provider_loc_string = str(provider[1]) + ' '
                if provider[2]:
                    provider_loc_string += str(provider[2]) + ' '
                provider_loc_string += str(provider[3]) + ' ' + str(provider[5])
                try:
                    place, (lat, lng) = geocoder.geocode(provider_loc_string)
                    location.latitude = lat
                    location.longitude = lng
                except Exception as exception:
                    logger.error('Location: ' + location.name + ' failed to be geocoded. Skipping this location. Error is: ' + str(exception))
                    continue
            else:
                location.latitude = float(provider[11])
                location.longitude = float(provider[12])

            print "adding " + location.name + location.city + location.zip_code
            location.save()

