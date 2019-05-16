#!/usr/bin/env python3.7
# -*- coding: utf-8 -*--

import sys, re, functools
from collections import OrderedDict

class Model:

    def __init__(self):
        self.array = ''
        self.tab = []
        
    def clean_float(self, x):
        return ('%f' % x).rstrip('0').rstrip('.')

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def to_fract(self, numerator):
        denominator = 1
        divisor = self.gcd(numerator, denominator)
        new_numerator, new_denumerator = numerator / divisor, denominator / divisor
        if (new_denumerator == 1):
            return '%d' % (new_numerator)
        return '%d/%d' % (new_numerator, new_denumerator)

    def split(self, regex, array):
        tab = []
        for element in re.finditer(regex, array):
            tab.append(element.group())
        return tab

    def parse(self, params):
        tab = []
        left = True
        for param in params:
            if param == '=':
                left = False
            elif len(param.split('*X^')) == 2:
                tmp = param.split('*X^')
                tab.append([float(tmp[0]) * (-1) if (left == False) else float(tmp[0]) , tmp[1]])
            elif len(param.split('*X')) == 2:
                tmp = param.split('*X')
                tab.append([float(tmp[0]) * (-1) if (left == False) else float(tmp[0]), '1'])
            else:
                tab.append([float(param) * (-1) if (left == False) else float(param), '0'])
        return list(OrderedDict((x[1], x) for x in map(lambda current: functools.reduce(lambda a, c: [a[0] + c[0], current[1]], filter(lambda elt: elt[1] == current[1], tab)), tab)).values())

    def rewrite(self, params):
        tmp = []
        for index, param in enumerate(params):
            if param[0] == 0.0:
                params.pop(index)
        power = int(params[len(params) - 1][1]) if len(params) > 0 else 0
        for i in (i for i in range(0, 3) if power <= 2):
            tmp.append(list(filter(lambda x: x[1] == chr(i + 48), params))[0][0] if list(filter(lambda x: x[1] == chr(i + 48), params)) != [] else 0)
        reduced_form = ''
        for index, element in enumerate(params):
            if index == 0:
                reduced_form += '%s ' % (self.clean_float(float(element[0]))) if element[1] == '0' else '%s*X '% (self.clean_float(float(element[0]))) if element[1] == '1' else '%s*X^%s ' % (self.clean_float(float(element[0])), self.clean_float(float(element[1])))
            elif element[0] < 0:
                reduced_form += '- %s ' % (self.clean_float(float(element[0]) * (-1))) if element[1] == '0' else '- %s*X ' % (self.clean_float(float(element[0]) * (-1))) if element[1] == '1' else '- %s*X^%s ' % (self.clean_float(float(element[0]) * (-1)), self.clean_float(float(element[1])))
            else:
                reduced_form += '+ %s ' % (self.clean_float(float(element[0]))) if element[1] == '0' else '+ %s*X ' % (self.clean_float(float(element[0]))) if element[1] == '1' else '+ %s*X^%s ' % (self.clean_float(float(element[0])), self.clean_float(float(element[1])))
        reduced_form += '= 0' if len(reduced_form) > 0 else '0 = 0'
        return [True, tmp, power, reduced_form]
    
    def resolve(self, leftArray, rightArray):
        self.array = (leftArray + '=' + rightArray).replace(' ', '')
        #améliorer regex pour gestion d'erreur
        self.tab = self.split(r"(-?[0-9]+\.?[0-9]*\*X\^[0-9]+(?![0-9])|=|-?[0-9]+\.?[0-9]*\*X(?!\^)|(?<!X)-?[0-9]+\.?[0-9]*)", self.array)
        if len(self.array) != sum(len(elt) for elt in self.tab) + self.array.count('+'):
            return [False, 'Parameters isn\'t well formated.']
        return self.rewrite(self.parse(self.tab))