class Employee:
    def __init__(self,code,name,age,salary):
        self.code = code
        self.name = name
        self.age = age
        self.salary = salary
    def income(self):
        result = 0.9*12*self.salary 
        return result
    def increaseSalary(self,amount):
        if amount > 0:
            self.salary = self.salary+ amount
    def display(self):
        print(f'code: {self.code}, name: {self.name}, age: {self.age}, salary: {self.salary}, income: {self.income()}\n')