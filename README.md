GeoDiggerUI
===========

The web interface for GeoDigger, which allows filtering of GeoDigger information.

## Installation

    git clone git://github.com/GeoDigger/geodigger-ui.git
    cd geodigger-ui
    sudo python setup.py install

## Usage

First, copy `config.example.py` to `config.py` in the `geodiggerui` folder and set up the configuration variables.

To use Pyramid's built-in development server, run

    pserve development.ini
    
Browse to http://localhost:8080/ to see the frontend.

Note: pserve should NOT be used in a production environment. Instead, set up nginx or Apache with a `wsgi` module to serve the site.

## Screenshot

![Screenshot](https://raw.githubusercontent.com/GeoDigger/geodigger-ui/master/frontend.png "Screenshot")
