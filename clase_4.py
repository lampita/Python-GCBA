frase="gmailco"

# print(frase != "")
# print(len(frase[0:(frase.find("@"))])>=1)
# print("@" in frase)
# print(frase.find("@",(frase.find("@")+1))==-1) 
# print(frase.count("@")<=1)
# print(frase.find(" ")==-1)

mail_nombre=len(frase[0:(frase.find("@"))])
mail_dominio=len(frase[frase.find("@"):frase.rfind(".")])
mail_extension= len(frase)-frase.rfind(".")

print("True") if mail_nombre >=1 else print("False")
print("True") if mail_dominio >=3 else print("False")
print("True") if mail_extension== 4 or  mail_extension== 3  else print("False")



# Formatee correctamente los textos ingresados en “apellido” y “nombre”, convirtiendo la primera letra de cada palabra a mayúsculas y el resto en minúsculas.

# Asegurarse que el correo electrónico no tenga espacios y contenga solo una “@”.

# Que clasifique por rango etario basándose en su edad (“Niño/a” para los menores de 15 años, “Adolescente” de 15 a 18 y “Adulto/a” para los mayores de 18 años.)
