# -*- coding: utf-8 -*-
from gitsync.model.project import Project
from gitsync.provider import Provider
from gitsync.tuleap import Tuleap


class TuleapProvider(Provider):

    def __init__(self, host, user, password, project, working_directory):
        super(Provider, self).__init__()
        self.tuleap = Tuleap(host=host,
                             port=None,
                             protocol='https://',
                             context=None,
                             username=user,
                             password=password)
        self.tuleap_host = host
        self.project = project
        self.working_directory = working_directory

    def _get_projects(self):
        return self.tuleap.get_projects()

    def _get_repositories_for_projects(self, id):
        return self.tuleap.get_repositories_for_projects(id)

    def projects(self):
        projects = []
        white_list = [self.project]
        for tuealp_project in self._get_projects():
            if tuealp_project.shortname in white_list:
                for repository in self._get_repositories_for_projects(tuealp_project.id):
                    project = Project(
                        {"name": "%s/%s" % (tuealp_project.shortname, repository.name),
                         "url": "ssh://gitolite@%s/%s" % (self.tuleap_host, repository.path),
                         "path": "%s/%s/%s" % (self.working_directory, tuealp_project.shortname, repository.name)})
                    projects.append(project)

        return projects

    def need_to_write_gitsync_file(self):
        return True
