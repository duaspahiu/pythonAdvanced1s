import datetime

from pythonProject1.mypackage.moduli1 import hello

tani = datetime.datetime.now()

print(tani)

print(tani.year , "hello")
print(tani.month)
print(tani.day)
print(tani.hour)
print(tani.minute)
print(tani.second)
print(tani.microsecound)

eventi = datetime.date(2025,2,5)

print(f"eventi mbahet ne mujine {eventi.month}, dhe ne diten {eventi.day}")
