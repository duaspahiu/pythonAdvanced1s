class Person:
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height

    def greet(self):
        print(f"Përshëndetje, unë jam {self.name}!")

    def bmi(self):
        return self.weight / self.height ** 2

    def bmi_category(self):
        b = self.bmi()
        if b < 18.5:
            return "Nën peshë"
        elif b < 25:
            return "Peshë normale"
        elif b < 30:
            return "Mbi peshë"
        else:
            return "Obez"

    def birthday(self):
        self.age += 1
        print(f"Gëzuar ditëlindjen, {self.name}! Tani je {self.age} vjeç.")

    def __str__(self):
        return f"{self.name}, {self.age} vjeç, {self.weight} kg, {self.height} m"


p = Person("blinkpinkja", 29, 49, 1.89)
p.greet()
print(p)
print(f"BMI: {p.bmi():.2f} ({p.bmi_category()})")
p.birthday()

low, high = p.ideal_weight_range()
print(f"Pesha e shëndetshme për gjatësinë tënde: {low:.1f} - {high:.1f} kg")
print("I rritur?", p.is_adult())

p.birthday()

class Child(Person):
    def __init__(self, name, age, weight, height, parent_name, school):
        super().__init__(name, age, weight, height)
        self.parent_name = parent_name
        self.school = school

    def greet(self):
        print(f"Tungjatjeta! Unë jam {self.name} dhe shkoj në {self.school}.")

    def __str__(self):
        return f"{super().__str__()}, prindi: {self.parent_name}, shkolla: {self.school}"


p = Person("blinkpinkja", 29, 49, 1.89)
c = Child("Ari", 10, 32, 1.40, "blinkpinkja", "Shkolla Fillore")

p.greet()
c.greet()               # versioni i ri i Child
print(c)
print("I rritur?", c.is_adult())   # False, e trashëguar nga Person
print(f"BMI: {c.bmi():.2f}")       # e trashëguar nga Person
c.birthday()            # e trashëguar nga Person