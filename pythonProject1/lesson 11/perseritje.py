"""file = open("example.txt",r")

content = file.read()

print(content)

file.close()


"""
import os
with open("emample2.txt","r") as file:
    content = file.read()
    print(content)

#with open("example2.txt","w") as file:
  # file.write("hello blinkpinkja")

with open("Example2.txt","a") as file:
    file.write("\nhello blinkpinkja")


if os.path.exists("gg.txt"):
    print("file ekziston")
else:
    print("fili nuk ekziston")