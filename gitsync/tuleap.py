# -*- coding: utf-8 -*-
import json
import requests


class TuleapBase(object):

    def __init__(self, dictionary):
        for current_key in dictionary.keys():
            setattr(self, current_key, dictionary[current_key])

    def __str__(self):
        return "\n".join(["%s : %s" % (x, str(getattr(self, x)))
                          for x in self.__dict__])

    def __repr__(self):
        return str(self)

    def to_string(self):
        return "\n".join(["%s : %s" % (x, str(getattr(self, x)))
                          for x in self.__dict__])


class Token(TuleapBase):

    def __init__(self, dictionary):
        super(Token, self).__init__(dictionary)


class Project(TuleapBase):

    def __init__(self, dictionary):
        super(Project, self).__init__(dictionary)


class GitRepository(TuleapBase):

    def __init__(self, dictionary):
        super(GitRepository, self).__init__(dictionary)


class Tuleap(TuleapBase):

    def __init__(self, host, port=None, protocol='https://', context=None,
                 username=None, password=None):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.context = context
        self._current_token = None
        self.username = username
        self.password = password

    @property
    def url(self):
        if self.context and self.port:
            template = "%(protocol)s%(host)s:%(port)d/%(context)s"
        elif self.context:
            template = "%(protocol)s%(host)s/%(context)s"
        else:
            template = "%(protocol)s%(host)s"
        return template % self.__dict__

    @property
    def api_url(self):
        return "%s/api" % (self.url.rstrip('/'))

    def is_token_valid(self):
        return self._current_token is not None

    @property
    def token(self):
        if not self.is_token_valid():
            url = "%s/tokens" % self.api_url
            data = {"username": self.username,
                    "password": self.password}
            headers = {"Content-Type": "application/json",
                       "Accept": "application/json"}
            r = requests.post(url,
                              data=json.dumps(data),
                              verify=False, headers=headers)
            self._current_token = Token(json.loads(r.text))

        return self._current_token

    def _get_authentification_header(self):
        return {"X-Auth-Token": self.token.token,
                "X-Auth-UserId": str(self.token.user_id)}

    def get_projects(self):
        projects = []
        url = "%s/projects" % (self.api_url)
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        headers.update(self._get_authentification_header())
        limit = 20
        offset = 0
        r = requests.get(url, verify=False, headers=headers, params={'limit': limit, 'offset': offset})
        max_element = int(r.headers['x-pagination-size'])
        while len(projects) < max_element:
            projects_json = json.loads(r.text)
            for project in projects_json:
                projects.append(Project(project))
            offset = offset + limit
            r = requests.get(url, verify=False, headers=headers, params={'limit': limit, 'offset': offset})
        return projects

    def get_repositories_for_projects(self, id):
        repositories = []
        url = "%s/projects/%s/git" % (self.api_url, id)
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        headers.update(self._get_authentification_header())
        limit = 20
        offset = 0
        r = requests.get(url, verify=False, headers=headers, params={'limit': limit, 'offset': offset})
        max_element = int(r.headers['x-pagination-size'])
        while len(repositories) < max_element:
            repositories_json = json.loads(r.text)['repositories']
            for repository in repositories_json:
                repositories.append(GitRepository(repository))
            offset = offset + limit
            r = requests.get(url, verify=False, headers=headers, params={'limit': limit, 'offset': offset})
        return repositories
