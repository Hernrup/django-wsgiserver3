Proxying and/or load balancing the wsgiserver instance behind nginx
-------------------------------------------------------------------

#) create your project, make sure you've installed django-wsigserver and added it to the installed apps in your settings.py file as described in the README.rst
#) python manage.py runwsgiserver (This will start the cherrypy webserver on port 8000 by default. In production, you may want to launch this with a process manager like upstart, supervisor or daemon tools)
#) create an nginx.conf file with 

::

    http {
      upstream mydjangoproject {
	server 127.0.0.1:8000 weight=3;
	# run more instances of wsgiserver on alternative ports to handle more requests
	# nginx will load balance them
	#server 127.0.0.1:8001;
	#server 127.0.0.1:8002;    
	#server 127.0.0.1:8003;
      }

      server {
	listen 80;
	server_name www.domain.com;
	location / {
	  proxy_pass http://mydjangoproject;
	}
      }
    }
