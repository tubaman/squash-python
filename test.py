#!/usr/bin/env python
import sys
from cookiestxt import MozillaCookieJar

from squash import Squash


cj = MozillaCookieJar(sys.argv[1])
cj.load(ignore_discard=True, ignore_expires=True)
squash = Squash("http://mysquashserver/squash", cj)
libraries = squash.get_libraries()
for library in libraries:
    print("library: %s" % library['title'])
    for child in library['children']:
        print("child: %s" % child['title'])
        assert child['attr']['rel'] == 'folder'
        folder = squash.get_folder(child['attr']['resId'])
        for requirement in folder:
            print("requirement: %s" % requirement['title'])
from IPython import embed; embed()
