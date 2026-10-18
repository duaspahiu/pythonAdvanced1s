import pandas as pd

produktet =["molla","banana","protokaj","Rrushi"]

seles = [150,200,100,90]

seles_Series = pd.series(seles,index=produktet)

print(seles_Series)

print(seles_Series["molla"])

shitjeTotale = seles_Series.sum()

print(shitjeTotale)

shitjeMatErdhe = seles_Series.idxmax()

print(f"shitje me se shumti ka pasur :{shitjeMatErdhe}")