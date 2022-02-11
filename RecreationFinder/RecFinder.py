import requests
import json
from requests.auth import HTTPBasicAuth
import math
from geopy.geocoders import Nominatim
import pandas as pd
from PIL import Image
from io import BytesIO
import random


SENSITIVE_info = json.load(open('./static/SENSITIVE.json', 'r'))
SENSITIVE_info = SENSITIVE_info['nps_api_key']

def get_local_nps_data(SENSITIVE_info, state):
    '''
    Uses NPS API key to query the input state for national parks. 
    ----------
    
    Parameters
    ----------
    SENSITIVE_info : string
        API key.
    state : string
        State abbreviation for NPS API query.

    Returns
    -------
    parks : dict
        All national parks in the query state.
    '''
    endpoint = f"https://{SENSITIVE_info}@developer.nps.gov/api/v1/parks?stateCode=" + state
    headers = {'X-Api-Key': SENSITIVE_info}
    auth = HTTPBasicAuth('apikey', SENSITIVE_info)
    req = requests.get(endpoint, headers=headers, auth=auth)
    parks = json.loads(req.text)
    return parks


def user_distance_to_rec(u_lat, u_lon, rec_lat, rec_lon):
    '''
    Defining function to calculate great circle distance between two coordinates.
    ----------
    
    Parameters
    ----------
    u_lat : float
        Users lattitude.
    u_lon : float
        Users longtitude.
    rec_lat : float
        Recreation/Park lattitude.
    rec_lon : float
        Recreation/Park longitude.

    Returns
    -------
    dist : float
        Distance via haversine formula.
    '''
    # Converting lat/lon to radians
    u_lat_rad = math.radians(u_lat) 
    u_lon_rad = math.radians(u_lon)
    rec_lat_rad = math.radians(rec_lat)
    rec_lon_rad = math.radians(rec_lon)
    # Calculating distance using haversine formula
    dist = 2*math.asin(math.sqrt((math.sin((u_lat_rad-rec_lat_rad)/2))**2+
                                 math.cos(u_lat_rad)*math.cos(rec_lat_rad)*
                                 (math.sin((u_lon_rad-rec_lon_rad)/2))**2)) 
    return dist


def nearest_rec(nps_data, u_lat, u_lon):
    '''
    Finding the nearest recreation given the coordinates of a user
    ----------
    
    Parameters
    ----------
    nps_data : dict
        Output of get_local_nps_data()
        Response from NPS API 
    u_lat : string
        Users lattitude.
        In output from get_user_location()
    u_lon : string
        Users longitude.
        In output from get_user_location()

    Returns
    -------
    park_data : dict
        Contains the name of the closest park and its associated info.
    '''
    # Creating dictionary for storing Name and dist_to_user.
    dist_to_user = {} 
    # Initializing index id.
    index_val = 0
    # Iterating over all stored locations.
    for n in range(len(nps_data['data'])):
        park = nps_data['data'][n]
        rec_lat = float(park['latitude'])
        rec_lon = float(park['longitude'])
        # Finding the distance to the user and saving in dictionary
        dist_to_user[park['fullName']] = user_distance_to_rec(u_lat, 
                                                              u_lon, 
                                                              rec_lat, 
                                                              rec_lon)     
    # Find park with minimal distance.
    closest_park = (min(dist_to_user, key=dist_to_user.get))
    
    # Get the data of the closest park.
    for k in range(len(nps_data['data'])):
        if nps_data['data'][k]['fullName'] == closest_park:
            index_val = k
            
    park_data = {"park":nps_data['data'][index_val], "closest_park":closest_park}

    return park_data 


def get_user_location(address):
    '''
    With a input address, get geolocation data.
    ----------
    
    Parameters
    ----------
    address : string
        A user input address in the US.

    Returns
    -------
    u_location_data : dict
        Geolocation information (lat/lon/state) and state abbreviaton.
    '''
    # Read in list of states and their abbreviations.
    state_codes = pd.read_csv("static/stateFIPS.csv" , header=None)
    try:
        # Get the users location
        u_location = {}
        geolocator = Nominatim(user_agent="RecFinder")
        location = geolocator.geocode(address)
        # Store the users lat/lon
        u_lat = location.latitude
        u_lon = location.longitude
        
        # Get state name/abbrev for NPS query
        str_location = str(location).split(",")
        state_codes = pd.read_csv("static/stateFIPS.csv" , header=None)
        u_state = []
        # Depending on the address, the indexing of the location may vary.
        # Picks the value for state by comparing to list of states
        for i in str_location:
            try:
                for n in range(len(state_codes[0])):
                    if i.split(" ")[1] == state_codes[0][n]:
                        u_state.append(i.split(" ")[1])
            except IndexError:
                pass
            
        # Store location data.    
        u_location = {"u_state":u_state[0],
                      "u_lat":u_lat,
                      "u_lon":u_lon}
        
        # Get abbreviation of the state.
        for state in state_codes[0]:
            if state == u_location['u_state']:

                state_index = state_codes[state_codes[0] == state].index.values
        state_abbrev = str(state_codes[1].iloc[state_index].values).lower()
        state_abbrev = state_abbrev.split("'")[1]


        u_location_data = {"u_location":u_location, "state_abbrev":state_abbrev}    

        return u_location_data
    
    except AttributeError:
        pass
        

def closest_park_data(park_data):
    '''
    Collect and organize information about the closest park for display.
    ----------
    
    Parameters
    ----------
    park_data : dict
        Output of nearest_rec()
        Name of the closest park and its associated info.

    Returns
    -------
    display_data : dict
        Activities, park name/description/images, and directions to the park.
    '''
    
    # Collect featured park activities.
    activities = []
    for k in range(len(park_data['park']['activities'])):
        activities.append(park_data['park']['activities'][k]['name'])
    activities = pd.DataFrame(activities)
    
    # Parks have varied amounts of activities, sometimes less than 5.
    try:
        display_data = {"activities" : activities,
                        "sample_activities" : activities.sample(n=5),
                        "description" : park_data['park']['description'],
                        "directions" : { "text": park_data['park']['directionsInfo'],
                                        "link": park_data['park']['directionsUrl']},
                        "operatingHours" : park_data['park']['operatingHours'],
                        "fees" : park_data['park']['entranceFees'],
                        "park_name" : park_data["closest_park"],
                        "images" : park_data['park']['images']} 
    except ValueError:
        display_data = {"activities" : activities,
                        "sample_activities" : activities,
                        "description" : park_data['park']['description'],
                        "directions" : { "text": park_data['park']['directionsInfo'],
                                        "link": park_data['park']['directionsUrl']},
                        "operatingHours" : park_data['park']['operatingHours'],
                        "fees" : park_data['park']['entranceFees'],
                        "park_name" : park_data["closest_park"],
                        "images" : park_data['park']['images']} 
        
    return display_data


def image_prep(display_data):
    '''
    Grabs and prepares image samples for UI display. 
    ----------
    
    Parameters
    ----------
    display_data : dict
        Data about the closest national park and index for easy access.
        Output of closest_park_data().

    Returns
    -------
    display_data : dict
       Updates input display_data with images ready for UI display.
    '''
    num_images = len(display_data['images'])
    
    # If no images are available for the park.
    if num_images == 0:
        image_set = {"image_0" : f"No images are currently available for {display_data['park_name']}"}
   
    # If the number of images available is less than the desired sample quantity.
    elif num_images < 4:
        image_set = {}
        # Ready image index counter
        j = 0
        # Grabbing all images available.
        for i in range(num_images):
            image_url = display_data['images'][i]['url']
            img_response = requests.get(image_url)
            image_set[f"image_{j}"] = Image.open(BytesIO(img_response.content))
            j += 1
            
    # If enough images available, pick and ready a random 3 images. 
    else:
        random_ind = random.sample(range(num_images), 3)
        image_set = {}
        # Ready image index counter
        j = 0
        # Picking a random 3 images.
        for i in random_ind:
            image_url = display_data['images'][i]['url']
            img_response = requests.get(image_url)
            image_set[f"image_{j}"] = Image.open(BytesIO(img_response.content))
            j += 1
    
    # Storing the images ready for UI display
    display_data['image_set'] = image_set
    
    return display_data


def RecreationFinder(address):
    '''
    Execute to find the name and information about the nearest national park. 
    ----------
    
    Parameters
    ----------
    address : string
        A user input address in the US.

    Returns
    -------
    ui_data : dict
        Data about the closest national park with images ready for UI display.
    '''
    # get location
    u_location_data = get_user_location(address)
    
    try:
        # get nps data
        nps_data = get_local_nps_data(SENSITIVE_info, 
                                      u_location_data['state_abbrev'])
    except TypeError:
        
        return print(f"The address {address} was not accepted. Please reformat and try again.")
    
    # find closest park
    park_data = nearest_rec(nps_data, 
                            u_location_data['u_location']['u_lat'], 
                            u_location_data['u_location']['u_lon'])
   
    # Find and organize info
    display_data = closest_park_data(park_data)
    
    # Image prep for the UI
    ui_data = image_prep(display_data)
    
    
    return ui_data

# Grand county public library in Moab Utah
address = "257 E Center Street Moab UT"

ClosestNationalPark = RecreationFinder(address)
