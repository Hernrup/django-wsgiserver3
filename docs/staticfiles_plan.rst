static files notes and plan
===========================
With django 1.3, there will be more support for static files based on
incorporating django-static files into django.contrib.  This is great and it
should make it possible to automatically deploy django apps with the wsgiserver.



a new settings parameter

{{STATIC_URL}}
settings.STATIC_URL  # probably a default '/static/'
setting.STATIC_ROOT  # possibly a default exists

django.contrib.staticfiles is being added

# the directories listed in STATICFILES_DIRS will by default will be added as subdirectories of /static/
STATICFILES_DIRS = ( "/path/to/another/directory",)

STATICFILES_DIRS = [
    "/path/to/another/directory",
    ("altdirprefix", "/path/to/root/of/static/files"),
    ]
altdirprefix gets added to STATIC_URL    

on the otherhand, when using manage.py collectstatic, it fuses all the static directories at STATIC_ROOT ex::
 
   app1/
       static/file1
       static/directory1/
   app2/
       static/file2
       static/directory/2

Then if you run django-admin.py collectstatic, STATIC_ROOT will look like this::

   STATIC_ROOT/
       admin/
       file1
       directory1/
       file2
       directory2/
       

So it seems like ideally, in development we would serve the fused directory from their original spots.  I would guess it would be easiest to use django.contrib.staticfiles.views.serve() own function to serve.

Here is the full contents of that file::

    """
    Views and functions for serving static files. These are only to be used during
    development, and SHOULD NOT be used in a production setting.

    """
    import os
    import posixpath
    import urllib

    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured
    from django.http import Http404
    from django.views import static

    from django.contrib.staticfiles import finders

    def serve(request, path, document_root=None, insecure=False, **kwargs):
	"""
	Serve static files below a given point in the directory structure or
	from locations inferred from the staticfiles finders.

	To use, put a URL pattern such as::

	    (r'^(?P<path>.*)$', 'django.contrib.staticfiles.views.serve')

	in your URLconf.

	It uses the django.views.static view to serve the found files.
	"""
	if not settings.DEBUG and not insecure:
	    raise ImproperlyConfigured("The staticfiles view can only be used in "
				       "debug mode or if the the --insecure "
				       "option of 'runserver' is used")
	normalized_path = posixpath.normpath(urllib.unquote(path)).lstrip('/')
	absolute_path = finders.find(normalized_path)
	if not absolute_path:
	    raise Http404("'%s' could not be found" % path)
	document_root, path = os.path.split(absolute_path)
	return static.serve(request, path, document_root=document_root, **kwargs)




While in light production it could be would want to serve ( STATIC_URL, STATIC_ROOT ) after running collectstatic.

I'm not sure if I want to stic with using 

Finally WSGISERVER_STATIC could be used to serve arbitrary static directories outside of the django static file 

       
STATICFILES_FINDERS is a tuple which list all the ways that the static files are found--I suppose could think about supporting these as well.

see also::
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

Other approaches
----------------
There are quite a few examples of wsgi applications which serve static files

bottle http://bottlepy.org/
luke/static https://bitbucket.org/luke/static/

cherrypy has static serving 





