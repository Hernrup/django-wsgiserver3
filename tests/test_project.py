# This is still a skelton right now

# using requests with django
# probably useful for api testing
# command line clients
# requests is not the highest efficiency library---eventually might need curl-based system
# if trying to do high volume application

# for django I'm using the following strategy for dealing with csrf security
# the main index includes the token. I then save this and use it in following requests
# by sending 'X-CSRFToken': csrftoken in the following headers
# I added this to my template in django to force the appearance of the csrf cookie
#  <div style="display:none"> <-- force inclusion of the cookie -->
#    <input type="hidden" name="csrfmiddlewaretoken" value="{{csrf_token}}"/>
#  </div>
# my view uses RequestContext to render the template

import requests, sys, os, time
import subprocess, StringIO
import unittest
import random

PIDFILE = os.path.join(os.getcwd(),'test_project.pid')

def launch_project_developer_mode():
    """start django wsgiserver as daemon in developer mode
    except can't do autoreload as daemon"""
    #print "hello from launch project developer mode"
    #sout = StringIO.StringIO()
    #serr = StringIO.StringIO()
    try:
        subprocess.check_call(["python", r"testdjangoproject/testdjango/manage.py",
            "runwsgiserver",
            "threads=10", "daemonize",
            "autoreload=0",
            "pidfile=%s" % PIDFILE])

    except subprocess.CalledProcessError, msg:
        print msg

def launch_project_production_mode():
    """start django wsgiserver as daemon
    do it in production mode: do not serve static files or autoreload
    create thread file"""
    # print "hello from launch project production mode"
    subprocess.check_call(["python", r"testdjangoproject/testdjango/manage.py",
                     "runwsgiserver",
                     "staticserve=False",
                     "autoreload=False",
                     "threads=10", "daemonize",
                     "pidfile=%s" % PIDFILE])
    

def stop_project():
    #print "olleh from stop project"
    subprocess.call(["python", r"testdjangoproject/testdjango/manage.py", "runwsgiserver",
                     "stop", "pidfile=%s" % PIDFILE])

    

class TestDeveloperMode(unittest.TestCase):
    rooturl = r'http://localhost:8000/'
    ajaxurl = r'http://localhost:8000/testajax/' # remember it needs to end in a slash
    @classmethod
    def setUpClass(clss):
        launch_project_developer_mode()
        time.sleep(1) # it takes a little time for the server to get started
        #self.session = requests.Session()

        #self.ajaxurl = r'http://localhost:8000/testajax/' # remember it needs to end in a slash

    @classmethod
    def tearDownClass(clss):
        stop_project()

    def test_django_root(self):
        time.sleep(1)
        self.session = requests.Session()
        r = self.session.get(self.rooturl)
        self.csrftoken =  r.cookies['csrftoken']
    

        self.assertTrue(r.status_code in (200, 304))


    def _check_ok(self, resp):
        self.assertTrue(resp.status_code in (200, 304))
        return resp
        
    def test_http_verbs(self):
        # first get the csrftoken
        self.session = requests.Session()
        r = self.session.get(r'http://localhost:8000/') # a session allows for persistent cookies and things
        csrftoken =  r.cookies['csrftoken']
        self.csrftoken = csrftoken
        headers= {#'content-type':'application/json',
                'X-CSRFToken': csrftoken }

        url = self.ajaxurl    
        self._check_ok(self.session.post(url, data='', headers=headers))
        self._check_ok(self.session.put(url, data='', headers=headers))
        self._check_ok(self.session.delete(url, data='', headers=headers))
        self._check_ok(self.session.head(url, data='', headers=headers))
        self._check_ok(self.session.options(url, data='', headers=headers))
        self._check_ok(self.session.patch(url, data='', headers=headers))


    # I have not found a good way to test autoreloading    
    # def test_autoreload(self):
    #     if not hasattr(self, 'session'):
    #         self.session = requests.Session()
    #     r=self.session.get(r'http://localhost:8000/testautoreload')
    #     self.assertTrue(r.status_code == 200)
    #     print r.text
    #     fp=open('testdjangoproject/testdjango/testdjango/autoload_test.py', 'w+')
    #     fp.write('x=%d\n' % random.randint(0,100))
    #     fp.close()
    #     time.sleep(2) # allow time for reload
    #     r=self.session.get(r'http://localhost:8000/testautoreload')
    #     print r.status_code
    #     self.assertTrue(r.status_code == 200)
    #     print r.text

    def test_get_static_from_root(self):
        """get a static file out of the root of the static directory"""
        r = requests.get(os.path.join(self.rooturl, 'static/teststaticfile1.txt'))
        # print r.status_code
        self.assertTrue(r.status_code==200) # or  r.status_code == 304)
        
    def test_get_static_from_app(self):
        """get a static file out of an app static directory"""
        r = requests.get(os.path.join(self.rooturl, r'static/dummyapp/dummyapp_in_sub.txt'))
        # print r.status_code
        self.assertTrue(r.status_code==200) # or  r.status_code == 304)


class TestProductionMode(unittest.TestCase):
    rooturl = r'http://localhost:8000/'
    ajaxurl = r'http://localhost:8000/testajax/' # remember it needs to end in a slash
    @classmethod
    def setUpClass(clss):
        launch_project_production_mode()
        time.sleep(1) # it takes a little time for the server to get started
        #self.session = requests.Session()

        #self.ajaxurl = r'http://localhost:8000/testajax/' # remember it needs to end in a slash

    @classmethod
    def tearDownClass(clss):
        stop_project()

    def test_django_root(self):
        time.sleep(1)
        self.session = requests.Session()
        r = self.session.get(self.rooturl)
        self.csrftoken =  r.cookies['csrftoken']
    

        self.assertTrue(r.status_code in (200, 304))


    def _check_ok(self, resp):
        self.assertTrue(resp.status_code in (200, 304))
        return resp
        
    def test_http_verbs(self):
        # first get the csrftoken
        self.session = requests.Session()
        r = self.session.get(r'http://localhost:8000/') # a session allows for persistent cookies and things
        csrftoken =  r.cookies['csrftoken']
        self.csrftoken = csrftoken
        headers= {#'content-type':'application/json',
                'X-CSRFToken': csrftoken }

        url = self.ajaxurl    
        self._check_ok(self.session.post(url, data='', headers=headers))
        self._check_ok(self.session.put(url, data='', headers=headers))
        self._check_ok(self.session.delete(url, data='', headers=headers))
        self._check_ok(self.session.head(url, data='', headers=headers))
        self._check_ok(self.session.options(url, data='', headers=headers))
        self._check_ok(self.session.patch(url, data='', headers=headers))


    def test_get_static_from_root(self):
        """get a static file out of the root of the static directory"""
        r = requests.get(os.path.join(self.rooturl, 'static/teststaticfile1.txt'))
        # print r.status_code
        self.assertTrue(r.status_code==404) 
        
    def test_get_static_from_app(self):
        """get a static file out of an app static directory"""
        r = requests.get(os.path.join(self.rooturl, r'static/dummyapp/dummyapp_in_sub.txt'))
        # print r.status_code
        self.assertTrue(r.status_code==404) # or  r.status_code == 304)

        
    

def do_stuff():
    session = requests.Session()
    r = session.get(r'http://localhost:8000/') # a session allows for persistent cookies and things

    # print "cookies:", r.cookies
    csrftoken = r.cookies['csrftoken'] # or something
    # print "csrftoken:", csrftoken, 

    # xmlrequestheader 
    # sys.exit(0)
    # test ajax
    # import json
    # useragent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'


    payload = {'some':'data'}

    headers= {#'content-type':'application/json',
              'X-CSRFToken': csrftoken }


    def check(resp):
        # print resp.status_code,
        if resp.status_code==200:
            print 'OK [%s] %s %s' % (resp.request.method, resp.request.path_url, resp.status_code)
        else:
            print 'BAD [%s] %s %s' % (resp.request.method, resp.request.path_url, resp.status_code)
        return resp

    staticfilename = 'teststaticfile1.txt'
    r = check(session.get(os.path.join(r'http://localhost:8000/static/',staticfilename)))

    # print "static file:", r.text, repr(r.text), repr(staticfilename)

    url = r'http://localhost:8000/testajax/' # remember it needs to end in a slash

    check(session.get(url, headers=headers))
    check(session.post(url, data='', headers=headers))
    check(session.put(url, data='', headers=headers))
    check(session.delete(url, data='', headers=headers))
    check(session.head(url, data='', headers=headers))
    check(session.options(url, data='', headers=headers))
    check(session.patch(url, data='', headers=headers))


# payload = {'key1': 'value1', 'key2': 'value2'}
# r = requests.post("http://httpbin.org/post", data=payload)
# print r.text

##### test autoload ####

def non_unittest_main():
    try:    
        launch_project_developer_mode()
        print "started project"
        time.sleep(1.0)
        do_stuff()
        raw = raw_input("press to end")
        stop_project()
    except: # KeyboardInterrupt:
        print sys.exc_info()
        stop_project()


    
if __name__== '__main__':
    # non_unittest_main()
    unittest.main()



