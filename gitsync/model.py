class Project(object):

    __allowed_properties = [
        'name',
        'url',
        'path'
    ]

    def __new__(cls, project):
        if not sorted(project.keys()) == sorted(cls.__allowed_properties):
            return None
        for allowed_property in cls.__allowed_properties:
            setattr(cls, allowed_property, project[allowed_property])

        return cls
