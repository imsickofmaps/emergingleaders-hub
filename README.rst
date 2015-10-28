emergingleaders-hub
=======================================

Setup
---------------------------------------

Remember to enable hbase and postgis on your postgres template
::
    psql -d template1 -c 'CREATE EXTENSION hstore;CREATE EXTENSION postgis;CREATE EXTENSION postgis_topology;'
    createdb -U postgres -h localhost emergingleaders_hub
    ./manage.py migrate

If postgis has not been installed, this may work for you (use appropriate version numbers)
::
    sudo apt-get install -y postgis postgresql-9.3-postgis-2.1


dokku Setup
---------------------------------------

on server

::

    dokku apps:create emergingleaders-hub
    dokku config:set emergingleaders-hub BUILDPACK_URL=git://github.com/dulaccc/heroku-buildpack-geodjango.git#1.1
    sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
    export POSTGRES_IMAGE="mdillon/postgis"
    export POSTGRES_IMAGE_VERSION="9.4"
    dokku postgres:create emergingleaders-hub-db
    dokku config:set emergingleaders-hub DATABASE_URL=postgis://postgres:pass@dokku-postgres-emergingleaders-hub-db:5432/emergingleaders_hub_db
    dokku postgres:connect emergingleaders-hub-db
    CREATE EXTENSION hstore;CREATE EXTENSION postgis;CREATE EXTENSION postgis_topology;

    # deploy app locally
    dokku run emergingleaders-hub python manage.py migrate
    dokku run emergingleaders-hub python manage.py createsuperuser


local

::
    git remote add production dokku@host.com:emergingleaders-hub
    git push production master


slack notifications

::
    sudo dokku plugin:install https://github.com/ribot/dokku-slack.git
    dokku slack:set emergingleaders-hub slackwebhook
