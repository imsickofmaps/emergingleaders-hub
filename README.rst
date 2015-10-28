emergingleaders-hub
=======================================

Local Setup
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
    # install plugins
    sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git postres
    sudo dokku plugin:install https://github.com/dokku/dokku-rabbitmq.git rabbitmq
    sudo dokku plugin:install https://github.com/ribot/dokku-slack.git

    # create app
    dokku apps:create emergingleaders-hub

    # set a custom buildpack for geodjango support
    dokku config:set emergingleaders-hub BUILDPACK_URL=git://github.com/dulaccc/heroku-buildpack-geodjango.git#1.1

    # create db with GIS support
    export POSTGRES_IMAGE="mdillon/postgis"
    export POSTGRES_IMAGE_VERSION="9.4"
    dokku postgres:create emergingleaders-hub-db
    dokku postgres:connect emergingleaders-hub-db
    CREATE EXTENSION hstore;CREATE EXTENSION postgis;CREATE EXTENSION postgis_topology;
    # connect db
    dokku config:set emergingleaders-hub DATABASE_URL=postgis://postgres:pass@dokku-postgres-emergingleaders-hub-db:5432/emergingleaders_hub_db

    # set up rabbitmq for workers
    dokku rabbitmq:create emergingleaders-hub-rabbitmq
    dokku rabbitmq:link emergingleaders-hub-rabbitmq emergingleaders-hub
    dokku config:set emergingleaders-hub BROKER_URL=amqp://emergingleaders-hub-rabbitmq:@dokku-rabbitmq-emergingleaders-hub-rabbitmq:5672/emergingleaders-hub-rabbitmq
    dokku config:set emergingleaders-hub EMERGINGLEADERS_HUB_VUMI_ACCOUNT_KEY=  EMERGINGLEADERS_HUB_VUMI_CONVERSATION_KEY= EMERGINGLEADERS_HUB_VUMI_ACCOUNT_TOKEN= EMERGINGLEADERS_HUB_FEEDBACK_USSD_NUMBER="*120*8864*xxxx#" EMERGINGLEADERS_HUB_FEEDBACK_MESSAGE_DELAY=120

    # deploy app with git push locally then
    dokku run emergingleaders-hub python manage.py migrate
    dokku run emergingleaders-hub python manage.py createsuperuser


local

::
    git remote add production dokku@host.com:emergingleaders-hub
    git push production master


optional slack notifications

::

    dokku slack:set emergingleaders-hub slackwebhook


The DOKKU_SCALE contains the trigger for how many processes to run for each aspect of the system. This app currently has one web and one worker.
