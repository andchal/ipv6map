# ipv6map

This is a quick demo I made for an interview.  It shows all of the IPv6 addresses in the world in a heatmap.

A production version can be found [here](http://159.65.229.58/ipv6/).

### Installing

First, create a virtualenv for Python 3 and activate it.
```
$ python3 -m venv myenv
$ source myenv/bin/activate
$ which python
</path/to/myenv/bin/python>
```
You will need to use pip to install Flask and the requests library
```
$ pip install Flask requests
```
Then, clone the repo.
```
$ git clone https://github.com/andchal/ipv6map
```
This project uses geolocation data from [maxmind.com](https://maxmind.com).  Run the following command to download a sample file.
```
$ cd /path/to/ipv6map
$ python data/getdata.py
```
Now, you can start the development server.
```
$ flask run
```
The app will then be visible at http://localhost:5000/ipv6


## Running the tests
All files beginning with 'test_' are unit tests.  You can run them by typing, for example:
```
$ python -m unittest test_rangeTree test_BBox

## Deployment

Before deploying in production, be sure to set
```
app.config[SECRET_KEY]
```
to something secure, change the reference to 'localhost' in 'static/js/map.js' to your preferred hostname,
and set 'debug=False' in app.py

## Built With

* [Leaflet](https://leafletjs.com/)
* [Leaflet.heat](https://github.com/Leaflet/Leaflet.heat)
* [Flask](http://flask.pocoo.org/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to Petah from [this StackOverflow question](https://stackoverflow.com/questions/8567114/how-to-make-an-ajax-call-without-jquery), whose pure js ajax code I have shamelessly stolen.

