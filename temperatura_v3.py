#!/usr/bin/python3

import os
import time
import csv

er

sensores = []

projeto = '/home/mdl/codes/PSD'

with open('/home/mdl/codes/sensores.csv'.format(projeto),'r', newline= '\n') as arquivo:

	leitura = csv.reader(arquivo, delimiter = ',')
	dados = list(leitura)
	for linha in dados:
 		a = linha[1]
 		sensores.append(a)

#print(dados)  #lista do arquivo csv com nome e valor
#print(sensores) #lista com endereço dos sensores
#print(len(sensores))


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')



#local para verificar oendereco dos sensores
# /sys/bus/w1/devices/

#Valores iniciais
cont_sensores = len(sensores)
ip_Zabbix = '10.254.32.33'
host = 'L03_VTD_PSD_AQS_000'
manda_Zabbix = 0


def read_temp_file():  #rotina para abertura e leitura do arquivo
    f = open(arquivo, 'r')
    lines = f.readlines()  #coloca em lista o arquivo W1_slave , linha 1 e 2
    print(lines)
    f.close()
    return lines

#Le os valores de temperatura
def read_temp():
    
    
    lines = read_temp_file()
    while lines[0].strip()[-3:] != 'YES':  #verifica se medição foi ok
        print("LEITURA INCONSISTENTE DO SENSOR!!!")
        time.sleep(0.1)
        lines = read_temp_file()
    temp_output = lines[1].find('t=')  #se ok, pega valor pra frente de t=
    if temp_output == -1:
        return -1
    temp_string = lines[1].strip()[temp_output+2:] #convert de string para floating
    temp_c = float(temp_string) / 1000.0
    return temp_c

#Funcao que envia os dados para o zabbix
def envia_zabbix(chave, valor):
	#debug
	a = str("zabbix_sender -z " + ip_Zabbix + " -s "+host + " -k " + chave +" -o " + str(valor))
	print (a)
	# envia valores para Zabbix
	os.system (str("zabbix_sender -z " + ip_Zabbix + " -s "+host + " -k " + chave +" -o " + str(valor)))

try:
  for i in list(range(cont_sensores)):
      arquivo = ('/sys/bus/w1/devices/{}/w1_slave'.format(sensores[i])) #arquivo é acrescido com o numero da pasta do sensor
      print(os.system('pwd'))
      
      if os.path.exists(arquivo): #verifica se o caminho arquivo existe
      
        temp = read_temp()  #rotina de medição de temperatura
        print('temperatura do sensor {} {}'.format((i),(temp)))
      else:
        temp = 0
        print('\nfalha sensor {}\n'.format(i))
      time.sleep(1)
      if manda_Zabbix == 1:
          chave = "tempMotS"+str(i)
          valor = round(temp,2)
          envia_zabbix(chave,valor)
except Exception as e:
  print (e)
