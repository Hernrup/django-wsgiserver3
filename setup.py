from distutils.core import setup

setup(
    name="django-wsgiserver3",
    version="0.8.1",
    license="BSD",
    description="""django-wsgiserver installs a web server for Django using CherryPy's WSGI server.""",
    author="""Peter Baumgartner Chris Lee-Messer the authors of CherryPy""",
    author_email="chris@lee-messer.net, pete@lincolnloop.com",
    maintainer="Chris Lee-Messer",
    # from README.rst
    long_description=open('README.rst').read(),
    url="http://bitbucket.org/cleemesser/django-wsgiserver/downloads",
    download_url="http://bitbucket.org/cleemesser/django-wsgiserver/downloads",
    packages=[
        "django_wsgiserver",
        "django_wsgiserver.management",
        "django_wsgiserver.management.commands",
        "django_wsgiserver.wsgiserver",
    ],
    # package_data
    # data_files=[],# where to put test certs
    classifiers=['Framework :: Django',
                 'Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'License :: OSI Approved :: BSD License',
                 'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
                 'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                 ],
)
