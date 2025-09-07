import os

valid_mail = False
valid_edad = False
valid_ingresos = False
total_ingresos = 0


def check_mail(mail):
    mail_nombre = len(mail[0 : (mail.find("@"))])
    mail_dominio = len(mail[mail.find("@") : mail.rfind(".")])
    mail_extension = len(mail) - mail.rfind(".")

    comprobacion_1 = True if mail_nombre >= 1 else False
    comprobacion_2 = True if mail_dominio >= 3 else False
    comprobacion_3 = True if mail_extension == 4 or mail_extension == 3 else False

    if comprobacion_1 and comprobacion_2 and comprobacion_3:
        return True
    else:
        print("El mail ingresado no es válido. Intente nuevamente.")
        return False


def check_edad(edad):
    if edad.isdigit() and int(edad) > 0 and int(edad) < 120:
        return True
    else:
        print("La edad ingresada no es válida. Intente nuevamente.")
        return False

def check_ingresos(ingresos):
    if ingresos.isdigit() and int(ingresos) > 0:
        return True
    else:
        print("Dato ingresado no válido. Intente nuevamente.")
        return False



def borrar_consola(bread_crumb):
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    print(f"\t{'=' * 21}\n\t\033[1;91mVALIDACION  DE  DATOS\033[0m\n\t{'=' * 21}")
    match bread_crumb:
        case 1:
            print("Nombre - Apellido - Edad - Mail - Ingresos\n")
        case 2:
            print("Nombre \x1b[1;32m\u2714\x1b[0m - Apellido - Edad - Mail  -  Ingresos\n")
        case 3:
            print(
                "Nombre \x1b[1;32m\u2714\x1b[0m - Apellido \x1b[1;32m\u2714\x1b[0m - Edad - Mail - Ingresos\n"
            )
        case 4:
            print(
                "Nombre \x1b[1;32m\u2714\x1b[0m - Apellido \x1b[1;32m\u2714\x1b[0m - Edad \x1b[1;32m\u2714\x1b[0m - Mail - Ingresos\n"
            )
        case 5:
            print(
                "Nombre \x1b[1;32m\u2714\x1b[0m - Apellido \x1b[1;32m\u2714\x1b[0m - Edad \x1b[1;32m\u2714\x1b[0m - Mail \x1b[1;32m\u2714\x1b[0m - Ingresos\n"
            )
        case 6:
            print("Nombre \x1b[1;32m\u2714\x1b[0m - Apellido \x1b[1;32m\u2714\x1b[0m - Edad \x1b[1;32m\u2714\x1b[0m - Mail \x1b[1;32m\u2714\x1b[0m - Ingresos \x1b[1;32m\u2714\x1b[0m\n")
            print("\nTodos los datos han sido validados correctamente. \x1b[1;32m\u2714\x1b[0m\n")


borrar_consola(1)

nombre = input("Ingrese su nombre: ").capitalize().strip()
borrar_consola(2)
apellido = input("Ingrese su apellido: ").capitalize().strip()
borrar_consola(3)
while not valid_edad:
    edad = input("Ingrese su edad: ")
    valid_edad = check_edad(edad)
borrar_consola(4)
while not valid_mail:
    mail = input("ingrese su mail: ")
    valid_mail = check_mail(mail)
borrar_consola(5)

for i in range(6):
    while not valid_ingresos:
        ingresos = input(f"Ingresos del mes {i+1}: ")
        valid_ingresos = check_ingresos(ingresos)
    total_ingresos += int(ingresos)
    valid_ingresos = False
    
borrar_consola(6)

estado = ""
if int(edad) < 15:
    estado = "Niño/a"
elif int(edad) <= 18:
    estado = "Adolescente"
else:
    estado = "Adulto/a"

print("=" * 40)
print(f"""\x1b[1mDATOS INGRESADOS:\x1b[0m
\x1b[1mNombre:\x1b[0m {nombre}
\x1b[1mApellido:\x1b[0m {apellido}
\x1b[1mEdad:\x1b[0m {edad}
\x1b[1mMail:\x1b[0m {mail}
\x1b[1mEstado de mayoría:\x1b[0m {estado}
\x1b[1mTotal de ingresos:\x1b[0m ${total_ingresos}""")
print("=" * 40)
print('\n\n\n\n')
