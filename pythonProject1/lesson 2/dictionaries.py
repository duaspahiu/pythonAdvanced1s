wow = {
    "liza" :12000,
    "Rundina" :6000,
    "Lora" :12000,
    "Erona":13000
}

print(puntoret["erona"])

puntoret["liza"]=14000

print(puntoret)


puntoret["donjeta"]=5000

print(puntoret)

del puntoret["rundina"]

print(puntoret)

print(puntoret.keys())
print(puntoret.values())
print(puntoret.items())