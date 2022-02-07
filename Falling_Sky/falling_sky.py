import requests
import json
from datetime import datetime, timedelta
import math as math


SENSITIVE_info = json.load(open('./static/SENSITIVE.json', 'r'))
SENSITIVE_info = SENSITIVE_info['nasa_api_key']


def make_stop_date(START_DATE):
    '''
    Takes in a starting date and outputs an end date.
    The end date is one week after the input START_DATE.

    START_DATE: string
       Date for query term. Format: %Y-%m-%d. First day of the window. 

    return: string
       Date as a string 7 days after the starting date.    
    '''

    START_DATE = datetime.strptime(START_DATE,"%Y-%m-%d")
    END_DATE = START_DATE + timedelta(days=7)
    END_DATE = datetime.strftime(END_DATE, "%Y-%m-%d")

    return END_DATE



def get_neo_data(START_DATE):
    '''
    Takes in a date to make a week query for NEO via NASA.
    Provides data for all NEO in in the query window. 

    START_DATE: string
        Date as a string. Format: %Y-%m-%d.

    return: dict
       All near_earth_objects from NASA database.    
    '''
    END_DATE = make_stop_date(START_DATE)
    endpoint = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={START_DATE}&end_date={END_DATE}&api_key={SENSITIVE_info}"
    req = requests.get(endpoint)
    all_neo = json.loads(req.text)
    return all_neo['near_earth_objects']


def get_all_hazards(all_neo):
    '''
    Takes output of get_neo_data(). All NEO dict.
    Reads and restructures data.
    Filters on if the NEO is a potential danger to Earth 

    all_neo: dict
        All near_earth_objects from NASA database.

    return: dict
        All potentially hazardous near_earth_objects with data.    

        obj_id: unique ID of object
        obj_l: clearance from earth of object
        obj_d: list of min and max diameters
        obj_v: velocity
        obj_name: name of the object
        chron: date of closest approach. 
    
    '''

    obj = [] # object ID
    for day in all_neo.keys():
        if all_neo[day][0]['is_potentially_hazardous_asteroid'] == True:
            obj.append({"obj_id": all_neo[day][0]['neo_reference_id'],
                            "obj_l" : all_neo[day][0]['close_approach_data'][0]['miss_distance'] ,
                            "obj_d" : all_neo[day][0]['estimated_diameter'],
                            "obj_v" : all_neo[day][0]['close_approach_data'][0]['relative_velocity'],

                            'chron' : day,
                            "obj_name" : all_neo[day][0]['name']
                            })

    return obj



def call_danger(all_hazards):
    '''
    Takes in output of get_all_hazards().
    Calls data for NEO with min clearance distance.

    all_hazards: dict
        All near_earth_objects from NASA database.

    return: dict
        All potentially hazardous near_earth_objects with data.    

        obj_id: unique ID of object
        obj_l: list of object clearance from earth, multi metric.
        obj_d: list of min and max diameters, multi metric.
        obj_v: list of relative velocity, multi metric.
        obj_name: name of the object
        chron: date of closest approach. 
    
    '''

    min_val = all_hazards[0]['obj_l']['kilometers']
    min_index = 0
    for n in range(1, len(all_hazards)):
        if all_hazards[n]['obj_l']['kilometers'] < min_val:
            min_val = all_hazards[n]['obj_l']['kilometers']
            min_index = n
    most_dangerous = all_hazards[min_index]

    return most_dangerous


def get_size(min_d, max_d):
    '''
    A, B, and C are the semiaxes of the assumed ellipsoid

    A : string
        max_d (max diameter of object).
    B : string
        min_d (min diameter of object).

    C = unknown semiaxis. Approximated as mean known semiaxes.

    return: float
       Volume of the object.    
    '''

    A = max_d/2
    B = min_d/2
    C = (A + B)/2

    volume = math.pi*(4/3)*A*B*C

    return volume


def calc_info(A, B, v):
    '''
    A : string
        max semiaxis in kilometers
    B : string
        min semiaxis in kilometers
    v : string
        velocity in kilometers per second

    return: dict
       Physical information and calculations about the NEO.    
    '''

    # get volume/surface area of obj
    min_axis_m = float(B)*1000
    max_axis_m = float(A)*1000
    volume = get_size(min_axis_m, max_axis_m)
    
    # C-class density in kg/m^3
    density = 1700

    # find mass in kg
    mass = volume*density 

    # find kinetic force 1/2(mv^2)
    velocity_ms = float(v)*1000
    kinetic_force = 0.5*mass*(velocity_ms**2)

    # Megaton tnt
    Megaton_TNT_joules = 4.184e+15
    impact_in_MTNT = kinetic_force/(Megaton_TNT_joules)

    obj_data = {"volume" : volume,
            "mass" : mass,
            "kinetic_force" : kinetic_force,
            "v": velocity_ms,
            "impact_in_MTNT" : impact_in_MTNT}

    return obj_data



def dont_look_up(date):
    '''
    date : string
        Starting date for 7 day query.
        format ex: '2022-05-03'  == May 3 2022
    
    return : dict
        Data for the NEO that is closest to earth during the window.
        Size, speed, impact force.

    '''
    # getting all NEO in query windwo
    all_neo = get_neo_data(date)
    # keeping only potentially hazardous NEO 
    all_hazards = get_all_hazards(all_neo)
    # selecting the most dangerous NEO
    biggest_danger = call_danger(all_hazards)

    # extracting data for calculations
    A = biggest_danger['obj_d']['kilometers']['estimated_diameter_max']
    B = biggest_danger['obj_d']['kilometers']['estimated_diameter_min']
    v = biggest_danger['obj_v']['kilometers_per_second']


    # getting NEO information
    data = calc_info(A, B, v)

    # link to NASA for further info about NEO
    id = biggest_danger['obj_id']
    data["link"] = f"https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr={id}"
    
    print()
    print(f"During the week of {date} to {make_stop_date(date)} the biggest NEO danger is on {biggest_danger['chron']}.")
    print(f"This NEO has the impact energy of {round(data['impact_in_MTNT'],2)} megatons of TNT.")
    print(f"This NEO impact would be the same as {round(data['impact_in_MTNT']/(25/1000),2)} of the nulcear bombs dropped on Nagasaki.")
    print(f"This NEO impact would be equivalent to {round(data['kinetic_force']/794328234724281502, 2)} simultaneous 9.0 Earthquakes.")
    print(f"This NEO impact has the same energy as {round(data['kinetic_force']/1000000000000000000, 2)} billion lightning bolts.")
    print(f"Get more information on this NEO at {data['link']}")
    print()

    return data



doom_of_week = dont_look_up('2022-05-05')



