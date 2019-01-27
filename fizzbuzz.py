# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 13:40:56 2019

@author: ankit
"""

def testprime(n):
    reply=0
    for j in range(2,n):
        if n%j==0:
            reply=1
            break
    return(reply)

for i in range(1,101):
    if i%3==0 and i%5==0:
        print("fizzbuzz")
        continue
    elif i%3==0:
        print("fizz")
        continue
    elif i%5==0:
        print("buzz")
        continue
    elif(testprime(i)==0 and i>1):
        print("prime")
        continue
    else:
        print(i)
       
            
     