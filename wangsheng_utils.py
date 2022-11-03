from math import radians, cos, sin, asin, sqrt
import requests

def haversine(lat1, long1, lat2, long2):
    """
    Code Ref.: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    # haversine formula 
    dlon = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

def find_lat_lng(address):
    req = requests.get('https://developers.onemap.sg/commonapi/search?searchVal='+address+'&returnGeom=Y&getAddrDetails=Y&pageNum=1')
    resultsdict = eval(req.text)
    if len(resultsdict['results'])>0:
        return resultsdict['results'][0]['LATITUDE'], resultsdict['results'][0]['LONGITUDE']
    else:
        return None, None


# find the nmber of nearest infrastructure to our property listing
# km is the maximum distance we want to calculate from. 
# calculate the number of infrastructure within x km
def count_nearest(lat, long, infrastructure, km):
    distances = infrastructure.apply(
        lambda row: haversine(lat, long, row['lat'], row['lng']), 
        axis=1)
    
    return sum(i <= km for i in distances)


# find the distance of the nearest infrastructure to our property listing
def find_nearest_distance(lat, long, infrastructure):
    distances = infrastructure.apply(
        lambda row: haversine(lat, long, row['lat'], row['lng']), 
        axis=1)
    return distances.min()


# get the population of the subzone the listing is in
def find_subzone_population(subzone, subzones_df):
    sz = subzones_df
    if subzone == "":
        sz_pop = None
    else:
        sz_pop = sz.loc[sz['name'] == subzone, 'population'].item()
    return sz_pop

# get the population density of the subzone the listing is in
def find_subzone_population_density(subzone, subzones_df):
    sz = subzones_df
    if subzone == "":
        sz_pop_density = None
    else:
        sz_pop_density = sz.loc[sz['name'] == subzone, 'population'].item()/sz.loc[sz['name'] == subzone, 'area_size'].item()
    return sz_pop_density