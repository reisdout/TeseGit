# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 16:37:26 2023

@author: visitante
"""

class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname() 


class Student(Person):
    def __init__(self, fname, lname):
      Person.__init__(self, fname, lname)  # parece que chama o construtor da pai 


x = Student("Mike", "Olsen")
x.printname() 


# importing pandas as pd
import pandas as pd
  
# Creating the dataframe
df = pd.DataFrame({"A":[12, 4, 5, 44, 1],
                "B":[5, 2, 54, 3, 2],
                "C":[20, 16, 7, 3, 8],
                "D":[14, 3, 17, 2, 6]})
  
# Print the dataframe
print (df)
df_mean = df.mean(axis = 0)
print(df_mean)

print(df_mean['A'])

