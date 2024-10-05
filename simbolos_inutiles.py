with open('gramatica2.txt') as file:
    producciones = [linea.strip() for linea in file]


no_terminales = set()
for produccion in producciones:
    lado_izquierdo = produccion.split('->')[0].strip()  
    no_terminales.add(lado_izquierdo)


nuevas_producciones = []
for produccion in producciones:
    lado_izquierdo, lado_derecho = produccion.split('->')
    lado_izquierdo = lado_izquierdo.strip()
    partes_derecho = lado_derecho.split('|') 


    nuevas_partes_derecho = []
    for parte in partes_derecho:

        if not any(simbolo.isupper() and simbolo not in no_terminales for simbolo in parte):
            nuevas_partes_derecho.append(parte)

    if nuevas_partes_derecho:
        nuevas_producciones.append(f"{lado_izquierdo} -> {'|'.join(nuevas_partes_derecho)}")


primera_linea = nuevas_producciones[0]
lado_izquierdo, lado_derecho = primera_linea.split('->')
lado_derecho = lado_derecho.strip()
partes_derecho = lado_derecho.split('|')  


no_terminales_primer_linea = set()
for parte in partes_derecho:
    for simbolo in parte:
        if simbolo.isupper(): 
            no_terminales_primer_linea.add(simbolo)


no_terminales_primer_linea.add(lado_izquierdo.strip())


resultado_final = []
for produccion in nuevas_producciones:
    lado_izquierdo, lado_derecho = produccion.split('->')
    lado_izquierdo = lado_izquierdo.strip()


    if lado_izquierdo in no_terminales_primer_linea:
        resultado_final.append(produccion)


for produccion in resultado_final:
    print(produccion)
