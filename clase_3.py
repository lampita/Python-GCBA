import os, time


error="\033[31m ERROR! \033[0m"
error_vacio="(campo vacio) 👎"
error_menor="(menor de 18 anos) 👎"
valido=True

def espera(puntos, tiempo):
    print("\nwait", end=" ", flush=True)
    while puntos >=0:
        
        print(".", end=" ", flush=True)
        time.sleep(tiempo)
        puntos-=1
    print()


def borrar_consola():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(f"\t{"="*21}\n\tVALIDACION  DE  DATOS\n\t{"="*21}")

borrar_consola()

nombre=input("\nIngrese su NOMBRE: ")
borrar_consola()

apellido=input("\nIngrese su APELLIDO: ")
borrar_consola()

edad=(input("\nIngrese su EDAD: "))
espera(4, 0.3)
borrar_consola()

if (nombre != ""):
    print(f"\nNombre: {nombre} 👍")
else:
    print(f"\nNombre: {error} {error_vacio}")
    valido=False
espera(4, 0.5)
borrar_consola()

if (apellido != ""):
    print(f"\nApellido: {apellido} 👍")
else:
    print(f"\nApellido: {error} {error_vacio}")
    valido=False
espera(4, 0.5)
borrar_consola()

if (edad != ""):
    if (int(edad) >= 18):
        print(f"\nEdad: {edad} 👍")
    else:
        print(f"\nEdad: {error} {error_menor}")
        valido=False
else:
    print(f"\nEdad: {error} {error_vacio}")
    valido=False
espera(5, 0.5)
borrar_consola()

if valido==True:
    print(f"\n\nBIENVENIDO {nombre} {apellido}. Tienes {edad} años. Eres mayor de edad.\n\n\n\n FIN DE LA VALIDACION")
else:
    print(f"\n\nLo siento, no has sido validado correctamente.\n\n\n\t{'*'*20}\n\tFIN DE LA VALIDACION\n\t{'*'*20}\n\n\n\n")





    

