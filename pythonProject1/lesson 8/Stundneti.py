class studenti:

    def __init__(self ,name,age, parentName, nivelin,pages):
        self.name=name
        self.age=age
        self.parentName=parentName
        self.nivelin=nivelin
        self.pagesa=pagesa

    def vjenNe0re(self):
        print( self.name+"ka marr pjes ne ore")


    def projektiPersonal(self):
        print("projketi final eshte i perfunder")

    def kryerjaEpagese(self):
        print(self.pagesa)

    def kryerjaEpagesa(self):
        self.pagesa=self.pagesa-40