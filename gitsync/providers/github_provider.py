# -*- coding: utf-8 -*-
from github import Github
from gitsync.model.project import Project
from gitsync.provider import Provider


class GithubProvider(Provider):

    def __init__(self, user, password, working_directory):
        super(Provider, self).__init__()
        self.user = user
        self.github = Github(self.user, password)
        self.working_directory = working_directory

    def projects(self):
        repositories = self.github.get_user().get_repos()
        repos = []
        for repo in repositories:
            if repo.full_name.startswith(self.user):
                repos.append(
                    Project({"name": repo.name,
                             "path": "%s/%s" % (self.working_directory, repo.name),
                             "url": "https://github.com/%s" % repo.full_name}))
        return repos

    def need_to_write_gitsync_file(self):
        return True
