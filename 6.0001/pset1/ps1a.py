# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 12:48:45 2021

@author: strou
"""

annual_salary = float(input('Enter your annual salary: '))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
total_cost = float(input('Enter the cost of your dream home: '))

current_savings = 0
portion_down_payment = .25
r=.04
months = 0

while current_savings <= total_cost * portion_down_payment:
    current_savings += annual_salary / 12 * portion_saved + current_savings * r / 12
    months += 1

print('Number of months:', months)