# Texas Population

Simple app to get the Texas population. This could be easily adapted to any state/region/country using data available [here](https://sedac.ciesin.columbia.edu/). 

## Getting Started 

Just compose build and up and you will hav ethe Docker container up and running:

```bash
$ docker-compose build
$ docker-compose up
```
If everything went well, you should be able to run the application in http://localhost:5000.

## Built With

- [Flask](http://flask.pocoo.org/) - A `Python` web framework.
- [Jinja2](http://jinja.pocoo.org/docs/2.10/) - A web templating language.
- [Leaflet](https://leafletjs.com/) - A JavaScript library for interactive maps.
- [SEDAC](https://sedac.ciesin.columbia.edu/) - NASA Socioeconomic Data and Applications Center

## Copyright
Copyright&copy; Caio Davi

Distributed under the MIT License (MIT).

> Notice: If you want to use this app, please keep in mind SEDAC asks for cite them when their data is used. Please take a look [here](https://sedac.ciesin.columbia.edu/citations) for more information. 
This is the recommended citation:
> <br>_Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): Population Count, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4JW8BX5. Accessed DAY MONTH YEAR._
