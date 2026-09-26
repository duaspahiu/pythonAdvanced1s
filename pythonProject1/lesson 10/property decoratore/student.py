
class stundet:
    def __init__(self,name,age):
        self.__name = name
        self.__age= age

        @property
        def name(self):
            return self.__name

        @name.setter
        def name(self):
            return self.__age

        @age.setter
        def age(self,age):
            self.__age = age

stundet1 = stundet("donjeta",18)

print(Stundenti1.name)

print(stundet1.age)

stundet1.age = 255

print(stundet1.age)