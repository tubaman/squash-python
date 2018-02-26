import re
import json

import requests
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
                raise Exception("Not logged in")
        return r

    def get(self, path, *args, **kwargs):
        return self.request('get', path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.request('post', path, *args, **kwargs)

    def get_libraries(self, workspace='requirement'):
        url = "/%s-workspace/" % workspace
        r = self.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        txt = re.search(r"model\s*:\s*(.*?),\s*workspace\s*:", unicode(soup.script), re.MULTILINE|re.DOTALL).group(1)
        txt = txt.replace("'", '"')
        libraries = json.loads(txt)
        return libraries

    def get_drive(self, id, workspace='requirement'):
        url = "/%s-browser/drives/%s/content" % (workspace, id)
        r = self.get(url)
        return r.json()

    def get_folder(self, id, workspace='requirement'):
        url = "/%s-browser/folders/%s/content" % (workspace, id)
        r = self.get(url)
        return r.json()

    def create_requirement(self, drive_id, name, reference="",
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
        r = self.post("/requirement-browser/drives/%s/content/new-requirement" % drive_id, json=data)
        return r.json()
