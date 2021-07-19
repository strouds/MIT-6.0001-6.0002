# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 12:48:45 2021

@author: strou
"""

annual_salary = float(input('Enter your annual salary: '))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
total_cost = float(input('Enter the cost of your dream home: '))
semi_annual_raise = float(input('Enter the semi­annual raise, as a decimal: '))

current_savings = 0
portion_down_payment = .25
r=.04
months = 0

while current_savings <= total_cost * portion_down_payment:
    current_savings += annual_salary / 12 * portion_saved + current_savings * r / 12
    if months > 1 and months%6 == 0:
        annual_salary *= 1 + semi_annual_raise
    months += 1

print('Number of months:', months)