#!/usr/bin/env python
import sys
from cookiestxt import MozillaCookieJar

from squash import Squash


cj = MozillaCookieJar(sys.argv[1])
base_url = sys.argv[2]

cj.load(ignore_discard=True, ignore_expires=True)
squash = Squash(base_url, cj)
libraries = squash.get_libraries()
for library in libraries:
    print("library: %s" % library['title'])
    if library['attr']['rel'] == 'drive':
        drive = squash.get_drive(library['attr']['resId'])
        for child in drive:
            print("child: %s" % child['title'])
            if child['attr']['rel'] == 'folder':
                folder = squash.get_folder(child['attr']['resId'])
                for requirement in folder:
                    print("requirement: %s" % requirement['title'])
            else:
                print("unknown child rel: %s" % child['attr']['rel'])
    else:
        print("unknown library rel: %s" % library['attr']['rel'])
