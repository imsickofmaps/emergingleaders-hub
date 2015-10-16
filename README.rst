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
