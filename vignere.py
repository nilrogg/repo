import sys
import random

#Variable global letras

LETRAS="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def main():
	texto="Mary tenia un corderito"
	clave="PATITO"
	clave=clave.upper()
	cifrado=encode_text(texto,clave)
	descifrado=decode_text(cifrado,clave)
	print "".join(cifrado)
	print "".join(descifrado)
	
#Funcion que sirve para codificar

def encode_text(mensaje,clave):
	claveIndex=0
	resultado=[]
	for simbolo in mensaje:
		num=LETRAS.find(simbolo.upper())
		if num!=-1:
			num+=LETRAS.find(clave[claveIndex])
			num%=len(LETRAS)
			resultado.append(LETRAS[num])
	return resultado

#Funcion que sirve para decodificar

def decode_text(mensaje,clave):
	claveIndex=0
	resultado=[]
	for simbolo in mensaje:
		num=LETRAS.find(simbolo.upper())
		if num!=-1:
			num-=LETRAS.find(clave[claveIndex])
			num%=len(LETRAS)
			resultado.append(LETRAS[num])
	return resultado
		
	
if __name__ == "__main__":
	main()