# Map Population

Simple app to get the population given a circle in the map, this is a beta version focusing only the state of Texas.

[![map.png](https://i.postimg.cc/SNjbbWgC/map.png)](https://postimg.cc/9r3nGq5Q)

You might notice some overvalue in the population sizes, probably because the population values used here are an estimation of population count for the year 2020. 
Either the map coverage and the year's population count could be easily adapted to any state/region/country using data available [here](https://sedac.ciesin.columbia.edu/). 

## Getting Started 

Just compose build and up and you will hav ethe Docker container up and running:

```bash
$ docker-compose build
$ docker-compose up
```
If everything went well, you should be able to run the application in http://localhost:5000.
This [article](https://medium.com/analytics-vidhya/how-to-use-nasa-open-access-data-to-find-worldwide-populations-230d19da5763?source=friends_link&sk=410dd39d1711144bf97ee3651d8d29a8) is a good walkthrough for some concepts used in this project.

## Built With


- [Leaflet](https://leafletjs.com/) - A JavaScript library for interactive maps.
- [Jinja2](http://jinja.pocoo.org/docs/2.10/) - A web templating language.
- [Flask](http://flask.pocoo.org/) - A `Python` web framework.
- [SEDAC](https://sedac.ciesin.columbia.edu/) - NASA Socioeconomic Data and Applications Center

## Copyright
Copyright&copy; Caio Davi

Distributed under the MIT License (MIT).

> Notice: If you want to use this app (or part of it), please keep in mind SEDAC asks for cite them when their data is used. Please take a look [here](https://sedac.ciesin.columbia.edu/citations) for more information. 
This is the recommended citation:
> <br>_Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): Population Count, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4JW8BX5. Accessed DAY MONTH YEAR._
