mail=""

# print(frase != "")
# print(len(frase[0:(frase.find("@"))])>=1)
# print("@" in frase)
# print(frase.find("@",(frase.find("@")+1))==-1) 
# print(frase.count("@")<=1)
# print(frase.find(" ")==-1)


def check_mail(mail):
    mail_nombre=len(mail[0:(mail.find("@"))])
    mail_dominio=len(mail[mail.find("@"):mail.rfind(".")])
    mail_extension= len(mail)-mail.rfind(".")

    comprobacion_1= True if mail_nombre >=1 else False
    comprobacion_2= True if mail_dominio >=3 else False
    comprobacion_3= True if mail_extension== 4 or  mail_extension== 3  else False
    
    if comprobacion_1 and comprobacion_2 and comprobacion_3:
         return True
    else: 
        return False

print(check_mail(mail))



# Formatee correctamente los textos ingresados en “apellido” y “nombre”, convirtiendo la primera letra de cada palabra a mayúsculas y el resto en minúsculas.

# Asegurarse que el correo electrónico no tenga espacios y contenga solo una “@”.

# Que clasifique por rango etario basándose en su edad (“Niño/a” para los menores de 15 años, “Adolescente” de 15 a 18 y “Adulto/a” para los mayores de 18 años.)
