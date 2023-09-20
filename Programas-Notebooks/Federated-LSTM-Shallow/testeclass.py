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

