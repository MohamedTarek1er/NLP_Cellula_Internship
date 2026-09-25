# class Food:
#     def __init__(self,name,price):
#         self.name=name
#         self.price=price
#         print("Food class constructor called")

#     def eat(self):
#         print("Eating food")


# class Apple (Food):
#     def __init__(self,name,price):
        
#         super().__init__(name,price)
#         print(f"{self.name} is created from Derived class")

#     def eat(self):
#         print(f"earting in derived class")

# fod=Apple("banaana",10)
# fod.eat()

# class base_one:
#     def __init__(self):
#         print("base one")


# class base_two:
#     def __init__(self):
#         print("base two")


# class member(base_one, base_two):
#     pass


# m=member()
# print(m.mro())


# class member:
#     def __init__(self,name):
#         self.__name = name

#     def say_hello(self):
#         print(f"hello {self.__name}")

# mem=member("ahmed")
# print(mem._member__name)






# class member:
#     def __init__(self,name):
#         self.__name = name


#     def get_name(self):
#         return self.__name

#     def set_name(self,name):
#         self.__name=name


# mem=member("ahmed")
# print(mem.get_name())
# mem.set_name("mohamed")
# print(mem.get_name())



# class member:
#     def __init__(self,name, age):
#         self.__name = name
#         self.__age = age

#     @property
#     def say_hello(self):
#         print(f"hello {self.__name} your age is {self.__age}")



# mem=member("ahmed", 20)
# mem.say_hello
    


# from abc import ABCMeta, abstractmethod
# class programming(metaclass=ABCMeta):

#     @abstractmethod
#     def has_oop():
#         pass 

# class python(programming): 
#     pass
#     # def has_oop(self): 
#     #     print("yes python has oop")

# mem=python() 
# mem.has_oop()
