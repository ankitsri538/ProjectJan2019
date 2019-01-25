# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 09:08:33 2019

@author: ankit
"""
myUniqueList=[1,2,3]
myLeftovers=[2,3]

def addtolist(item):
    if item in myUniqueList:
        myLeftovers.append(item)
        print("False")
    else:
        myUniqueList.append(item)
        print("True")
    

addtolist(5)
addtolist(5)

print(myUniqueList)
print(myLeftovers)


