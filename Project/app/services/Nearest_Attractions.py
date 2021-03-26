import googlemaps
import pprint
import time

#Get my Key
API_KEY = 'AIzaSyAw3Q7eJyqIazB2ucevU3NhnVmsqs5Z3bQ'

#Define our client
gmaps = googlemaps.Client(key = API_KEY)

#Define our search
places_result = gmaps.places_nearby(location = '1.3817722,103.8964149', radius = 1000, open_now=False, type='restaurant')
# # pprint.pprint(places_result)

# #pause script for 3 seconds
# time.sleep(3)

# #get next 20 results
# places_result = gmaps.places_nearby(page_token = places_result['next_page_token'])

# pprint.pprint(places_result)

#loop through each place in the results
for place in places_result['results']:
    #define my place id
    my_place_id = place['place_id']
    #define the fields we want sent back to us
    my_fields = ['name', 'formatted_phone_number','type']
    #make a request for the details
    place_details = gmaps.place(place_id = my_place_id, fields = my_fields)
    #print the results
    print(place_details)