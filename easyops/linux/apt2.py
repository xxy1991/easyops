#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-02-01 23:59
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

from typing import List, Set, Callable


class SourceConfigItem(object):
    def __init__(self, os: str, item):
        self.__os = os
        self.__item = item

    @property
    def name(self) -> str:
        return self.__item['name']

    @property
    def scheme(self) -> List[str]:
        if 'scheme' in self.__item:
            return self.__item['scheme']
        return ['http']

    @property
    def host(self) -> str:
        return self.__item['host']

    @property
    def location(self) -> str or None:
        if 'location' in self.__item:
            return self.__item['location']
        return None

    @property
    def is_location_default(self) -> bool:
        if 'location-default' in self.__item:
            return self.__item['location-default']
        return False

    @property
    def os(self) -> str:
        return self.__os

    @property
    def is_default(self) -> bool:
        if 'default' in self.__item:
            return self.__item['default']
        return False

    def __repr__(self) -> str:
        return repr(dict(
            name=self.name,
            scheme=self.scheme,
            host=self.host,
            location=self.location,
            location_default=self.is_location_default,
            os=self.os,
            default=self.is_default
        ))


class SourceConfigSet(object):
    def __init__(self, data):
        self.__set = set()
        for os in data:
            for item in data[os]:
                config = SourceConfigItem(os, item)
                self.__set.add(config)

    def get_by_name(self, os: str, name: str) -> SourceConfigItem or None:
        result = set(filter(lambda item: item.name == name, self.get_by_os(os)))
        if len(result) > 0:
            return result.pop()
        result = set(filter(lambda item: item.name == name, self.__set))
        if len(result) > 0:
            return result.pop()
        return None

    @staticmethod
    def filter(filter_func: Callable[[SourceConfigItem], bool], configs: set) -> Set[SourceConfigItem]:
        return set(filter(filter_func, configs))

    @staticmethod
    def filter_by_scheme(scheme: Callable[[List[str]], bool] or None, configs: set) -> Set[SourceConfigItem]:
        if scheme is None:
            return configs
        return set(filter(lambda item: scheme(item.scheme), configs))

    def get_by_os(self, os: str) -> Set[SourceConfigItem]:
        return self.filter(lambda item: item.os == os, self.__set)

    def get_by_location(self, location: str) -> Set[SourceConfigItem]:
        return self.filter(lambda item: item.location == location, self.__set)

    def get_by_default(self, os, location=None, scheme=None) -> SourceConfigItem or None:
        result = self.get_by_os(os)

        if location is not None:
            result = set(result).intersection(self.get_by_location(location))
            result = set(filter(lambda item: item.is_location_default, result))
        if scheme is not None:
            result = set(filter(lambda item: scheme(item.scheme), result))
        return result

    def get_mirror(self, os='common', name=None, location=None, scheme=None) -> SourceConfigItem or None:
        # priority level
        # name-os > name >
        # os-location-default > os-default >
        # common-location-default > common-default
        if name is not None:
            config = self.get_by_name(os, name)
            if scheme is not None and scheme(config.scheme):
                return config

        os_set = self.get_by_os(os)
        loc_set = self.get_by_location(location)
        result = self.filter_by_scheme(scheme, os_set.intersection(loc_set))
        if len(result) > 0:
            configs = set(self.filter(lambda item: item.is_location_default, result))
            if len(configs) > 0:
                return result.pop()
            return result.pop()

        result = self.filter_by_scheme(scheme, set(self.filter(lambda item: item.is_default, os_set)))
        if len(result) > 0:
            return result.pop()

        if os != 'common':
            return self.get_mirror(location=location, scheme=scheme)

        return None
