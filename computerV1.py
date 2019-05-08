import sys
import re

def atoi(s):
	n, notnegative = 0, 1
	if s[0]=="-":
		notnegative = -1
		s = s[1:]
	for i in s:
		n = n*10 + ord(i)-ord("0")
	return notnegative*n

def split(regex, array):
    tab = []
    for element in re.finditer(regex, array):
        tab.append(element.group())
    return tab

def getCoeff(tab):
    left = True
    coeff = 0
    for element in tab:
        if element != '=':
            if left:
                coeff += atoi(element.split('*')[0])
            else:
                coeff -= atoi(element.split('*')[0])
        else:
            left = False
    return coeff

def organize(power_zero, power_one, other_power):
    coeff = []
    degree = 0
    new = ''
    if getCoeff(power_zero) != 0:
        new += str(getCoeff(power_zero)) + ' * X^0'
        coeff.append(getCoeff(power_zero))
    else:
        coeff.append('')
    for number in range(0, 99):
        if len(other_power[number]) > 1:
            tmp = getCoeff(other_power[number])
            if tmp < 0:
                if number == 0 or number == 1:
                    coeff.append(tmp)
                degree = number + 1
                new += ' - {tmp} * X^{number}'.format(tmp = (tmp * -1), number = number + 1)
            elif tmp > 0:
                if number == 0 or number == 1:
                    coeff.append(tmp)
                degree = number + 1
                new += ' + {tmp} * X^{number}'.format(tmp = tmp, number = number + 1)
            else:
                if number == 0 or number == 1:
                    coeff.append('')
        else:
            if number == 0 or number == 1:
                coeff.append('')
    new += ' = 0'
    return [degree, coeff, new]

def result(organize):
    result = 'Reduced form: {reduced_form}\nPolynomial degree: {degree}\n'.format(reduced_form = organize[2], degree = organize[0])
    if organize[0] in [0, 1 ,2]:
        b = float(organize[1][1])
        c = float(organize[1][0])
        if organize[0] == 0:
            if c == '':
                organize[2] = '0 = 0'
                result += 'All real number are solution'
            else:
                result += 'There is no solution'
        elif organize[0] == 1:
            if c == '':
                result += 'The solution is:\n0'
            else:
                only_solution = (-1 * c / b)
                result += 'The solution is:\n{only_solution}'.format(only_solution = only_solution)
        else:
            a = float(organize[1][2])
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

res = split(r"(-?[.0-9]+\*X\^[0-9]+(?![0-9])|=|-?[0-9.]+\*X(?!\^)|-?[0-9.]+)", sys.argv[1].replace(' ', ''))
print(res)

#organize = organize(split(r"(-?[.0-9]+\*X\^0|(?<![\^0-9])-?[.0-9]+(?![*.0-9])|=)", array), split(r"(-?[.0-9]+\*X\^1(?![0-9])|-?[.0-9]+\*X(?!\^)|=)", array), autoSplit(array))

#print(result)

#2*X^0+4*X^1-1.56*X^2=-1+7*X^1-468576*X

#5.5555*X^0+4*X^1+9.9*X^0=5.9+1*X^53+9.9

#0.564684*X = 2154*X + 2.14*X^1

#5*X^0+4*X^1=4*X^0+8*X

#4.8*X^0-6*X^1+0.9*X^2-5.6*X^3=3.3*X^2

#5*X^0+4*X^1-9.3*X^2=1*X^101+4-5*X

#(-?[.0-9]+\*X\^0|(?<![\^0-9])-?[.0-9]+(?![*.0-9])|=)