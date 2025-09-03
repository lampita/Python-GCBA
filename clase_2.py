import os
def borrar_consola():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    

borrar_consola()

print("\033[1;91mGESTION DE USUARIOS\033[0m".center(100))
nombre=input("\nIngrese su nombre: ")
edad=input("\nIngrese su edad: ")
email=input("\nIngrese su email: ")

borrar_consola()

h_bar= "-" * (len(nombre)+40)
relleno_edad= " " * (len(h_bar)-15-len(str(edad)))
relleno_mail= " " * (len(h_bar)-10-len(email))
cierre= " " * (len(h_bar))


print(f"\n\t+{h_bar}+")
print(f"\t+{' '*20}\033[1;45m{nombre}\033[0m{' '*20}+")
print(f"\t+{h_bar}+")
print(f"\t+{' '*4}\033[1;30mEdad:\033[0m {edad} años{relleno_edad}+")
print(f"\t+{' '*4}\033[1;30mmail:\033[0m {email}{relleno_mail}+")
print(f"\t+{cierre}+")
print(f"\t+{h_bar}+\n\n\n\n")