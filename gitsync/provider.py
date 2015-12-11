# -*- coding: utf-8 -*-
from abc import ABCMeta
import abc


class Provider(object):
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def projects(self):
        pass

    @abc.abstractproperty
    def need_to_write_gitsync_file(self):
        pass
