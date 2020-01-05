#!/usr/bin/env python
from flask import Flask, render_template, make_response, request
from flask_json import FlaskJSON, JsonError, json_response
from flask_cors import CORS
import rasterio
from math import sin, cos, sqrt, atan2, radians, asin, degrees

app = Flask(__name__, instance_relative_config=True)
path = 'rasters/texas.tif'
dataset = rasterio.open(path)
band1 = dataset.read(1)
affine = dataset.transform
FlaskJSON(app)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/population', methods = ['POST'])
def population():
    if request.method == 'POST':
        try:
            points = str(request.get_json()['data']['points'])
            location = request.get_json()['data']['location']
            longitude = float(location['coordinates'][0])
            latitude = float(location['coordinates'][1])
            radius = float(location['radius'])
            point = (longitude, latitude)
            response = circle_population(point, radius, points)
        except (KeyError, TypeError, ValueError, IndexError):
            return json_response(501)
        return  json_response(data = response, headers_={'X-STATUS': 'ok'})
    else:
        raise JsonError(description='Invalid value.')

def circle_population(point, radius, points):
    # meters to kilometers:
    radius = radius / 1000
    # get the vertices of a square containing the circle:
    vertice1, vertice2 = get_vertices(point, sqrt(2*radius**2))
    # get the population of the circle:
    population, points = get_population(vertice1, vertice2, band1, affine, center = point, radius = radius, points = points)
    # return as a dict (wich will be converted to JSON by Flask):
    response = {
        'population' : population,
        'points' : points,
    }
    return response

def get_vertices(point, distance):
    # get the top left vertice by walking the given distance towards 315 deegres from the center:
    vertice1 = get_destination_point(point, 315, distance)
    # get the botton right vertice by walking the given distance towards 135 deegres from the center:
    vertice2 = get_destination_point(point, 135, distance)
    # return the vertices:
    return vertice1, vertice2

def get_destination_point(point, bearing, distance):
    # the earth radius (in km):
    earth_radius = 6373.0
    # transform the angle to radians:
    bearing = radians(bearing)
    # transform the latitude to radians:
    longitude = radians(point[0])
    # transform the longitude to radians:
    latitude = radians(point[1])
    # move the given distance towards the angle in the y axis:
    dest_latitude  = asin(sin(latitude)*cos(distance/earth_radius) +
                    cos(latitude)*sin(distance/earth_radius)*cos(bearing))
    # move the given distance towards the angle in the x axis:
    dest_longitude = longitude + atan2(sin(bearing)*sin(distance/earth_radius)*cos(latitude),
                    cos(distance/earth_radius)-sin(latitude)*sin(dest_latitude))
    # return the vertice in degrees (as they are lat and lgd):
    return (degrees(dest_longitude), degrees(dest_latitude))

def distance(point1, point2):
    R = 6373.0
    # transform all the angles to radians: 
    lat1 = radians(point1[1])
    lon1 = radians(point1[0])
    lat2 = radians(point2[1])
    lon2 = radians(point2[0])
    # calculate the difference between the latitudes:
    dlon = lon2 - lon1
    # calculate the difference between the longitudes:
    dlat = lat2 - lat1
    # using the ‘haversine’ formula:
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def get_population(vertice1, vertice2, band, affine, center = False, radius = False, points = False):
    # get the position (x,y) in the image for the first vertice:
    vertice1_xy = rasterio.transform.rowcol(affine, vertice1[0], vertice1[1])
    # get the position (x,y) in the image for the second vertice:
    vertice2_xy = rasterio.transform.rowcol(affine, vertice2[0], vertice2[1])
    # start a counter for the population:
    population = 0
    # create an empty array for the data points 
    pointsArray = []
    # for all pixels between those vertices:
    for i in range(vertice1_xy[0], vertice2_xy[0]+1):
        for j in range(vertice1_xy[1], vertice2_xy[1]+1):
            # get the value of the the pixel 
            new_point = rasterio.transform.xy(affine , i, j, offset='center')
            # if the the distance is less than the radius:
            if distance(center, new_point) <= radius:
                # increase the population with the value of the pixel:
                population += band[i][j]
                # if the data points were requested:
                if points == 'True':
                    # append them to the array:
                    pointsArray.append(new_point)
    return population, pointsArray