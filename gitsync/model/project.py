# -*- coding: utf-8 -*-


class Project(object):

    __allowed_properties = [
        'name',
        'url',
        'path'
    ]

    def __init__(self, project):
        if not sorted(project.keys()) == sorted(self.__allowed_properties):
            return None
        for allowed_property in self.__allowed_properties:
            setattr(self, allowed_property, project[allowed_property])
