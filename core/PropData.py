#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PropData.py
MIT License (c) Marie Faure <dev at faure dot systems>

Class to track changes in variables and to publish them optimally in the props outbox.
"""


class PropData:

    # __________________________________________________________________
    def __init__(self, name, type, initial, decimal=None, precision=1, alias=("1", "0"), logger=None):
        super().__init__()

        self._logger = logger
        self._name = name
        self._type = type
        self._decimal = decimal
        self._precision = precision
        self._true, self._false = alias

        if type == int:
            v = int(str(initial))
            self._value = v
            self._reference = v + 1
            if self._logger:
                self._logger.info(
                    "{0} '{1}' {2}={3} {4}={5}".format("New int Publishable", self._name, "with initial", initial,
                                                       "and precision", self._precision))
        elif type == float:
            v = float(str(initial))
            self._value = v
            self._reference = v + 1.0
            if self._logger and self._decimal:
                self._logger.info(
                    "{0} '{1}' {2}={3} {4}={5} {6}={7}".format("New float Publishable", self._name, "with initial",
                                                               initial, "and precision", self._precision, "and decimal",
                                                               self._decimal))
            elif self._logger:
                self._logger.info(
                    "{0} '{1}' {2}={3} {4}={5}".format("New float Publishable", self._name, "with initial", initial,
                                                       "and precision", self._precision))
        elif type == str:
            self._value = initial
            self._reference = initial + "_"
            if self._logger:
                if initial:
                    self._logger.info(
                        "{0} '{1}' {2}={3}".format("New str Publishable", self._name, "with initial", initial))
                else:
                    self._logger.info("{0} '{1}' {2}=''".format("New str Publishable", self._name, "with initial"))
        elif type == bool:
            self._value = initial
            self._reference = not initial
            if self._logger:
                self._logger.info(
                    "{0} '{1}' ({2}/{3}) {4}={5}".format("New boolean Publishable", self._name, self._true, self._false,
                                                         "with initial", initial))
        else:
            self._type = int
            v = 0
            self._value = v
            self._reference = v + 1
            self._decimal = None
            self._precision = 1
            if self._logger:
                self._logger.info(
                    "{0} '{1}' {2}={3} {4}={5}".format("New incorrect Publishable created as int", self._name,
                                                       "with initial", initial, "and precision", self._precision))

    # __________________________________________________________________
    def __str__(self):
        self._reference = self._value
        if self._type == float and self._decimal:
            return "{0}={1:.{prec}f}".format(self._name, self._value, prec=self._decimal)
        elif self._type == int:
            return "{0}={1}".format(self._name, str(self._value))
        elif self._type == bool:
            if self._value:
                return "{0}={1}".format(self._name, self._true)
            else:
                return "{0}={1}".format(self._name, self._false)
        else:
            if isinstance(self._value, str):
                if not self._value:
                    return "{0}=-".format(self._name)
                else:
                    return "{0}={1}".format(self._name, self._value)
            else:
                try:
                    v = str(self._value)
                    if v:
                        return "{0}={1}".format(self._name, v)
                except:
                    pass
                finally:
                    return "{0}=-".format(self._name)

    # __________________________________________________________________
    def change(self):
        if self._type == int or self._type == float:
            if abs(self._reference - self._value) > self._precision:
                return self.__str__()
            else:
                return None
        else:
            if self._reference != self._value:
                return self.__str__()
            else:
                return None

    # __________________________________________________________________
    def update(self, value):
        self._value = value

    # __________________________________________________________________
    def value(self):
        return self._value
