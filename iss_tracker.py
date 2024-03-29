from flask import Flask, request
from geopy.geocoders import Nominatim
import requests 
import xmltodict
import math
import time

app = Flask(__name__)

url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
response = requests.get(url)

global data 
data = xmltodict.parse(response.text)

geocoder = Nominatim(user_agent='iss_tracker')

@app.route('/', methods=['GET'])
def dataset() -> dict:
    """
    This function returns all of the data from the XML file.
    Args:
    This function does not have a set parameter, but the app route can be called 
    with '/' and the route retrieves the data through 'GET'
    Returns:
    This function returns the data set as a dictionary
    """
    global data
    return data

@app.route('/epochs', methods=['GET'])
def modifepoch() -> list:
     """
     This function returns a modified list of epochs given in the query parameters:
     limit and offest. When no limit or offset is given, the function will return 
     the entire data set.
     Args:
     This function does not have a set parameter, but the app route can be called
     with '/epochs' and the route retrieves the data through 'GET'. The route also 
     takes in a limit and offset that can be called with '/epochs?limit=int&offset
     =int'
     Returns:
     This function returns the epochs (strings) in the ISS data set as a list
     """
     global data
     result = []
     ds_statevector = data['ndm']['oem']['body']['segment']['data']['stateVector']
     limit = request.args.get("limit", len(ds_statevector))
     try: 
         limit = int(limit)
     except: 
         return "Error! Invalid repsonse :("

     offset = request.args.get("offset", 0)
     try:
         offset = int(offset)
     except:
         return "Error! Invalid repsonse :("

     for l in range(limit):
         result.append(ds_statevector[offset+l]['EPOCH'])
     return result 

@app.route('/epochs/<string:epoch>', methods=['GET'])
def spefepochs(epoch:str) -> dict:
     """
     This function returns the specific data set that correlates to a specific
     epoch
     Args:
     arg1 (str): epoch is the main parameter for the function and is a string.
     A specific epoch is being called in the command line as stated in the data set. 
     The route retrieves the data set that is attatched to the specific epoch.
     Returns:
     The function returns the data set of the desired epoch (dictionary) 
     """
     global data

     ds_statevector = data['ndm']['oem']['body']['segment']['data']['stateVector']
     for e in range(len(ds_statevector)):
         if(ds_statevector[e]['EPOCH'] == str(epoch)):
             return ds_statevector[e]

@app.route('/epochs/<string:epoch>/speed', methods=['GET'])
def speedofepoch(epoch:str) -> float: 
     """
     This function returns the speed of a desired epoch through obtaining the x dot,
     y dot, and z dot values and mathematically manipulating them through the speed 
     equation
     Args:
     arg1 (str): epoch is the main parameter for the function and is a string.
     A specific epoch is being called in the command line as stated in the data set.      
     The route retrieves the data set that is attatched to the specific epoch.
     Returns:
     This function returns the speed of the epoch (string)
     """
     global data

     ds_statevector = data['ndm']['oem']['body']['segment']['data']['stateVector']
     for e in range(len(ds_statevector)):
         if (ds_statevector[e]['EPOCH'] == str(epoch)):
             xd = abs(float(ds_statevector[e]['X_DOT']['#text']))
             yd = abs(float(ds_statevector[e]['Y_DOT']['#text']))
             zd = abs(float(ds_statevector[e]['Z_DOT']['#text']))

             speed = round(math.sqrt(xd**2 + yd**2 + zd**2),3)
             return str(speed)
     return 0

@app.route('/epochs/<string:epoch>/location', methods=['GET'])
def isslocation(epoch:str) -> dict:
    """
    This function returns latitude, logitude, altitude and geoposition for a specific epoch.
    Args:
    arg1 (str): epoch is the main parameter for the function and is a string. A specific epoch 
    is being called in the command line as stated in the data set. The route retrieves the 
    data set that is attatched to the specific epoch and uses it to then return the latitude, 
    logitude, altitude and geoposition of the ISS at that given epoch.
    Returns:
    This function will return a dictionary.
    """
    global data
    
    ds_statevector = data['ndm']['oem']['body']['segment']['data']['stateVector']
    mean_earth_radius = 6371.07103

    for t in range(len(ds_statevector)):
        if (ds_statevector[t]['EPOCH'] == str(epoch)):
            epoch = ds_statevector[t]['EPOCH']
            ehrs = int(epoch[9:11])
            emins = int(epoch[12:14])

            xd = float(ds_statevector[t]['X']['#text'])
            yd = float(ds_statevector[t]['Y']['#text'])
            zd = float(ds_statevector[t]['Z']['#text'])
            
            lat = math.degrees(math.atan2(zd, math.sqrt(xd**2 + yd**2)))
            lon = math.degrees(math.atan2(yd, xd)) - ((ehrs-12)+(emins/60))*(360/24) + 32
            if(lon < -180):
                lon = lon + 360
            elif(lon > 180):
                lon = lon - 360

            alt = math.sqrt(xd**2 + yd**2 + zd**2) - mean_earth_radius
            geoloc = geocoder.reverse((lat, lon), zoom=15, language='en')
            if (str(geoloc) == "None"):
                geoloc = "Over a body of water"

            location = {
                    "Latitude": float(lat),
                    "Longitude": float(lon),
                    "Altitude": float(alt),
                    "Geoposition": str(geoloc)
                    }
            return location

@app.route('/now', methods=['GET'])
def issnow() -> dict:
    """
    This function finds the most current Epoch and returns the location, geolocation,
    and the speed of the epoch.
    Args: 
    This function does not have a set parameter, but the app route can be called
    with '/now' and the route retrieves the list object through 'GET'.
    Returns:
    This function returns all the information of the epoch via dictionary
    """
    global data
    ds_statevector = data['ndm']['oem']['body']['segment']['data']['stateVector']
    mean_earth_radius = 6371.07103
    
    lowestdiff = 100000000000000000000000
    
    #converting the current time
    nowtime = time.time()

    for t in range(len(ds_statevector)):
        currepoch = ds_statevector[t]['EPOCH']

        #converting current epoch time
        epochtime = time.mktime(time.strptime(currepoch[:-5], '%Y-%jT%H:%M:%S'))
        potentialdiff = abs(nowtime - epochtime)

        if (potentialdiff < lowestdiff): 
            lowestdiff = potentialdiff 
            mostcurr_epoch = currepoch

    for e in range(len(ds_statevector)):
        if (ds_statevector[e]['EPOCH'] == mostcurr_epoch):
            epoch = ds_statevector[e]['EPOCH']
            ehrs = int(epoch[9:11])
            emins = int(epoch[12:14])

            xd = float(ds_statevector[e]['X']['#text'])
            yd = float(ds_statevector[e]['Y']['#text'])
            zd = float(ds_statevector[e]['Z']['#text'])

            lat = math.degrees(math.atan2(zd, math.sqrt(xd**2 + yd**2)))
            lon = math.degrees(math.atan2(yd, xd)) - ((ehrs-12)+(emins/60))*(360/24) + 32
            if(lon < -180):
                lon = lon + 360
            elif(lon > 180): 
                lon = lon - 360
            
            alt = math.sqrt(xd**2 + yd**2 + zd**2) - mean_earth_radius
            uni = "km"
            
            geoloc = geocoder.reverse((lat, lon), zoom=15, language='en')
            if (str(geoloc) == "None"):
                geoloc = "Over a body of water"

            
            xs = abs(float(ds_statevector[e]['X_DOT']['#text']))    
            ys = abs(float(ds_statevector[e]['Y_DOT']['#text']))
            zs = abs(float(ds_statevector[e]['Z_DOT']['#text']))

            speed = round(math.sqrt(xs**2 + ys**2 + zs**2),3)
            unis = "km/s"

            epochinfo ={
                    "1) Epoch information":{ 
                        "Closest Epoch": str(mostcurr_epoch),
                        "Seconds from now": float(lowestdiff),
                        },

                    "2) Location": {
                        "Latitude": float(lat),
                        "Longitude": float(lon)
                        },

                    "3) Altitude":{ 
                        "Value":float(alt),
                        "Units":str(uni)
                        },

                    "4) Geo Information":{
                        "Geoposition": str(geoloc)
                        },

                    "5) Speed":{ 
                        "Value": float(speed),
                        "Units": str(unis)
                        }
                    }
    return epochinfo

@app.route('/comment', methods=['GET'])
def commentlist() -> list:
    """
    This function returns the comment list object from the ISS data set.
    Args:
    This function does not have a set parameter, but the app route can be called
    with '/comment' and the route retrieves the list object through 'GET'.
    Returns:
    This function returns the comment (list)
    """
    global data

    commlist = []
    ds_comm = data['ndm']['oem']['body']['segment']['data']['COMMENT']
    
    for c in range(len(ds_comm)):
        commlist.append(ds_comm[c])
    return commlist    

@app.route('/header', methods=['GET'])
def headerdict() -> dict:
    """
    This function returns the header dictionary object from the ISS data set.
    Args:
    This function does not have a set parameter, but the app route can be called
    with '/header' and the route retrieves the dict object through 'GET'.
    Returns:
    This function returns the header (dict)
    """
    global data
    ds_header = data['ndm']['oem']['header']
    return ds_header

@app.route('/metadata',  methods=['GET'])
def metadatadict() -> dict:
    """
    This function returns the metadata dictionary object from the ISS data set.
    Args:
    This function does not have a set parameter, but the app route can be called
    with '/header' and the route retrieves the dict object through 'GET'.
    Returns:
    This function returns the metadata (dict)
    """
    global data
    ds_meta = data['ndm']['oem']['body']['segment']['metadata']
    return ds_meta

@app.route('/help', methods=['GET'])
def helpepoch() -> list:
    """
    This function returns strings that describe what each app route does and how to call
    each one.
    Args: This function does not have a set parameter, but the app route can be called
    with '/help' and the route retrieves the data through 'GET'.
    Returns:
    This function returns the app routes and their function as a list of strings 
    """
    helpstring = ["/: returns the whole data set",
            "/epochs?limit=int&offset=int: returns a modified list of Epochs with the parameters",
            "/epochs/<str:epoch>: returns state vectors for a specific Epoch",
            "/epochs/<str:epoch>/speed: returns the speed for a specific Epoch",
            "/comment: returns comment list object",
            "/header: returns the header dictionary object",
            "/metadata: returns the metadata dictionary object",
            "/epochs/<epoch>/location: returns latitude, longitude, altitude, and geoposition for given Epoch",
            "/now: returns latitude, longitude, altidue, and geoposition for Epoch that is nearest in time",
            "/help: returns text that explains each app route",
            "/delete-data: deletes all the data from the  dictionary object",
            "/post-data: reloads the dictionary object with data from the web"]
            
    return helpstring

@app.route('/delete-data', methods=['DELETE'])
def deletedata() -> list :
    """
    This function deletes old state vectors from the global data variable.
    Args: This function does not have a set parameter, but the app route can be called
    with '/delete-data' and the route deletes the data through 'DELETE'.
    Returns:
    This function returns an empty data set (dictionary).
    """
    global data 
    data['ndm']['oem']['body']['segment']['data']['stateVector'] = []
    return []

@app.route('/post-data', methods=['POST'])
def postdata() -> dict:
    """
    This function returns an updated dictionary of data from the ISS XML data.
    Args: This function does not have a set parameter, but the app route can be called
    with '/post-data' and the route retrieves the data through 'POST'.
    Returns:
    This function returns the data set (dictionary).
    """
    global data
    response = requests.get(url)
    data = xmltodict.parse(response.text)
    return data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
