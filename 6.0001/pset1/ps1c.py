# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 12:48:45 2021

@author: strou
"""

annual_salary_fixed = float(input('Enter the starting salary: '))
# annual_salary_fixed = 1000000
total_cost = 1000000
semi_annual_raise = .07
portion_down_payment = .25
r=.04
current_savings = 0

high = 1.0
low = 0.0
portion_saved = (high + low) / 2
epsilon = 100
counter = 0

while abs(current_savings - total_cost * portion_down_payment) >= epsilon and portion_saved < 1.0:
    # if counter >= 1:
    #     break
    current_savings = 0
    annual_salary_temp = annual_salary_fixed
    for months in range(36):
        current_savings += annual_salary_temp / 12 * portion_saved + current_savings * r / 12
        if months > 0 and months%6 == 0:
            annual_salary_temp *= 1 + semi_annual_raise
        # print(months, annual_salary_temp) #lol realized annual_salary was ballooning since it never got reset
    # print(counter, portion_saved, current_savings)
    if current_savings < total_cost * portion_down_payment:
        low = portion_saved
    else:
        high = portion_saved
    portion_saved = (high + low) / 2
    counter += 1
if portion_saved < 1.0:
    print('Best savings rate:', round(portion_saved, 4))
    print('Steps in bisection search:', counter)
else:
    print('It is not possible to pay the downpayment in three years.')

        
    
# for months in range(32):
#     current_savings += annual_salary / 12 * portion_saved + current_savings * r / 12
#     if months > 1 and months%6 == 0:
#         annual_salary *= 1 + semi_annual_raise
    

# while current_savings <= total_cost * portion_down_payment:
#     current_savings += annual_salary / 12 * portion_saved + current_savings * r / 12
#     if months > 1 and months%6 == 0:
#         annual_salary *= 1 + semi_annual_raise
#     months += 1

# print('Number of months:', months)

