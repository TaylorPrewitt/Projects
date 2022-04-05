import requests
import json
import time
import pandas as pd


SENSITIVE_info = json.load(open('./static/SENSITIVE.json', 'r'))
SENSITIVE_info = SENSITIVE_info['pubg_api_key']


root_url = "https://api.pubg.com/"
endpoint = "tournaments"
auth = SENSITIVE_info


def get_data(root_url, endpoint, auth):
    '''
    Grabs basic data for a given root_url, endpoint, and authorization.

    Parameters
    ----------
    root_url : string
        Root url for the API to be queried. 
    endpoint : string
        Specific endpoint at the API which hosts the data.
    auth : string
        API key.

    Returns
    -------
    dict
        API endpoint response.

    '''
    # Ensuring format of the root url
    if root_url[-1] != '/':
        root_url = f"{root_url}/"
        
    # Creating full query url
    url = f"{root_url}{endpoint}"
    # Auth header
    header = {"Authorization": f"Bearer {auth}",
              "Accept": "application/vnd.api+json"}
    
    # Making API request.
    req = requests.get(url, headers=header)
    
    return json.loads(req.text)


    
def get_ids(root_url, endpoint, auth):
    '''
    Collects ID's of all data entries at the input endpoint.

    Parameters
    ----------
    root_url : string
        Root url for the API to be queried. 
    endpoint : string
        Specific endpoint at the API which hosts the data.
    auth : string
        API key.

    Returns
    -------
    id_list : list
        All ID's returned from the endpoint.

    '''
    # Execute function to get data
    id_dict = get_data(root_url, endpoint, auth)
    # 
    id_list = [id_dict['data'][n]['id'] for n in range(0, len(id_dict['data']))]
       
    return id_list


def hash_ids(id_list, block_s):
    '''
    Split list up into chunks.

    Parameters
    ----------
    id_list : list
        Data to be split into chunks.
    block_s : int
        Block size. Number of entries per block. The API request rate limit.
        

    Returns
    -------
    block_list : list
        Each row is a list of ID's of length=block_s.
        Total length of block_list is id_list/block_s

    '''
    block_list = [id_list[n:n+block_s] for n in range(0, len(id_list), block_s)]
    return block_list


def get_throttled_data(root_url, endpoint, block_list, auth, max_n=0, rl=60):
    '''
    Queries an API endpoint with a set request rate.

    Parameters
    ----------
    root_url : string
        Root url for the API to be queried. 
    endpoint : string
        Specific endpoint at the API which hosts the data.
    block_list : list
        Each entry is a list if ID's of length=block_s.
        Total length of block_list is id_list/block_s
    auth : string
        API key.
    max_n : int, optional
        Maximum number of blocks to parse. 
        The default is 0.
    rl : int, optional
        Rate limit of API response. 
        The default is 60.

    Returns
    -------
    tournament_data : list
        Data for all tested endpoint-ID combinations.

    '''
    time.sleep(rl)
    
    if max_n == 0:
        max_n = len(block_list)
        
        
    tournament_data = []
    for i in block_list[0:max_n]:
        for n in i:
            data_endpoint = f"{endpoint}/{n}"
            data = get_data(root_url, data_endpoint, auth)
            tournament_data.append(data)
        time.sleep(rl)
        
    return tournament_data       
        

def get_match_ids(tournament_data, block_s):
    '''
    Collects and partitions match IDs for followup API query.

    Parameters
    ----------
    tournament_data : list
        Data for all tested endpoint-ID combinations.
    block_s : int
        Block size. Number of entries per block. The API request rate limit

    Returns
    -------
    block_matches : list
        Partitioned match ID's for tournaments.
        Each row is a list of ID's of length=block_s.
        Total length of block_list is id_list/block_s

    '''    
    matches = []
    for k in range(len(tournament_data)):    
        tourn_k = tournament_data[k]['data']['relationships']['matches']['data']
        for i in range(len(tourn_k)):
            match_id = tourn_k[i]['id']
            matches.append(match_id)
    block_matches = hash_ids(matches, block_s)
    return block_matches


def get_detailed_match_data(root_url, endpoint, block_list, auth, max_n=0):
    '''
    Collects details from a API url and a given endpoint. Partitions data.
    No rate limit consideration. 

    Parameters
    ----------
    root_url : string
        Root url for the API to be queried. 
    endpoint : string
        Specific endpoint at the API which hosts the data.
    block_list : list
        Each row is a list of ID's of length=block_s.
        Total length of block_list is id_list/block_s
    auth : string
        API key. 
    max_n : int, optional
        Maximum number of blocks to parse. 
        The default is 0.

    Returns
    -------
    match_data : list
        API endpoint response. 

    '''
    root_url = f"{root_url}shards/tournament"
    
    if max_n == 0:
        max_n = len(block_list)
        
        
    match_data = []
    for i in block_list[0:max_n]:
        for n in i:
            data_endpoint = f"{endpoint}/{n}"
            data = get_data(root_url, data_endpoint, auth)
            match_data.append(data)
        
    return match_data 



def get_participant_perf(match_details):
    '''
    Given match details, collects each players peformance over various metrics.

    Parameters
    ----------
    match_details : list
        Output of get_detailed_match_data().

    Returns
    -------
    player_data : list
        Observations of player/team stats/ids per game played.

    '''
    player_data = []
    for i in range(len(match_details)):
        for j in range(len(match_details[i]['included'])):  
            player_stats = {'match_id':match_details[i]['data']['id'],
                            'participant_id':match_details[i]['included'][j]['id'],
                            'participant_stats':match_details[i]['included'][j]['attributes']}
            player_data.append(player_stats)
    
    return player_data


def collect_tourn_player_data(root_url, auth, block_s, max_n=0, rl=60):
    '''
    Executes:
        get_ids()
        hash_ids()
        get_throttled_data()
        get_match_ids()
        get_detailed_match_data()
        get_participant_perf()

    Parameters
    ----------
    root_url : string
        Root url for the API to be queried. 
    auth : string
        API key.
    block_s : int
        Block size. Number of entries per block. The API request rate limit
    max_n : int, optional
        Maximum number of blocks to parse. 
        The default is 0.
    rl : int, optional
        Rate limit of API response. 
        The default is 60.


    Returns
    -------
    player_data : list
        Observations of player/team stats/ids per game played.

    '''
    id_list = get_ids(root_url,"tournaments", auth)
    block_list = hash_ids(id_list, block_s)
    tournament_data = get_throttled_data(root_url,"tournaments", 
                                         block_list, auth, max_n, rl)
    block_matches = get_match_ids(tournament_data, block_s)
    match_details = get_detailed_match_data(root_url,
                                            "matches", 
                                            block_matches, 
                                            auth)
    player_data = get_participant_perf(match_details)
    
    return player_data



def collect_player_stats(root_url, auth, block_s, max_n=0, rl=60):
    '''
    Executes collect_tourn_player_data().
    Then filters for any rows which are not individual player stats, some rows
    are team/outcome stats which did not have the same keys as the target data. 
    

    Parameters
    ----------
    root_url : string
        Root url for the API to be queried. 
    auth : string
        API key.
    block_s : int
        Block size. Number of entries per block. The API request rate limit
    max_n : int, optional
        Maximum number of blocks to parse. 
        The default is 0.
    rl : int, optional
        Rate limit of API response. 
        The default is 60.

    Returns
    -------
    player_stats : list
        Observations of individual player stats/ids per game played.

    '''
    # Run 
    player_data = collect_tourn_player_data(root_url, auth, block_s, max_n, rl)
    
    # Get only Individual player stats
    player_stats = []
    for n in range(len(player_data)):
        try:
            # Individual player stat lists have 23 keys, and others do not. 
            if len(player_data[n]['participant_stats']['stats']) == 23:
                player_stats.append(player_data[n]['participant_stats']['stats'])
        except KeyError:
            # Some rows of player_data[n] do not have 'stats' key. 
            # Avoids error being thrown and ignores. 
            pass
    return player_stats



player_stats = collect_player_stats(root_url, auth, block_s=10,max_n=1, rl=60)

player_stats_df = pd.DataFrame(player_stats)
player_stats_df.to_csv("pubg_stats.csv")
