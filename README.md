# ISS Tracker Project 

## What to Expect?
Within the repository, you will find a python script named "iss_tracker.py". 
This file contains different app routes that will help the user obtain and manipulate 
parts of the data. The second file you will find is an assembled docker file named
"Dockerfile" that contains commands for building a new image for iss-tracker.py. 
The last file that you will find in the repo is called the docker-compose.yml.
This file helps with managing the container in a more efficient way! 

## The ISS Data Set
What is the ISS and what is the data set? The ISS is NASA's International Space 
Station! The data set provided by the Trajectory Operations and Planning Officer 
shows where the ISS is located at different times. So cool right? 

So, how exactly are you supposed to access the data set? Great question! 
You would need to open up a browser and visit this link: 
**[ISS Data Set](https://spotthestation.nasa.gov/trajectory_data.cfm)**

From there, you will see that you have the option to download the data set as a TXT 
file or an XML file. For the purposes of this python script, you would need to 
download the XML file. The data set provides position and velocity data generated by 
the ISS Trajectory Operations and Planning Officer flight controllers at NASA!

## Try it out!
Now there are a couple of ways that you can interface with the code. 
First is through pulling from the repository directly and using the flask app in the command line. The second is using a docker image container with preset code.

### The Flask App and How to Use it

**What is it?**
The flask application is written in the python script "iss_tracker.py". It is mainly used for querying the ISS position and velocity data through various app routes!

**How Do You Access it?**
In order to actually run the application:

1. Log into your vm in two seperate command line windows using:
``username-vm``
2. Pull the data from the repository 
3. Then in one of the windows run the debugger server using:
``flask --app app --debug run``
4. Once the server is running, you can then start inputting the different queries in the other window you logged into
5. To run the queries, you must use the command:
``curl localhost:5000``

### The Docker Image and How to Use it

**What is it?**
Docker is a containerization platform that can package software called containers for
others to use! The Dockerfile included in the repository helps to build the docker
image that was used for iss_tracker.py.

**How Do You Access it?**
In order to obtain the container and run the docker image, there are two ways!

If you would like to just obtain the Docker Image and run the code:
1. pull the docker image in your vm with the handle:
``docker pull dcn558/iss_tracker:project`` 
2. run the image in seperate vm window with the command: 
``docker run -it --rm -p 5000:5000 dcn558/iss_tracker:project``
3. run the different routes

If you would like to start from the Dockerfile and build your own image:
1. clone the repository to obtain the Dockerfile and the python script in one vm
window
2. create your own docker hub account
3. once you modify the code or make your own code, you can build your own image
using:
``docker build -t <dockerhubusername>/iss_tracker:<version> .`` 
4. then to check if you have created your image run the line: ``docker images``
5. then to test your image, open another vm window and type the command:
``docker run -it --rm -p 5000:5000 username/iss_tracker:<version>``
6. now you can interface with the container and the code in the other vm window!  

**Docker Compose File**
Let's say you pull all the files from the repository and you want to run the docker! 
You can use the docker compile file to run services/ actions!

Here are some things you can try out!

``docker-compose version``: Prints out the version information

``docker-compse config``: Validates the docker compose file

``docker-compose up``: spins up all the services

``docker-compose down``: tears down the services

``docker-compose build``: builds the images in the YAML file

``docker-compose run``: runs the container defined in the YAML file

### What are the Different Queries?
In this python script, there are eight different routes you can experiment with.

1. If you want to retrieve the whole entire data set, you can input:

``curl localhost:5000/``

This will return the whole entire data set as a dictionary. So if you see your screen flash with a bunch of numbers, 
do not be alarmed! That is just the computer communicating that it was able to turn the XML file into a readable 
dictionary for you to manipulate.

2. If you want to see all of the Epochs in the data set, you can input:

``curl localhost:5000/epochs``

This will return all of the Epochs ***ONLY***. You will multiple lines that look like:

> 2023-048T12:04:00.000Z

3. Now, what if you want to see a set of Epochs starting from the middle of the data set? You can now add a query parameter: limit and offset!
So if you would like to see the Epochs 10 through 14, you would input:

``curl localhost:5000/epochs?limit=4&offset=9``

Since the computer starts printing from index 0, you would want your offset to equal the Epoch that you want - 1 (ex: 6th Epoch = offset of 5).
You will most likely see a list that looks like this:

> [ 
>
>  "2023-082T11:48:00.000Z",
>
>  "2023-082T11:52:00.000Z",
>
>  "2023-082T11:56:00.000Z",
>
>  "2023-082T12:00:00.000Z"
>
> ]

4. If you want to see the state vectors for a specific Epoch, you can input:

``curl localhost:5000/epochs/(specific epoch)``

So, if you wanted to see the second Epoch data set, you would want to put:

``curl localhost:5000/epochs/2023-069T12:04:00.000Z``

This will return the data set that belongs to the specific Epoch! You will see something along the lines of:

> X = -5998.4652356788401
>
> Y= 391.26194859011099
>
> Z = -3164.26047476557
>
> X_DOT = -2.8799691318087701
>
> Y_DOT = -5.2020406581448801
>
> Z_DOT = 4.8323394499086101

5. If you want to see the speed for a specific Epoch in the data set, you can input:

``curl localhost:5000/epochs/(specific epoch)/speed``

So if you wanted to see the second Epoch's speed, you would type:

``curl localhost:5000/epochs/2023-069T12:04:00.000Z/speed``

This will return a float! 

>
> 7.66
>

6. If you want to see the comments of the data set, you can input:

``curl localhost:5000/comment``

This will return a list of strings with comments of the data! It will most likely 
look like this:

> [
>
>  "Units are in kg and m^2",
>
>  "MASS=460875.00",
>
>  "DRAG_AREA=1382.32",
>
>  "DRAG_COEFF=3.30",
>
>  "SOLAR_RAD_AREA=0.00",
>
> "SOLAR_RAD_COEFF=0.00",
>
>  "Orbits start at the ascending node epoch",
>
>  "ISS first asc. node: EPOCH = 2023-03-13T12:02:49.637 $ ORBIT = 2694 $ LAN(DEG) = 90.97459",
>
>  "ISS last asc. node : EPOCH = 2023-03-28T11:07:27.443 $ ORBIT = 2926 $ LAN(DEG) = 15.99058",
>
>  "Begin sequence of events",
>
>  "TRAJECTORY EVENT SUMMARY:",
>
>  null,
>
>  "|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP    |",
>
>  "|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
>
>  "|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
>
>  "=============================================================================",
>
>  "SpX27 Launch          074:00:30:41.000             0.0     428.2     408.6",
>
>  "(0.0)   (231.2)   (220.6)",
>
>  null,
>
>  "SpX27 Docking         075:11:52:14.000             0.0     428.1     408.4",
>
>  "(0.0)   (231.1)   (220.5)",
>
>  null,
>
>  "68S Undocking         087:09:52:30.000             0.0     425.0     407.4",
>
>  "(0.0)   (229.5)   (220.0)",
>
>  null,
>
>  "=============================================================================",
>
>  "End sequence of events"
>
> ]

7. If you would like to see the header dictionary, you can input:

``curl localhost:5000/header``

You will most likely see:

> {
>
>  "CREATION_DATE": "2023-073T02:14:56.800Z",
>
>  "ORIGINATOR": "JSC"
>
> }

8. If you would like to see the meta data dictionary, you can input:

``curl localhost:5000/metadata``

You will most likely see something along the lines of:

> {
>
>  "CENTER_NAME": "EARTH",
>
>  "OBJECT_ID": "1998-067-A",
>
>  "OBJECT_NAME": "ISS",
>
>  "REF_FRAME": "EME2000",
>
>  "START_TIME": "2023-072T12:00:00.000Z",
>
>  "STOP_TIME": "2023-087T12:00:00.000Z",
>
>  "TIME_SYSTEM": "UTC"
>
> }

9. If you would like to get the location for a specific epoch, you can input:

``curl localhost:5000/epochs/(specific epoch)/location``

So, if you wanted to see the location of the second epoch, you can input:

``curl localhost:5000/epochs/2023-072T12:00:00.000Z/location``

The app route will return a dictionary that gives the altitude, geoposition, latitude
and longitude of the specific epoch.

> {
>
>  "Altitude": 427.80942237159707,
>
>  "Geoposition": "Over a body of water",
>
>  "Latitude": -8.60388519298572,
>
>  "Longitude": 107.42432909697723
>
> }

10. If you would like to see the location and speed of the most recent epoch, you
can input:

``curl localhost:5000/now``

You will see the closest epoch, how far away it is from the current time, location, 
and speed!

> {
>
>  "1) Epoch information": {
>
>    "Closest Epoch": "2023-073T22:40:00.000Z",
>
>    "Seconds from now": 26.14461374282837
>
>  },
>
>  "2) Location": {
>
>    "Latitude": 36.442966873224286,
>
>    "Longitude": 91.52686172399729
>
>  },
>
>  "3) Altitude": {
>
>    "Units": "km",
>
>    "Value": 418.4332916640178
>
>  },
>
>  "4) Geo Information": {
>
>    "Geoposition": "Urt Moron, Golmud City, Haixi Mongol and Tibetan Autonomous Prefecture, Qinghai, China"
>
>  },
>
>  "5) Speed": {
>
>    "Units": "km/s",
>
>    "Value": 6789.504
>
>  }
>
> }

11. If you need a friendly reminder of what each app route does, you are in luck! In order to see each app route and their function, just input:

``curl localhost:5000/help``

This will return a list of app routes provided in the file and their descriptions.

12. Let's say that you notice that the data set you are using is outdated, well no problem! You can delete the current data that you have stored using:

``curl localhost:5000/delete-data -X DELETE``

It is important to note that you must need the: `` -X DELETE`` because the action for the app route is not 'GET' like the previous routes. So if you forget that part of the command, it will return an error. 

To test if you cleared the data, you can try to run:

``curl localhost:5000/``

and it should return an empty data set.

> []

13. In order to get updated data, you should input: 

``curl localhost:5000/post-data -X POST`` 

This should return an updated data set as a dictionary!

After you delete your data, you need to reload the data using post in order to run the other routes! And just like with the "delete-data" route, you need to make sure to have the ``-X POST`` in the command for the route to do its action.






