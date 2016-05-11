# -*- coding: utf-8 -*-
import os
import yaml

from gitsync.model.project import Project
from gitsync.provider import Provider


GITSYNC_FILE = "git-sync.yml"


class Loader(yaml.Loader):

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


class FileProvider(Provider):

    def __init__(self):
        super(Provider, self).__init__()
        self.project_file = GITSYNC_FILE
        Loader.add_constructor('!include', Loader.include)

    def _read_projects_from_yaml(self):
        file_handler = os.path.join(os.curdir, self.project_file)
        projects = []
        try:
            with open(file_handler) as json_file:
                raw_projects = yaml.load(json_file, Loader)
        except Exception:
            raise Exception("Invalid yaml file...")

        for raw_project in raw_projects:
            if raw_project.get('projects'):
                projects.extend(raw_project['projects'])
            elif raw_project.get('projects_files'):
                projects.extend(raw_project['projects_files'])
            else:
                projects.append(raw_project)

        return projects

    def projects(self):
        yaml_projects = self._read_projects_from_yaml()
        return list(map(lambda yaml_project: Project(yaml_project),
                        yaml_projects))

    def need_to_write_gitsync_file(self):
        return False
