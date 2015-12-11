# -*- coding: utf-8 -*-
import getpass
from github import Github
from gitsync.model.project import Project
from gitsync.provider import Provider


class GithubProvider(Provider):

    def __init__(self, user):
        super(Provider, self).__init__()
        self.user = user
        passw = getpass.getpass('Your github password:')
        self.github = Github(user, passw)

    def projects(self):
        repositories = self.github.get_user().get_repos()
        repos = []
        for repo in repositories:
            if repo.full_name.startswith(self.user):
                repos.append(
                    Project({"name": repo.name,
                             "path": "/tmp/%s" % repo.name,
                             "url": "https://github.com/%s" % repo.full_name}))
        return repos

    def need_to_write_gitsync_file(self):
        return True
