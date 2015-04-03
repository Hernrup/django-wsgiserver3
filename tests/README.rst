testing django-wsgiserver
-------------------------

Assuming you have a unix-like operating system, here are instructions for running
the tests. They should also work on windows with suitable adjustments of the
commands but I have not tried yet.

I set up a virtualenv and activate it

I use pip to make sure the dependencies (django 1.5, requests)
are included::
  pip install -r requirements.txt
  
To run basic tests::
  python test_project.py

To investigate the project yourself "by hand"::

  cd testdjangoproject/testdjango
  python manage.py runwsgiserver

And visit http://locahost:8000/ in a browser

To run ssl tests::

  ./test_ssl

and vist https://localhost:8443/ in a browser
and the ajax tests will run assuming that javascript is activated.

It should look like a bootstrap site if all the css is loaded via the built in static file serving.


  
