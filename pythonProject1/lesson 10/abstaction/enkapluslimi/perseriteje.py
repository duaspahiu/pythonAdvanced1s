class Mausi:

    def __init__(self, emri,ngjyra,pesha):
        self.emri=emri
        self.ngjyra=ngjyra
        self.pesha=pesha


    def rightClick(sel):
     print("eshte klikuar butoni i djatht")


    def leftClick(sel):
     print("eshte klikuar butoni i majt")



class MausiUsb(Mausi):
    def __init__(self, emri, ngjyra,pesha,usbPort):
        super().__init__(emri,ngjyra,pesha)
        self.usbPort = usbPort

    def coonectPort(self):
        print("usb port is connected to the pc ")


mausiMeUsb = MausiUsb("lenovo","ebardhe","25g","yes")

mausiMeUsb.leftClick(