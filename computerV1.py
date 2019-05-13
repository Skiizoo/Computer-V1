#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys, re
from collections import OrderedDict

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def to_Frac(numerator):
    denominator = 1
    divisor = gcd(numerator, denominator)
    new_numerator, new_denumerator = numerator / divisor, denominator / divisor
    if (new_denumerator == 1):
        return '%d' % (new_numerator)
    return '%d/%d' % (new_numerator, new_denumerator)

def split(regex, array):
    tab = []
    for element in re.finditer(regex, array):
        tab.append(element.group())
    return tab

def parse(params):
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
    return list(OrderedDict((x[1], x) for x in map(lambda current: reduce(lambda a, c: [a[0] + c[0], current[1]], filter(lambda elt: elt[1] == current[1], tab)), tab)).values())

def rewrite(params):
    tmp = []
    for index, param in enumerate(params):
        if param[0] == 0.0:
            params.pop(index)
    power = int(params[len(params) - 1][1]) if len(params) > 0 else 0
    for i in (i for i in range(0, 3) if power <= 2):
        tmp.append(filter(lambda x: x[1] == chr(i + 48), params)[0][0] if filter(lambda x: x[1] == chr(i + 48), params) != [] else 0)
    reduced_form = ''
    for index, element in enumerate(params):
        if index == 0:
            reduced_form += '%s ' % (element[0]) if element[1] == '0' else '%s*X '% (element[0]) if element[1] == '1' else '%s*X^%s ' % (element[0], element[1])
        elif element[0] < 0:
            reduced_form += '- %s ' % (element[0] * (-1)) if element[1] == '0' else '- %s*X ' % (element[0] * (-1)) if element[1] == '1' else '- %s*X^%s ' % (element[0] * (-1), element[1])
        else:
            reduced_form += '+ %s ' % (element[0]) if element[1] == '0' else '+ %s*X ' % (element[0]) if element[1] == '1' else '+ %s*X^%s ' % (element[0], element[1])
    reduced_form += '= 0' if len(reduced_form) > 0 else '0 = 0'
    return [tmp, power, reduced_form]

def result(params):
    result = '\x1b[1;30;40mReduced form: \x1b[0m c + b*X + a*X^2 = 0 --> \x1b[0;32;40m%s\x1b[0m\n\x1b[1;30;40mPolynomial degree: \x1b[0m \x1b[0;32;40m%s\x1b[0m \n' % (params[2], params[1])
    if params[1] <= 2:
        a, b, c = float(params[0][2]), float(params[0][1]), float(params[0][0])
        if params[1] == 0:
            result += '\x1b[0;32;40mAll real number are solution\x1b[0m' if c == 0 else '\x1b[0;31;40mThere is no solution\x1b[0m'
        elif params[1] == 1:
            result += '\x1b[1;30;40mThe solution is:\x1b[0m\nx1 = \x1b[0;32;40m0\x1b[0m' if c == 0 else '\x1b[1;30;40mThe solution is:\x1b[0m\nx1 = -c/b --> \x1b[0;32;40m%s\x1b[0m' % (to_Frac(-1 * c / b))
        else:
            delta = (b * b) - (4 * a * c)
            result += '\x1b[1;30;40mDiscriminant: \x1b[0m b^2 - 4ac --> %s^2 - 4*%s*%s --> \x1b[0;32;40m%s\x1b[0m' % (b, a, c, delta)
            if delta > 0:
                first_solution, second_solution = ((-1 * b) + (delta ** (.5))) / (2 * a), ((-1 * b) - (delta ** (.5))) / (2 * a)
                result += ' > 0\n\x1b[1;30;40mThe two solutions are:\x1b[0m\nx1 = (-b + √Δ)/2a --> (-%s + √%s)/2*%s --> \x1b[0;32;40m%s\x1b[0m \nx2 = (-b - √Δ/2a --> (-%s - √%s)/2*%s --> \x1b[0;32;40m%s\x1b[0m' % (b, delta, a, to_Frac(round(first_solution, 6)), b, delta, a, to_Frac(round(second_solution, 6)))
            elif delta == 0:
                result += ' = 0\n\x1b[1;30;40mThe solution is:\x1b[0m\nx1 = -b/a --> -%s/%s --> \x1b[0;32;40m%s\x1b[0m' % (b, a, to_Frac(-1 * b / a))
            else:
                result += ' < 0\n\x1b[1;30;40mThe two solutions are:\x1b[0m\nx1 = (-b + i√Δ)/2a --> \x1b[0;32;40m(-%s + i√%s)/%s\x1b[0m \nx2 = (-b - i√Δ/2a --> \x1b[0;32;40m(-%s - i√%s)/%s\x1b[0m' % (b, delta if delta > 0 else delta * (-1), 2 * a, b, delta if delta > 0 else delta * (-1), 2 * a)
    else:
        result += 'The polynomial degree is stricly greater than 2, \x1b[0;31;40mI can\'t solve.\x1b[0m'
    print result

def initialize():
    if len(sys.argv) != 2:
        sys.exit('\x1b[0;31;40mUsage: python computerV1.py [1 parameters].\x1b[0m')
    else:
        array = sys.argv[1].replace(' ', '')
        res = split(r"(-?[0-9]+\.?[0-9]*\*X\^[0-9]+(?![0-9])|=|-?[0-9]+\.?[0-9]*\*X(?!\^)|(?<!X)-?[0-9]+\.?[0-9]*)", array)
        if len(array) != sum(len(elt) for elt in res) + array.count('+'):
            sys.exit('\x1b[0;31;40mParameters isn\'t well formated.\x1b[0m')
        result(rewrite(parse(res)))

initialize()

#HANDLING PARSING ERRORS (regex)
#DETAILS                                @done
#FRACTIONS                              @done
#IRREELS                                @done
#COLOR                                  @done