import sys
import re
from collections import OrderedDict

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
    if power <= 2:
        tmp.append(filter(lambda x: x[1] == '0', params)[0][0] if filter(lambda x: x[1] == '0', params) != [] else 0)
        tmp.append(filter(lambda x: x[1] == '1', params)[0][0] if filter(lambda x: x[1] == '1', params) != [] else 0)
        tmp.append(filter(lambda x: x[1] == '2', params)[0][0] if filter(lambda x: x[1] == '2', params) != [] else 0)
    reduced_form = ''
    for index, element in enumerate(params):
        if index == 0:
            reduced_form += '{coeff}*X^{power} '.format(coeff = element[0], power = element[1])
        elif element[0] < 0:
            reduced_form += '- {coeff}*X^{power} '.format(coeff = element[0] * (-1), power = element[1])
        else:
            reduced_form += '+ {coeff}*X^{power} '.format(coeff = element[0], power = element[1])
    reduced_form += '= 0' if len(reduced_form) > 0 else '0 = 0'
    return [tmp, power, reduced_form]

def result(params):
    result = 'Reduced form: {reduced_form}\nPolynomial degree: {degree}\n'.format(reduced_form = params[2], degree = params[1])
    if params[1] <= 2:
        a = float(params[0][2])
        b = float(params[0][1])
        c = float(params[0][0])
        if params[1] == 0:
            result += 'All real number are solution' if c == 0 else 'There is no solution'
        elif params[1] == 1:
            result += 'The solution is:\n0' if c == 0 else 'The solution is:\n{only_solution}'.format(only_solution = (-1 * c / b))
        else:
            delta = (b * b) - (4 * a * c)
            if delta > 0:
                first_solution = ((-1 * b) + (delta ** (.5))) / (2 * a)
                second_solution = ((-1 * b) - (delta ** (.5))) / (2 * a)
                result += 'Discriminant is strictly positive, the two solutions are:\n{first_solution}\n{second_solution}'.format(first_solution = first_solution, second_solution = second_solution)
            elif delta == 0:
                only_solution = (-1 * b) / a
                result += 'The solution is:\n{only_solution}'.format(only_solution = only_solution)
            else:
                result += 'Discriminant is stricly negative, no real solution.'
    else:
        result += 'The polynomial degree is stricly greater than 2, I can\'t solve.'
    print result

res = split(r"(-?[.0-9]+\*X\^[0-9]+(?![0-9])|=|-?[0-9.]+\*X(?!\^)|-?[0-9.]+)", sys.argv[1].replace(' ', ''))
result(rewrite(parse(res)))