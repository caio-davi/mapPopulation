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
            response = getPopulation(longitude, latitude, radius, points)
        except (KeyError, TypeError, ValueError):
            raise JsonError(description='Invalid value.')
        return json_response(data = response, headers_={'X-STATUS': 'ok'})
    else:
        raise JsonError(description='Invalid value.')

def getPopulation(longitude, latitude, radius, points=False):
    radius = radius / 1000   
    population, points = circlePopulation((longitude , latitude), radius, points)
    response = {
        'population' : population,
        'points' : points,
    }
    return response

def circlePopulation(point, radius, points):
    radius = radius
    xy = rasterio.transform.rowcol(affine, point[0], point[1])
    vertice1, vertice2 = get_vertices(point, sqrt(2*radius**2))
    return get_population(vertice1, vertice2, band1, affine, center = point, radius = radius, points = points)

def get_vertices(point, distance):
    vertice1 = get_destination_point(point, 315, distance)
    vertice2 = get_destination_point(point, 135, distance)
    return vertice1, vertice2

def get_destination_point(point, bearing, distance):
    earth_radius = 6373.0
    bearing = radians(bearing)
    longitude = radians(point[0])
    latitude = radians(point[1])
    dest_latitude  = asin(sin(latitude)*cos(distance/earth_radius) +
                    cos(latitude)*sin(distance/earth_radius)*cos(bearing))
    dest_longitude = longitude + atan2(sin(bearing)*sin(distance/earth_radius)*cos(latitude),
                    cos(distance/earth_radius)-sin(latitude)*sin(dest_latitude))
    return (degrees(dest_longitude), degrees(dest_latitude))

def distance(point1, point2):
    R = 6373.0
    lat1 = radians(point1[1])
    lon1 = radians(point1[0])
    lat2 = radians(point2[1])
    lon2 = radians(point2[0])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def get_population(vertice1, vertice2, band, affine, center = False, radius = False, points = False):
    vertice1_xy = rasterio.transform.rowcol(affine, vertice1[0], vertice1[1])
    vertice2_xy = rasterio.transform.rowcol(affine, vertice2[0], vertice2[1])
    population = 0
    pointsArray = []
    try:
        for i in range(vertice1_xy[0], vertice2_xy[0]+1):
            for j in range(vertice1_xy[1], vertice2_xy[1]+1):
                new_point = rasterio.transform.xy(affine , i, j, offset='center')
                if distance(center, new_point) <= radius:
                    population += band[i][j]
                    if points == 'True':
                        pointsArray.append(new_point)
    except (IndexError):
        print('Error: IndexError in ',center) if center else print('Error: Index Error.')
    return population, pointsArray