#!/usr/bin/python3
#coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil
import sys
from datetime import datetime
from datetime import date
from pathlib import Path

plt.switch_backend('Agg')
plt.rcParams['axes.facecolor'] = 'black'


'''
**************************************************************************************
				Declaracao das constantes
**************************************************************************************
'''

projeto = '/mnt/mdl_data/correntePSD/'
dataAtual = datetime.now()
hora = dataAtual.strftime("%H-%M-%S")
dataAtual = dataAtual.strftime("20%y-%m-%d")


ipZabbix = "10.254.32.33"
flagSendZabbix = 1
geraGraficos = 1

debug = 0
debug2 = 0

lowTriggerPeakCurrCl = 3			#usado para mudar cor do grafico
upTriggerPeakCurrCl = 6				#usado para mudar cor do grafico
lowLimitPeakCurrCl = 3				#usado para enviar para o zabbix
upLimitPeakCurrCl = 9				#usado para enviar para o zabbix

lowTriggerPeakCurrOp = -6
upTriggerPeakCurrOp = -3
lowLimitPeakCurrOp = -9
upLimitPeakCurrOp = -3

lowTriggerMeanCurrOp = -1.8
upTriggerMeanCurrOp = -1
lowLimitMeanCurrOp = -3
upLimitMeanCurrOp = 0

lowTriggerWeightOp = 2
upTriggerWeightOp = 10
lowLimitWeightOp = 3
upLimitWeightOp = 9

lowTriggerWeightCl = 2
upTriggerWeightCl = 10
lowLimitWeightCl = 3
upLimitWeightCl = 9

lowTriggerWeight = 2
upTriggerWeight = 10
lowLimitWeight = 3
upLimitWeight = 9

lowTriggerMeanCurrCl = 1
upTriggerMeanCurrCl = 1.8
lowLimitMeanCurrCl = 0
upLimitMeanCurrCl = 3

lowTriggerMeanManCurrOp = -3
upTriggerMeanManCurrOp = -1
lowLimitMeanManCurrOp = -5
upLimitMeanManCurrOp = 0

lowTriggerMeanManCurrCl = 1
upTriggerMeanManCurrCl = 3
lowLimitMeanManCurrCl = 0
upLimitMeanManCurrCl = 4

lowTriggerManClCurr = 1
upTriggerManClCurr = 3
lowLimitManClCurr = 0
upLimitManClCurr = 4

lowTriggerOpTime = 2.5
upTriggerOpTime = 4.5
lowLimitOpTime = 2
upLimitOpTime = 5

lowTriggerClTime = 2.5
upTriggerClTime = 4.5
lowLimitClTime = 2
upLimitClTime = 5

opDoor = 0
opPeak1 = 0
opPeak2 = 0
opIndexInit = 0
opIndexEnd = 0
manOpCurr = 0
countOpPeak1 = 0
countOpPeak2 = 0
count2OpPeak2 = 0
flagManOpCurr = 0
clDoor = 0
clPeak1 = 0
clPeak2 = 0
clIndexInit = 0
clIndexEnd = 0
clTime = 0
manClCurr = 0
countClPeak1 = 0
countClPeak2 = 0
countClosedDoor = 0
manCurrCl = []
tempo = []
openingDoor = 0
closedDoor = 0
closingDoor = 0
openedDoor = 0
flag0 = 0
flag1 = 0
flag2 = 0
flag3 = 0
kComecoAbertura = 0
kFinalAbertura = 0
kComecoFechamento = 0
kFinalFechamento = 0
begin = 1
mediaAbertura = 0
mediaFechamento = 0
offset = 0



def createDirs(logsDir, figsDir, dataAtual=dataAtual, horaAtual=hora):
	if(os.path.isdir(logsDir) == 0):
		if(debug):("Pasta dos logs nao existe, sera criada !")
		os.mkdir(logsDir);
		if(debug):("Deu bom !")
	else:
		if(debug):("Pasta dos logs ja existe")
	if(debug):(logsDir)

	if(os.path.isdir(f"{logsDir}/{dataAtual}") == 0):
		if(debug):("Pasta dos logs do dia nao existe, sera criada !")
		os.mkdir(f"{logsDir}/{dataAtual}");
		if(debug):("Deu bom !")
	else:
		if(debug):("Pasta dos logs do dia ja existe")
	if(debug):(f"{logsDir}/{dataAtual}")


	if(os.path.isdir(f"{logsDir}/{dataAtual}/{horaAtual}") == 0):
		if(debug):("Pasta da hora dos logs do dia nao existe, sera criada !")
		os.mkdir(f"{logsDir}/{dataAtual}/{horaAtual}/");
		if(debug):("Deu bom !")
	else:
		if(debug):("Pasta da hora dos logs do dia ja existe")
	if(debug):(f"{logsDir}/{dataAtual}/{horaAtual}")

	if(os.path.isdir(figsDir) == 0):
		if(debug):("Pasta das figs nao existe, sera criada !")
		os.mkdir(figsDir);
		if(debug):("Deu bom !")
	else:
		if(debug):("Pasta das figs ja existe")
	if(debug):(figsDir)

	if(os.path.isdir(f"{figsDir}/{dataAtual}") == 0):
		if(debug):("Pasta das figs do dia nao existe, sera criada !")
		os.mkdir(f"{figsDir}/{dataAtual}");
		if(debug):("Deu bom !")
	else:
		if(debug):("Pasta das figs do dia ja existe")
	if(debug):(f"{figsDir}/{dataAtual}")

	if(os.path.isdir(f"{figsDir}/{dataAtual}/{horaAtual}") == 0):
		if(debug):("Pasta da hora das figs do dia nao existe, sera criada !")
		os.mkdir(f"{figsDir}/{dataAtual}/{horaAtual}");
		if(debug):("Deu bom !")
	else:
		if(debug):("Pasta da hora das figs do dia ja existe")
	if(debug):(f"{figsDir}/{dataAtual}/{horaAtual}")



'''
**************************************************************************************
				Configura pastas
**************************************************************************************
'''
#pastaDoDia = "/home/pi/projetos/05_Monitoramento_PSD/figs/"+dataAtual
#pastaDasFigs = "/var/www/html/graficos/"+dataAtual
#pastaLogs = "/home/pi/projetos/05_Monitoramento_PSD/logs/"+dataAtual
pastaDoDia = "/home/mdl/PSD/figs/teste/"
pastaDasFigs = "/var/www/mdlweb/graficos/teste/"
#logsDir = "/home/pi/PSD/logs/teste/"
logsDir = "/var/www/mdlweb/logs"
figsDir = "/var/www/mdlweb/figs"
logs = f"/home/mdl/PSD/logs/{dataAtual}"
#pastaLogs = "/home/pi/PSD/logs/"+dataAtual


modificacao = lambda f: f.stat().st_mtime
dir = Path(logs)


#nomePastaDasFigs = ultimoArquivo[-19:-11]

portasMod = []
portasMod.append([11, 12, 13, 14, 21, 22, 23, 24])
portasMod.append([31, 32, 33, 34, 41, 42, 43, 44])
portasMod.append([51, 52, 53, 54, 61, 62, 63, 64])

nice = [11,12,13,14,21,22,23,24,31,32,33,34,41,42,43,44,51,52,53,54,61,62,63,64]

#corrente = list(map(lambda x:((x-offset1)*16.66), epa))

'''
**************************************************************************************
			Constroi a figura de cada porta
**************************************************************************************
'''
def plotaAlternativa():
	fig, ax = plt.subplots(3,1)
	fig.set_size_inches(14, 9)
	fig.facecolor='#008060'
	ax[0].grid(True);ax[1].grid(True);ax[2].grid(True)
	ax[0].set_xlabel('Tempo (ms)')
	ax[0].set_ylabel('Corrente do motor (A)', fontweight="bold")
	ax[1].set_xlabel('Tempo (ms)')
	ax[1].set_ylabel('Corrente do motor (A)', fontweight="bold")
	ax[2].set_xlabel('Tempo (ms)')
	ax[2].set_ylabel('Corrente do motor (A)', fontweight="bold")
#	ax[0].set_ylim(-6, 6)
#	ax[1].set_ylim(-8, 3)
#	ax[2].set_ylim(-3, 8)

	#ax[0].axvline(x=tempo[kComecoAbertura], c="r", linewidth="0.5")
	#ax[0].axvline(x=tempo[kFinalAbertura], c="r", linewidth="0.5")
	#ax[0].axvline(x=tempo[kComecoFechamento], c="r", linewidth="0.5")
	#ax[0].axvline(x=tempo[kFinalFechamento], c="r", linewidth="0.5")
	#ax[1].axvline(x=tempo[opIndexInit+20], c="r", linewidth="0.5")
	#ax[1].axvline(x=tempo[opIndexEnd-20], c="r", linewidth="0.5")
	ax[2].axvline(x=tempo[kComecoAbertura], c="r", linewidth="0.5")
	ax[2].axvline(x=tempo[kFinalAbertura], c="r", linewidth="0.5")

	ax[0].plot(naruto.iloc[kComecoAbertura-200:kFinalFechamento+200,1], naruto.iloc[kComecoAbertura-200:kFinalFechamento+200,2], color="orange", label="Corrente do motor")
	ax[1].plot(tempo, current, color="orange", label="Corrente do motor")
	ax[2].plot(tempo[opIndexInit:opIndexEnd], current[opIndexInit:opIndexEnd], color="orange", label="Corrente do motor")
	ax[0].set_title(f'Curva de corrente', fontweight="bold")
#	plt.savefig(pastaDoDia+'/'+nomePastaDasFigs+'/P'+str(porta)+'.png', format='png')
	plt.subplots_adjust(top=1-(35/25.4)/8, bottom=(12/25.4)/8, right=1-(5/25.4)/16, left=(20/25.4)/16, hspace=0.4)
#	fig.tight_layout()
	fig.savefig(f"{figsDir}/{dataAtual}/{horaDoLog}/teste.png", format='png')
	plt.clf()
	plt.cla()
	plt.close()



'''
**************************************************************************************
			Constroi a figura de cada porta
**************************************************************************************
'''
def createFigure(porta, fail):
	fig, ax = plt.subplots(3,1)
	fig.set_size_inches(14, 9)
	fig.facecolor='#008060'
	ax[0].grid(True);ax[1].grid(True);ax[2].grid(True)
	ax[0].set_xlabel('Tempo (ms)')
	ax[0].set_ylabel('Corrente do motor (A)', fontweight="bold")
	ax[1].set_xlabel('Tempo (ms)')
	ax[1].set_ylabel('Corrente do motor (A)', fontweight="bold")
	ax[2].set_xlabel('Tempo (ms)')
	ax[2].set_ylabel('Corrente do motor (A)', fontweight="bold")
	#ax[0].axis([0, tempo[len(tempo)-1], -6, 6])
	#ax[1].set_ylim(-8, 3)
	#ax[2].set_ylim(-3, 8)
	if(fail == 0):
		ax[0].set_ylim(-6, 6)
		#print(f"{tempo[-1]}")
		ax[0].set_xlim(tempo[0], tempo.iloc[-1])
		ax[1].set_title(f'Abertura', fontweight="bold")
		ax[2].set_title(f'Fechamento', fontweight="bold")

		if( (tempo[opIndexEnd]-tempo[opIndexInit]) > (tempo[clIndexEnd]-tempo[clIndexInit]) ):
			indexToGraph = int(tempo[clIndexInit]+tempo[opIndexEnd])
			ax[1].set_xlim(tempo[opIndexInit], tempo[opIndexEnd])
			ax[2].set_xlim(tempo[opIndexInit], tempo[opIndexEnd])
			ax[1].fill_between(tempo[:opIndexEnd], current[:opIndexEnd]-0.5, current[:opIndexEnd]+0.5, alpha=0.3)
			ax[1].plot(tempo[opIndexInit:opIndexEnd], current[opIndexInit:opIndexEnd], color="orange", label="Corrente do motor")
			ax[2].fill_between(tempo[clIndexInit:indexToGraph]-tempo[clIndexInit], current[clIndexInit:indexToGraph]-0.5, current[clIndexInit:indexToGraph]+0.5, alpha=0.3)
			ax[2].plot(tempo[clIndexInit:indexToGraph]-tempo[clIndexInit], current[clIndexInit:indexToGraph], color="orange", label="Corrente do motor")
		else:
			indexToGraph = int(tempo[clIndexEnd]-tempo[clIndexInit])
			ax[1].set_xlim(0, indexToGraph )
			ax[2].set_xlim(0, indexToGraph )
			ax[1].fill_between(tempo[:indexToGraph], current[:indexToGraph]-0.5, current[:indexToGraph]+0.5, alpha=0.3)
			ax[1].plot(tempo[:indexToGraph], current[:indexToGraph], color="orange", label="Corrente do motor")
			ax[2].fill_between(tempo[clIndexInit:clIndexEnd]-tempo[clIndexInit], current[clIndexInit:clIndexEnd]-0.5, current[clIndexInit:clIndexEnd]+0.5, alpha=0.3)
			ax[2].plot(tempo[clIndexInit:clIndexEnd]-tempo[clIndexInit], current[clIndexInit:clIndexEnd], color="orange", label="Corrente do motor")

		#plt.axis([0, tempo[kFinalFechamento-1], -6, 6])

		ax[0].text(tempo[int(len(tempo)/4.5)], 12, "Companhia do Metropolitano de Sao Paulo - METRO SP", fontweight="bold", size=20, color="blue")
		ax[0].text(tempo[int(len(tempo)/3)], 9, "Monitoramento Portas de Plataforma (PSD) - VTD", fontweight="bold", size=15)
		ax[0].text(tempo[int(len(tempo)*4/6)], 15.2, f"Ciclo realizado em {dataAtual} as {horaDoLog}", size=8)

		ax[0].axvline(x=tempo[opIndexInit], c="r", linewidth="0.5")
		ax[0].axvline(x=tempo[opIndexEnd], c="r", linewidth="0.5")
		if(debug):(f"clIndexInit={clIndexInit} clIndexEnd={clIndexEnd} tempo={len(tempo)}")
		ax[0].axvline(x=tempo[clIndexInit], c="r", linewidth="0.5")
		ax[0].axvline(x=tempo[clIndexEnd], c="r", linewidth="0.5")

		#ax[1].axvline(x=tempo[opIndexInit+20], c="r", linewidth="0.5")
		#ax[1].axvline(x=tempo[opIndexEnd-20], c="r", linewidth="0.5")

		#ax[2].axvline(x=tempo[-500], c="r", linewidth="0.5")
		#ax[2].axvline(x=tempo[-200], c="r", linewidth="0.5")

		#plt.text(tempo[70], correnteMinima, "Pico de Abertura", fontweight="bold")
		#plt.text(tempo[clIndexInit-800], correnteMaxima, "Pico de Fechamento", fontweight="bold")
		#plt.text(tempo[int(clIndexEnd/2) - 220], meanManCurrOp+0.5, "Porta aberta", fontweight="bold")

		marginText = tempo[0]
		if( (peakCurrentOp > upTriggerPeakCurrOp) | (peakCurrentOp < lowTriggerPeakCurrOp) ):
			ax[0].text(marginText, 15, f"Corrente Pico Aber.:...... {peakCurrentOp:4.2f}A", color = 'red', fontweight='bold' )
		else:
			ax[0].text(marginText, 15, f"Corrente Pico Aber.:...... {peakCurrentOp:4.2f}A", color = 'black', fontweight='bold')

		if( (meanCurrentOp > upTriggerMeanCurrOp) | (meanCurrentOp < lowTriggerMeanCurrOp) ):
			ax[0].text(marginText, 14, f"Corrente Arrasto Aber.:. {meanCurrentOp:4.2f}A", color = 'red', fontweight='bold' )
		else:
			ax[0].text(marginText, 14, f"Corrente Arrasto Aber.:. {meanCurrentOp:4.2f}A", color = 'black', fontweight='bold')

		if( (meanManCurrOp > upTriggerMeanManCurrOp) | (meanManCurrOp < lowTriggerMeanManCurrOp) ):
			ax[0].text(marginText, 13, f"Corrente Manut. Aber.:.. {meanManCurrOp:4.2f}A", color = 'red', fontweight='bold' )
		else:
			ax[0].text(marginText, 13, f"Corrente Manut. Aber.:.. {meanManCurrOp:4.2f}A", color = 'black', fontweight='bold' )

		if( (peakCurrentCl > upTriggerPeakCurrCl) | (peakCurrentCl < lowTriggerPeakCurrCl) ):
			ax[0].text(marginText, 12, f"Corrente Pico Fech.:....... {peakCurrentCl:4.2f}A", color = 'red', fontweight='bold' )
		else:
			ax[0].text(marginText, 12, f"Corrente Pico Fech.:....... {peakCurrentCl:4.2f}A", color = 'black', fontweight='bold')

		if( (meanCurrentCl > upTriggerMeanCurrCl) | (meanCurrentCl < lowTriggerMeanCurrCl) ):
			ax[0].text(marginText, 11, f"Corrente Arrasto Fech.:.. {meanCurrentCl:4.2f}A", color = 'red', fontweight='bold' )
		else:
			ax[0].text(marginText, 11, f"Corrente Arrasto Fech.:.. {meanCurrentCl:4.2f}A", color = 'black', fontweight='bold' )

		if( (meanManCurrCl > upTriggerMeanManCurrCl) | (meanManCurrCl < lowTriggerMeanManCurrCl) ):
			ax[0].text(marginText, 10, f"Corrente Manut. Fech.:... {meanManCurrCl:4.2f}A", color = 'red', fontweight='bold' )
		else:
			ax[0].text(marginText, 10, f"Corrente Manut. Fech.:... {meanManCurrCl:4.2f}A", color = 'black', fontweight='bold' )

		if( (opTime > upTriggerOpTime) | (opTime < lowTriggerOpTime) ):
			ax[0].text(marginText, 9, f"Tempo Abertura:............ {opTime:3.2f}s", color = 'red', fontweight="bold" )
		else:
			ax[0].text(marginText, 9, f"Tempo Abertura:............ {opTime:3.2f}s", color = 'black', fontweight='bold')

		if( (clTime > upTriggerClTime) | (clTime < lowTriggerClTime) ):
			ax[0].text(marginText, 8, f"Tempo Fechamento:....... {clTime:3.2f}s", color = 'red', fontweight="bold")
		else:
			ax[0].text(marginText, 8, f"Tempo Fechamento:....... {clTime:3.2f}s", color = 'black', fontweight='bold' )

		if( (clTime > upTriggerClTime) | (clTime < lowTriggerClTime) ):
			ax[0].text(marginText, 7, f"Temp. Motor:.................. {clTime:3.2f}C", color = 'red', fontweight="bold")
		else:
			ax[0].text(marginText, 7, f"Temp. Motor:.................. {clTime:3.2f}C", color = 'black', fontweight='bold' )

		ax[0].fill_between(tempo, current-0.5, current+0.5, alpha=0.4)


	ax[0].plot(tempo, current, color="orange", label="Corrente do motor")
	ax[0].set_title(f'Curva de corrente P{porta}', fontweight="bold")
#	plt.savefig(pastaDoDia+'/'+nomePastaDasFigs+'/P'+str(porta)+'.png', format='png')
	plt.subplots_adjust(top=1-(35/25.4)/8, bottom=(12/25.4)/8, right=1-(5/25.4)/16, left=(20/25.4)/16, hspace=0.4)
#	fig.tight_layout()
	fig.savefig(f"{figsDir}/{dataAtual}/{horaDoLog}/P{porta}.png", format='png')
	plt.clf()
	plt.cla()
	plt.close()



'''
**************************************************************************************
		Analisa de deve mandar as informacoes para o zabbix
**************************************************************************************
'''
def zabbixAnalise(porta):
	if( (peakCurrentCl > lowLimitPeakCurrCl) and (peakCurrentCl <  upLimitPeakCurrCl) ):
		sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(porta), "peakCl", str(peakCurrentCl) )

	if( (peakCurrentOp > lowLimitPeakCurrOp) and (peakCurrentOp <  upLimitPeakCurrOp) ):
		sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(porta), "peakOp", str(peakCurrentOp) )

	if( (meanManCurrOp > lowLimitMeanManCurrOp) and (meanManCurrOp <  upLimitMeanManCurrOp) ):
		sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(porta), "manCurrentOp", str(meanManCurrOp) )

	if( (meanManCurrCl > lowLimitMeanManCurrCl) and (meanManCurrCl <  upLimitMeanManCurrCl) ):
		sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(porta), "manCurrentCl", str(meanManCurrCl) )

	if( (meanCurrentOp > lowLimitMeanCurrOp) and (meanCurrentOp <  upLimitMeanCurrOp) ):
		sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(porta), "meanCurrentOp", str(meanCurrentOp) )

	if( (meanCurrentCl > lowLimitMeanCurrCl) and (meanCurrentCl <  upLimitMeanCurrCl) ):
		sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(porta), "meanCurrentCl", str(meanCurrentCl) )
	'''
	if( (weightOp > lowLimitWeightOp) and (weightOp <  upLimitWeightOp) ):
		sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(porta), "weightOp", str(weightOp) )

	if( (weightCl > lowLimitWeightCl) and (weightCl <  upLimitWeightCl) ):
		sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(porta), "weightCl", str(weightCl) )
	'''

	if( (weight > lowLimitWeight) and (weight <  upLimitWeight) ):
		sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(porta), "weight", str(weight) )

	if( (opTime > lowLimitOpTime) and (opTime <  upLimitOpTime) ):
		sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(porta), "openTime", str(opTime) )

	if( (clTime > lowLimitClTime) and (clTime <  upLimitClTime) ):
		sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(porta), "closeTime", str(clTime) )



'''
**************************************************************************************
			Envia as informacoes para o zabbix
**************************************************************************************
'''
def sendZabbix(server, host, key, value):
	os.system(str("zabbix_sender -z " + server + " -s " + host + " -k " + key + " -o " + value ))





'''
**************************************************************************************
				Loop principal
**************************************************************************************
'''

for j in range(1, 4):
	files = dir.glob('*.csv')
	ordenados = sorted(files, key=modificacao, reverse=False)
	#print(logs)
	if(debug):print(ordenados)
	if(len(ordenados) > 3):
		ultimoArquivo = str(ordenados[0])
		doorIndex = int(ultimoArquivo[-5])-1
		horaDoLog = ultimoArquivo[-19:-11]
		if(debug2):
			print(f"Comecou o arquivo: {ultimoArquivo}")
			print(f"Hora do LOG: {horaDoLog} Indice da Porta: {doorIndex}")
		createDirs(logsDir, figsDir, dataAtual, horaDoLog)
		naruto = pd.read_csv(f"{ultimoArquivo}", delimiter = ';', skiprows=[1, 2])
		for i in range(2, 10):
			zoro = naruto.iloc[:, i]
			if(len(zoro) > 60000):
				break
			if(debug2):
				print ("*****************************")
				print (f"Comecou a P{portasMod[doorIndex][i-2]}")
				print ("Entrou na analise 1")
				'''
				print ("begin:"+str(begin))
				print ("openedDoor:"+str(openedDoor))
				print ("closingDoor:"+str(closingDoor))
				print ("closedDoor:"+str(closedDoor))
				'''
			try:
				for k in range (1, len(zoro)-5):
					#print(f"zoro[{k}] = {zoro[k]}")
					if( begin ):
						if(debug):print (f"tentou comeco da abertura flag0={flag0} k={k}  zoro[k+20]={zoro[k+20]} zoro[k]={zoro[k]}")
						if( (zoro[k+20] < zoro[k]) and (( abs(zoro[k+20] - zoro[k]) ) > 80) and (openingDoor==0)):
							flag0 = flag0 + 1
							#if(debug):print (f"tentou comeco da abertura flag0={flag0} k={k}  zoro[k+30]={zoro[k+30]} zoro[k]={zoro[k]}")
							if(flag0 > 5):
								kComecoAbertura = k
								openingDoor = 1
								closedDoor = 0
								openedDoor = 0
								closingDoor = 0
								flag0 = 0
								begin = 0
								if(debug):print (f"	Achou comeco da abertura da P{portasMod[doorIndex][i-2]} k = {kComecoAbertura}")
						else:
							flag0 = 0
							if(k > 2000):break

					if(openingDoor and (k > (1.5*kComecoAbertura)) ):
						if( (zoro[k+30] < zoro[k]) and (( abs(zoro[k] - zoro[k+30]) ) > 100) ):
							flag1 = flag1 + 1
							if(flag1 > 5):
								kFinalAbertura = k+100
								abertura = zoro[kComecoAbertura:kFinalAbertura]
								openingDoor = 0
								closedDoor = 0
								closingDoor = 0
								openedDoor = 1
								flag1 = 0
								if(debug):print ("	Achou final abertura da P"+str(portasMod[doorIndex][i-2])+" k = "+str(kFinalAbertura))
						else:
							flag1 = 0

					if( openedDoor and (k > (1.5*kFinalAbertura)) ):
						#if( (zoro[k+5] > zoro[k]) and (abs(zoro[k+5] - zoro[k]) > 0.3) and (k > 1000)):
						if( (zoro[k+20] > zoro[k]) and (( abs(zoro[k+20] - zoro[k]) ) > 80) ):
							flag2 = flag2 + 1
							if(debug):print (f"tentou comeco do fechamento flag2={flag2} k={k}  zoro[k+20]={zoro[k+20]} zoro[k]={zoro[k]}")
							if(flag2 > 3):
								kComecoFechamento = k
								aberta = zoro[kFinalAbertura: kComecoFechamento]
								openingDoor = 0
								closedDoor = 0
								openedDoor = 0
								closingDoor = 1
								flag2 = 0
								if(debug):print ("	Achou comeco do fechamento da P"+str(portasMod[doorIndex][i-2])+" k = "+str(kComecoFechamento))
						else:
							flag2 = 0

					if( closingDoor ):
						if( (zoro[k+50] > zoro[k]) and (abs(zoro[k+50] - zoro[k]) > 100) and (k > kComecoFechamento+300)):
						#if( (zoro[k+5] > zoro[k]) and (abs(zoro[k+5] - zoro[k]) > 0.3) ):
							flag3 = flag3 + 1
							if(flag3 > 8):
								kFinalFechamento = k+50
								fechamento = zoro[kComecoFechamento:kFinalFechamento]
								fechada = zoro[kFinalFechamento:]
								openingDoor = 0
								closedDoor = 1
								openedDoor = 0
								closingDoor = 0
								flag3 = 0
								if(debug):print ("	Achou final fechamento da P"+str(portasMod[doorIndex][i-2])+" k = "+str(kFinalFechamento))
						else:
							flag3 = 0

			except KeyError:
				if(debug):print("Provavelmente nao encontrou os valores esperados")


			if (closedDoor):	#analise 1 bem sucedida
				if(debug2):
					print("Entrou na analise 2")
				mediaAbertura = abertura.mean()
				mediaFechamento = fechamento.mean()
				offsetCorrente = (mediaAbertura+mediaFechamento)/2
				if(kComecoAbertura > 200):
					current = naruto.iloc[kComecoAbertura-200:kFinalFechamento+200, i]
					tempo = naruto.iloc[kComecoAbertura-200:kFinalFechamento+200, 1]
				else:
					current = naruto.iloc[:kFinalFechamento+200, i]
					tempo = naruto.iloc[:kFinalFechamento+200, 1]
				offsetTempo = int(tempo[kComecoAbertura])

				current.reset_index(inplace=True, drop=True)
				tempo.reset_index(inplace=True, drop=True)

				if(debug):
					print(f"offset de Corrente:{offsetCorrente}\noffset de Tempo:{offsetTempo}")
					#print(f"{current}")


				current = current.sub(offsetCorrente)
				current = current.mul(1/65)
				tempo = tempo.sub(offsetTempo)

				#plotaAlternativa()
				if(debug2):
					print (f'{current.head()}')
					print (f'{tempo.head()}')

				if( (offsetCorrente > 1800) and (offsetCorrente < 2500) ):
#					for k in range (kComecoAbertura, kFinalFechamento):
					for k in range (len(current)):
						if( (opDoor == 0) and (k < len(current)/2 )):				#se for comeco do arquivo a porta estara abrindo

							if( (current[k] < 0) and (opPeak1 == 0) ):				#se o valor for positivo significa que esta indo pro segundo pico
								countOpPeak1 = countOpPeak1 + 1
								if(countOpPeak1 >= 8):					#mais de 5 medidas seguidas positivas categoriza o segundo pico
									opPeak1 = 1
									opIndexInit = k-7
							else:
								countOpPeak1 = 0

							if( (current[k] > 0) and (opPeak2 == 0) and (opPeak1) ):				#se o valor for positivo significa que esta indo pro segundo pico
								countOpPeak2 = countOpPeak2 + 1
								if(countOpPeak2 >= 5):					#mais de 5 medidas seguidas positivas categoriza o segundo pico
									opPeak2 = 1
							else:
								countOpPeak2 = 0


							if( (opPeak2 == 1) and (current[k] < 0) ):				#quando voltar para a parte negativa porta terminou de abrir
								count2OpPeak2 = count2OpPeak2 + 1
								if(count2OpPeak2 >= 40):
									opDoor = 1
									opIndexEnd = k
							else:
								count2OpPeak2 = 0
						else:
							if(clPeak1 == 0):
								if(current[k] > 0):					#detecta o primeiro pico do fechamento
									countClPeak1 = countClPeak1 + 1
									if(countClPeak1 >= 8):
										if(debug):print ("	pico de fechamento 1")
										clPeak1 = 1
										clIndexInit = k-15
								else:
									countClPeak1 = 0
							else:

								if(clPeak2 == 0):					#detecta o segundo pico do fechamento
									if(current[k] < 0):
										countClPeak2 = countClPeak2 + 1
										if(debug):print ("	pico de fechamento 2 tentando")
										if(countClPeak2 >= 3):
											if(debug):print ("	pico de fechamento 2")
											clPeak2 = 1
									else:
										countClPeak2 = 0
								else:
									if(current[k] > 0):				#final do fechamento
										countClosedDoor = countClosedDoor + 1
										if(countClosedDoor >= 40):
											if(debug):print ("	fechada")
											countClosedDoor = 0
											clIndexEnd = k
											break
									else:
										countClosedDoor = 0



					if(debug):
						print ("	indice do comeco de abertura: "+str(opIndexInit))
						print ("	indice do final de abertura: "+str(opIndexEnd))
						print ("	indice do comeco do fechamento: "+str(clIndexInit))
						print ("	indice do final do fechamento: "+str(clIndexEnd))

					if(clIndexEnd):
						if(debug):
							print ("	Conseguiu achar os pontos da curva")
#						corrente = current.loc[opIndexInit:clIndexEnd-1]
						#corrente = current.loc[opIndexInit:clIndexEnd]
						#tempo = naruto.iloc[opIndexInit:clIndexEnd, 1]

						#plotaAlternativa()

						manutencaoCl1 = current[:opIndexInit]
						abertura = current[opIndexInit:opIndexEnd]
						manutencaoOp = current[opIndexEnd:clIndexInit]
						fechamento = current[clIndexInit:clIndexEnd]
						manutencaoCl2 = current[clIndexEnd:]

						#plotaAlternativa()

						peakCurrentOp = current.min()
						meanCurrentOp = abertura.mean()
						meanManCurrOp = manutencaoOp.mean()

						peakCurrentCl = current.max()
						meanCurrentCl = fechamento.mean()
						meanManCurrCl = manutencaoCl2.mean()

						weightOp = (-0.766 + 4.587*meanCurrentOp)*-1;
						weightCl = -0.766 + 4.587*meanCurrentCl;

						weight = (weightOp + weightCl)/2;

						opTime = tempo[opIndexEnd] / 1000
						clTime = ( tempo[clIndexEnd-1] - tempo[clIndexInit] ) / 1000

						if(debug):
							print ("		Corrente Maxima = "+str(peakCurrentCl)+" A")
							print ("		Corrente Minima = "+str(peakCurrentOp)+" A")
							print ("		Corrente Manutencao aberta = "+str(meanManCurrOp)+" A")
							print ("		Tempo Abertura = "+str(opTime)+" s")
							print ("		Tempo Fechamento = "+str(clTime)+" s")

						if(geraGraficos):createFigure(str(portasMod[doorIndex][i-2]), 0)
						if(flagSendZabbix):
							zabbixAnalise(portasMod[doorIndex][i-2])
							sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(portasMod[doorIndex][i-2]), "erro01", "0")

					else:
						if(debug):
							print ("	Nao achou os pontos na analise 2")
						if(flagSendZabbix):	#nao conseguiu pegar os parametros da curva, envia erro
							sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(portasMod[doorIndex][i-2]), "erro01", "1")
						#corrente = zoro.loc[:]
						current = naruto.iloc[:, i]
						tempo = naruto.iloc[:, 1]
						clIndexEnd = kFinalFechamento
						if(geraGraficos):createFigure(str(portasMod[doorIndex][i-2]), 1)

				else:
					if(debug):print("Valor do offset deu zuado")


			else:					#nao conseguiu pegar os parametros iniciais da curva, envia erro

				if(debug):
					print ("Nao achou os pontos na analise 1")
				#current = zoro.loc[:]
				current = naruto.iloc[:, i]
				tempo = naruto.iloc[:, 1]
				clIndexEnd = kFinalFechamento
				if(geraGraficos):createFigure(str(portasMod[doorIndex][i-2]), 1)
				if(flagSendZabbix):
					sendZabbix(ipZabbix, "L03_VTD_PSD_PRT_0"+str(portasMod[doorIndex][i-2]), "erro01", "1")


			if(debug2):
				print (f"Terminou a P{portasMod[doorIndex][i-2]}")
				print ("*********************\n")
			opDoor = 0
			opPeak1 = 0
			opPeak2 = 0
			opTime = 0
			opIndexInit = 0
			opIndexEnd = 0
			meanManCurrOp = 0
			countOpPeak1 = 0
			countOpPeak2 = 0
			count2OpPeak2 = 0
			flagManOpCurr = 0
			clDoor = 0
			clPeak1 = 0
			clPeak2 = 0
			clIndexInit = 0
			clIndexEnd = 0
			clTime = 0
			manClCurr = 0
			countClPeak1 = 0
			countClPeak2 = 0
			closedDoor = 0
			closingDoor = 0
			openedDoor = 0
			flag0 = 0
			flag1 = 0
			flag2 = 0
			flag3 = 0
			kComecoAbertura = 0
			kFinalAbertura = 0
			kComecoFechamento = 0
			kFinalFechamento = 0
			abertura = 0
			fechamento = 0
			begin = 1
			offset = 0


		#shutil.move(ultimoArquivo[:-5]+str(j)+".csv", str(dir)+"/bkp")
		print (f"Terminou o arquivo: {ultimoArquivo}")
		shutil.move(f"{ultimoArquivo}", f"{logsDir}/{dataAtual}/{horaDoLog}/")
	else:
		print(f"Acabou os arquivos tam. ordenados: {len(ordenados)}\nvlw!!")
		break

