#!/usr/bin/env python
import sys
from cookiestxt import MozillaCookieJar

from squash import Squash


cj = MozillaCookieJar(sys.argv[1])
base_url = sys.argv[2]
workspace = sys.argv[3]

cj.load(ignore_discard=True, ignore_expires=True)
squash = Squash(base_url, cj)
libraries = squash.get_libraries(workspace=workspace)
for library in libraries:
    print("library: %s" % library['title'])
    if library['attr']['rel'] == 'drive':
        drive = squash.get_drive(library['attr']['resId'], workspace=workspace)
        for child in drive:
            if child['attr']['rel'] == 'folder':
                print("%s: %s" % (child['attr']['rel'], child['title']))
                folder = squash.get_folder(child['attr']['resId'], workspace=workspace)
                for item in folder:
                    print("%s: %s" % (item['attr']['rel'], item['title']))
            else:
                print("%s: %s" % (child['attr']['rel'], child['title']))
    else:
        print("%s: %s" % (library['attr']['rel'], library['title']))
