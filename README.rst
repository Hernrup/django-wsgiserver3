==================
django-wsgiserver3
==================

(a python3-friendly version of django-wsgiserver)

Warning:
--------

This is a modified version of django-wsgiserver. It was made for my own use with Python 3.
It works for me, and it may work for you, but I cannot guarantee stability or bug-fixes.
At the time of modification, django-wsgiserver was at version 0.8.0rc1.

-Christopher Welborn

The original django-wsgiserver can be found here:
    https://bitbucket.org/cleemesser/django-wsgiserver

Everything else in this README is from the original:

What's New
----------

version 0.8.0beta is updated for use with django 1.5. It now includes
autoreloading of files when they change and integration with django's static
files application.

Summary
-------

django-wsgiserver is a django app for serving Django sites via
CherryPy's excellent, production ready, pure-python web server without needing to
install all of Cherrypy_.  Note that Cherrypy names its server "wsgiserver" but
it is actually a full-blown, multi-threaded http/https web server which has been
used on production sites alone, or more often proxied behind a something like
Apache or nginx.

Uses
----
The wsgiserver component has been used for years in production.  Peter
Baumgartner noted that it solved problems for him on memory on a memory-limited
VPS hosted site [#]_.  Performance-wise it does well: it can serve up thousands
of requests per second [Piel2010].

I have used django-wsgiserver for small production sites, though daemonized
modwsgi_ and uwsgi_ have served me well. I use it all the time though during
development. It's my "pocket-sized" server. completely written in python and it
gives me an instant approximation of the final production environment I use.  In
some ways, it's much better than the development server which is built into
django: It gives a quick way of running an SSL for sites that require https, and
it has no problem serving pages that do multiple ajax calls that would cause the
built-in runserver to hang.

To use django-wsgiserver, I add it to my installed apps in my project settings
file, then do::

   $ manage.py runwsgiserver

and reload my browser page and the problem is fixed.

It's also useful to see if some weird effect is being caused by runserver's
process of loading the settings twice.::

  $ manage.py runwsgiserver autoload=False


This project is a slight modification of code form Peter Baumgartner code (see `Peter's
blog post`_) Peter and others did the work of creating a management command.
I've added a few small improvements from my point of view: It doesn't require
installing cherrypy separately. It uses the same port as the development server
(8000) so I don't need to re-enter my testing url in my browser, and it works by
default with OS's like Mac OS 10.6 and 10.8 and Ubuntu 10.04 which prefer binding
localhost to an ip6 address.

Feature list
------------
- multi-threaded production ready webserver for low to medium traffic sites
- pure python
- setuptools/pip installable (so install right in virtualenv)
- small memory footprint
- by default replaces mimics the django built-in server, serves admin media by
  default for easy testing and deployment. Will serve from STATICFILES_ROOT if it's defined.
- autoreloads code like the development server by default
- supports https/ssl to make testing under https easy

Planned features
----------------
- It would be nice allow to run without installing into INSTALLED_APPS so don't need to touch code cf. gunicorn_django
- It would be nice to print out the requests in development mode (like runserver dose) using logging. Maybe do this with wsgi middleware?
- python 3.x compatibility  

Requirements
------------
- django version 1.5. It might work with 1.3 or 1.4. It will not work fully with 1.2 or below. (see 0.6 series for that)

To get started using the server, you need nothing outside of itself and
the project code that you would like to serve up. However, for ssl support, you
may need PyOpenSSL--though the new cherrypy server includes support for using the
python built-in ssl module depending on which version of python you are using.

License
-------
django-wsgiserver is BSD licensed based on lincolnloop's django-cpservers original code.


Installation
------------
To install, django-wsgiserver follows the usual pattern for a django python application.  You have several options

1. pip install django-wsgiserver OR
2. easy_install django-wsgiserver
3. If you would like to use the latest possible version, you can use pip and mercurial checkout from bitbucket

::

   pip install -e hg+https://bitbucket.org/cleemesser/django-wsgiserver#egg=django-wsgiserver

4. Alternatively you can download the code and install it so that django_wsgiserver is on your PYTHONPATH

After you used one of the methods above, you need to add django_wsgiserver to your INSTALLED_APPS in your django project's settings file

Usage
-----
To see how to run the server as a management command, run::

    $ python manage.py runwsgiserver help  
    
from within your project directory. You'll see something like what's below::

    CPWSGI_HELP = r"""
      Run this project in CherryPy's production quality http webserver.
      Note that it's called wsgiserver but it is actually a complete http server.

	runwsgiserver [options] [cpwsgi settings] [stop]

    Optional CherryPy server settings: (setting=value)
      host=HOSTNAME         hostname to listen on
			    Defaults to 127.0.0.1,
			    (set to 0.0.0.0 to bind all ip4 interfaces or :: for
			    all ip6 interfaces)
      port=PORTNUM          port to listen on
			    Defaults to 8000
      server_name=STRING    CherryPy's SERVER_NAME environ entry
			    Defaults to localhost
      daemonize=BOOL        whether to detach from terminal
			    Defaults to False
      pidfile=FILE          write the spawned process-id to this file
      workdir=DIRECTORY     change to this directory when daemonizing
      threads=NUMBER        Number of threads for server to use
      ssl_certificate=FILE  SSL certificate file
      ssl_private_key=FILE  SSL private key file
      server_user=STRING    user to run daemonized process
			    Defaults to www-data
      server_group=STRING   group to daemonized process
			    Defaults to www-data

      staticserve=True|False|collectstatic]
			    If True, serve the static files automatically using
			    django.contrib.staticfiles like the builting django server.
			    If staticserve=collectstatic, instead serve static files
			    from a single directory at STATIC_ROOT. You need to run
			    "manage.py collectstatic" first.
			    Defaults to True.

      adminserve=True|False  Deprecated. Has no effect. The admin is served if
			     staticserve is active.


    Examples:
      Run a "standard" CherryPy wsgi server--good for local development
	$ manage.py runwsgiserver

      Run a CherryPy server on port 80
	$ manage.py runwsgiserver port=80

      Run a CherryPy server as a daemon and write the spawned PID in a file, don't serve staticfiles or autoreload
	$ manage.py runwsgiserver daemonize=true pidfile=/var/run/django-cpwsgi.pid autoreload=False staticserve=False

      Run a CherryPy server using ssl with test certificates located in /tmp
	$ manage.py runwsgiserver ssl_certificate=/tmp/testserver.crt ssl_private_key=/tmp/testserver.key

      Run the wsgi server but serve all the static files from a single collected file tree
	$ manage.py collectstatic    # collects all the static files to STATIC_ROOT
	$ manage.py runwsgiserver staticserve=collectstatic



Dev Notes
---------

If you want to use an installed version of Cherrypy--perhaps because you now have
a more recent version, you only need to change one line of code in (around line
177) of django_wsgiserver/management/commands/run_wsgiserver.py::

    from django_wsgiserver.wsgiserver import CherryPyWSGIServer as Server
    #from cherrypy.wsgiserver import CherryPyWSGIServer as Server

Just comment out the import from django_wsgiserver.wsgiserver and uncomment the import from cherrypy.wsgiserver to make the switch. For SSL use, you need to search and replace  "django_wsigserver." back to "cherrypy." Note: This change will break the some of the above documentation.

The patches to the original cherrypy wsgiserver are kept in the django-wsgiserver/patches directory of the repo.

To do
-----
- I should probably just add a switch to allow use of the native cherrypy install
- Consider comparisons to other server backends: tornado, uwsgi, gunicorn
- further security tests
- add shell command that will serve a django project in a default way without needing to alter settings.py to add to INSTALLED_APPS
- ? add ability to printout requests like django built in runserver (cf. django-odeon)

Changelog
---------
- 0.8.0 target django 1.5+, python 2.6, 2.7, and 3.2+
        - add autoreload as default
	- serve static files correctly using django.contrib.staticfiles

- 0.7.0 target django 1.3 -- not released -- 
        added support for serving static files directory by default if
	STATICFILES_ROOT is defined. Added more tests: ssl, staticfiles and
	started to document them.  Experimental: STATICFILES_DIRS during
	development to avoid needing to collect all files.
	- Added django-odeon's patch to wsgiserver to make it robust to illegal header lines
	
- 0.6.10 add path for django.contrib.admin to address issue #5,#6
- 0.6.9 typo fix
- 0.6.8 Changed name of bitbucket repo to django-wsgiserver to match it's pypi name
	
- 0.6.7 using open().read() in setup file broke setuptools/pip install because README.rst wasn't included. Created MANIFEST.in file and now include README.rst tests/, docs/ 
- 0.6.6 fix up cherrypy dependency in ssl that was accidently introduced in the
  move to cherrypy.wsgiserver 3.2 branch
- 0.6.5 added mediahandler wsgi application
- 9/6/10 0.6.4 added code to automatically serve the admin media like the
  development server does by default. Can turn off on command line for
  production.

- 9/6/10 0.6.3 - see if I can get the download to finally include all the
  packages--didn't have wsgiserver!

- added test project in tests/ directory

- got tired of typing run_cp_wsgiserver so did a rename so I could use
  runwsgiserver instead.

- updated wsgiserver to svn r2680 (matches cherrypy version 3.2 beta+). This
  fixes some bugs and gives better python 2.6 support.  This version of cherrypy
  will also support python 3.x for whenever django starts supporting it.

- use port 8000 as with django devserver rather than Cherrypy's default 8088

- adapted defaults host=127.0.0.1 in order to work with ip4 by default.  This
  addresses an issue I first noticed on mac OS 10.6 and later on ubuntu 10.04
  where ip6 is active by default. Can get around this by adjusting the host
  option.  For binding all ip4 interfaces, set to 0.0.0.0. For all ip6 interfaces
  I believe you use '::' You can also bind a specific interface by specifying
  host=<specific ip address>  See http://www.cherrypy.org/ticket/711
  
- switched code to use run_cp_wsgiserver instead of runcpserver





Acknowledgments
---------------
Many thanks to Peter and lincolnloop for describing how to do this and writing the code.

Peter acknowledged idea and code snippets borrowed from Loic d'Anterroches, adapted to run as a management command

Note, there is also similar code on PyPi and at http://hg.piranha.org.ua/cpserver/ maintained by Alexander Solovyov

The latest version of the cherrypy wsgiserver can be retrieved with::

    svn co http://svn.cherrypy.org/trunk/cherrypy/wsgiserver

Peter hosts his code at http://github.com/lincolnloop/django-cpserver 

Contributors
------------
 * Charl Botha (cpbotha) http://timescapers.com/  staticfiles work
 * jamalex patch to prevent static files access outside of media root
References
----------

.. [#] For example `Peter's blog post`_ describes using django_cpserver on a VPS.

.. _`Peter's blog post`: http://lincolnloop.com/blog/2008/mar/25/serving-django-cherrypy/

.. _Cherrypy: http://www.cherrypy.org/

.. _[Piel2010] : http://nichol.as/benchmark-of-python-web-servers Nicholas Piel provides a nice comparison of different wsgi servers. Cherrypy's wsgiserver does quite respectably, demonstrating > 2000 requests/sec even at high load for http 1.0 connections with good response latencies.  It does reasonably with http 1.1 connections as well.

.. _modwsgi : http://code.google.com/p/modwsgi/

.. _uwsgi : http://projects.unbit.it/uwsgi/

.. _[dev-picayune2008] : http://www.devpicayune.com/entry/hosting-django-with-cherrypy-wsgi-server Using middleware to add logging and serve the admin media files.  Paste TransLogger.

.. _[arteme2009] : http://www.arteme.fi/2009/02/26/django-cherrypy-dev-server-and-static-files/  More on serving admin files and static files in general with wsgiserver.