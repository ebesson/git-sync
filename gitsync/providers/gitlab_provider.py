# -*- coding: utf-8 -*-
import gitlab

from gitsync.model.project import Project
from gitsync.provider import Provider


class GitlabProvider(Provider):

    def __init__(self, url, token, working_directory):
        super(Provider, self).__init__()
        self.gitlab = gitlab.Gitlab(url=url, private_token=token)
        self.working_directory = working_directory

    def projects(self):
        projects = []
        for project in self.gitlab.projects.list(owned=True):
            projects.append(Project(
                {"name": "%s" % project.attributes['path'],
                 "url": project.attributes['http_url_to_repo'],
                 "path": "%s/%s" % (self.working_directory, project.attributes['path'])}))

        return projects

    def need_to_write_gitsync_file(self):
        return True
