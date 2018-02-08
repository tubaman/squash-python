#!/usr/bin/env python
import sys
import re
import json

import requests
from cookiestxt import MozillaCookieJar
from bs4 import BeautifulSoup


class Squash(object):
    """Client for Squash Test Management"""

    def __init__(self, base_url, cookie_jar):
        self.base_url = base_url
        self.cookie_jar = cookie_jar
        self.session = requests.Session()
        for cookie in self.cookie_jar:
            self.session.cookies.set_cookie(cookie)

    def request(self, method, path, *args, **kwargs):
        r = self.session.request(method, self.base_url + path, *args, **kwargs)
        r.raise_for_status()
        if r.headers['Content-Type'].startswith('text/html'):
            soup = BeautifulSoup(r.text, 'html.parser')
            if soup.head.title.text == 'Authentication':
                raise ValueError("Not logged in")
        return r

    def get(self, path, *args, **kwargs):
        return self.request('get', path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.request('post', path, *args, **kwargs)

    def get_libraries(self):
        r = self.get("/requirement-workspace/")
        soup = BeautifulSoup(r.text, 'html.parser')
        txt = re.search(r"model\s*:\s*(.*?),\s*workspace\s*:", unicode(soup.script), re.MULTILINE|re.DOTALL).group(1)
        txt = txt.replace("'", '"')
        libraries = json.loads(txt)
        return libraries

    def get_drive(self, index):
        r = self.get("/requirement-browser/drives/%s/content" % index)
        return r.json()

    def get_folder(self, index):
        r = self.get("/requirement-browser/folders/%s/content" % index)
        return r.json()

    def create_requirement(self, drive_index, name, reference="",
                           description="", criticality="MINOR",
                           category="CAT_UNDEFINED"):
        data = {
            'name': name,
            'reference': reference,
            'description': description,
            'criticality': criticality,
            'category': category,
            'customFields': {},
        }
        r = self.post("/requirement-browser/drives/%s/content/new-requirement" % drive_index, json=data)
        return r.json()


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
