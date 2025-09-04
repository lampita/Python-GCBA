valid_mail = False
valid_edad = False


def check_mail(mail):
    mail_nombre = len(mail[0 : (mail.find("@"))])
    mail_dominio = len(mail[mail.find("@") : mail.rfind(".")])
    mail_extension = len(mail) - mail.rfind(".")

    comprobacion_1 = True if mail_nombre >= 1 else False
    comprobacion_2 = True if mail_dominio >= 3 else False
    comprobacion_3 = True if mail_extension == 4 or mail_extension == 3 else False

    if comprobacion_1 and comprobacion_2 and comprobacion_3:
        print("mail correcto")
        return True
    else:
        print("mail incorrecto")
        return False


def check_edad(edad):
    if edad.isdigit():
        print("edad correcta")
        return True
    else:
        print("edad incorrecta")
        return False


nombre = input("Ingrese su nombre: ").capitalize()
apellido = input("Ingrese su apellido: ").capitalize()

while not valid_edad:
    edad = input("Ingrese su edad: ")
    valid_edad = check_edad(edad)

while not valid_mail:
    mail = input("ingrese su mail: ")
    valid_mail = check_mail(mail)

estado = ""
if int(edad) < 15:
    estado = "Niño/a"
elif int(edad) <= 18:
    estado = "Adolescente"
else:
    estado = "Adulto/a"

print(nombre, apellido, edad, mail, estado)
