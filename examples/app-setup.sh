#!/bin/sh

# quit on errors:
set -o errexit

# quit on unbound symbols:
set -o nounset

DIR=`dirname "$0"`

cd $DIR
export FLASK_APP=app.py

# Install specific dependencies
mkdir $DIR/instance

npm install -g mkdirp node-sass@3.8.0 clean-css-cli requirejs uglify-js

# Install assets
flask collect -v
flask webpack buildall

# Create the database
flask db init
flask db create
