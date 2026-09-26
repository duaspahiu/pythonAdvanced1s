from abc import  ABC, abstractmethod

class Animal(ABC):

    @abstractmethod
    def make_sound(self):
        pass


class Cat(Animal):

    def make_sound(self):
        print("mauuuu mauuuu")