#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/25 16:45
"""

class TestA:

    name = None

    age = 11

    def show(self):
        print(self.name)
        print(self.age)


a = TestA()
a.name = "cesh"
a.show()