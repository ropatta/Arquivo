#!/usr/bin/python3
#t

import os
import time
import csv

debug = 1
sensores = []
hosts = []
ambiente = 0

projeto = '/home/mdl/PSD'

with open('{}/codes/outros/sensores.csv'.format(projeto),'r', newline = "\n") as arquivo:
	leitura = csv.reader(arquivo, delimiter = ',')
	dados = list(leitura)
	#print (dados[:][1])
	#print (len(dados))
	for linha in range (len(dados)):
		hosts.append (dados[linha][1])
		sensores.append (dados[linha][2])

if debug:
	print ("num de sensores: "+str(len(sensores)) )
	print ("num de hosts: "+str(len(hosts)) )
	print ('\n sensores', sensores)
	print ('\n hosts',hosts)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#local para verificar o endereco dos sensores
# /sys/bus/w1/devices/

#Valores iniciais
cont_sensores = len(sensores)
ip_Zabbix = '10.254.32.33'
chave = "tempMot"
#host = 'L03_VTD_PSD_AQS_000'
manda_Zabbix = 1

#Verifica os arquivos de temperatura
def read_temp_file():
    f = open(arquivo, 'r')
    lines = f.readlines()
    f.close()
    return lines

#Le os valores de temperatura
def read_temp():
    lines = read_temp_file()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.1)
        lines = read_temp_file()
    temp_output = lines[1].find('t=')
    if temp_output == -1:
        return -1
    temp_string = lines[1].strip()[temp_output+2:]
    temp_c = float(temp_string) / 1000.0
    return temp_c

#Funcao que envia os dados para o zabbix
def envia_zabbix(host, valor):
	if debug:
	  print (str("zabbix_sender -z " + ip_Zabbix + " -s "+host + " -k " + chave +" -o " + str(valor)))
	# envia valores para Zabbix
	if (valor >= 10):
		os.system (str("zabbix_sender -z " + ip_Zabbix + " -s "+host + " -k " + chave +" -o " + str(valor)))

try:
  arquivo = ('/sys/bus/w1/devices/{}/w1_slave'.format(sensores[0]))
  if os.path.exists(arquivo):
    ambiente = read_temp()
  else:
    temp = 0
  if debug:
    print('temperatura ambiente {}'.format((ambiente)))

  for i in range (len(sensores)):
      arquivo = ('/sys/bus/w1/devices/{}/w1_slave'.format(sensores[i]))
      if os.path.exists(arquivo):
        temp = read_temp()
        if debug:
          print('temperatura {} {}\n'.format((i),(temp)))
      else:
        temp = 0
        print('\nfalha sensor {}\n'.format(i))
      time.sleep(.5)
      if manda_Zabbix :
          host = hosts[i]
          valor = round(temp,2)
          if (ambiente > 10):
            os.system("zabbix_sender -z {} -s {} -k tempMotS0 -o {}".format(ip_Zabbix, host, ambiente))
          if debug:
            print ("zabbix_sender -z {} -s {} -k tempMotS0 -o {}".format(ip_Zabbix, host, round(ambiente,2)))
          envia_zabbix(host, valor)
except Exception as e:
  print (e)
