def nombre_es_valido(nombre):
    if not nombre.strip():
        print ("Campo vacío")
        return "campo vacio",False
     
    if any(char.isdigit() for char in nombre):
        print ("Contiene números")
        return False
    
    if any(not char.isalpha() for char in nombre):
        print("Contiene caracteres especiales")
        return False
    
    return True

nombre=""


print(nombre_es_valido(nombre))