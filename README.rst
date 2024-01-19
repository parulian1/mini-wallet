==================
Mini wallet
==================


Case study for backend example of a mini wallet transaction.

--------------------
Local Configuration
--------------------

1. clone source code mini-wallet from github

2. download and install docker desktop / docker into your local
    https://www.docker.com/products/docker-desktop/

3. download and install python3.10 into your local that suitable for your OS
    https://www.python.org/downloads/

4. install VirtualEnv and VirtualEnvWrapper in your local.
   https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-16-04

5. create your own project env

   .. noted::

      $ mkvirtualenv venv

6. activate your project env

   .. noted::

      $ workon venv

7. go to your project directory and install requirement.txt

   .. noted::

      $ pip install requirement.txt

8. run docker desktop or activate your docker then run docker-compose up -d in terminal (this required for running postgres).

9. migrate all models to database.

   for sending your models structure to database used command

   .. noted::

      python manage.py migrate

10. then run the apps.

   .. noted::

      $ python manage.py runserver

11. optional* , you may load data from fixtures into your database.

    .. noted::

        $ python manage.py loaddata < fixtures.json
