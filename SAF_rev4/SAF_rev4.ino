
#include <avr/wdt.h>
#include <Ethernet.h>
#include "config.h"

const int port = 10051;             
EthernetClient client;
String item[] = { "FURTO_LESTE", "FURTO_OESTE", "RECONHE"};
int entradas[] = {22, 24, 26};
int pinCount = 3;                 
bool valores[3] = {0,0,0};
int valoresAnt[3] = {0,0,0};
       
const unsigned delayZabbixSender = 0;   
unsigned long timeout = 0;
unsigned long sender_resp_time = 0;
unsigned long semConexaoZabbix = 0;
unsigned long semConexaoZabbixAnt = 0;
unsigned long semConexaoZabbixRst = 0;
unsigned long timeoutConexaoZabbix = 0;
unsigned long tempo1,dif;

boolean enviado = false;

String zabbixMessagePayload = "";
const int senderTentativas = 5;

void setup() {
  tempo1 = millis();
  Serial.begin(115200);
  configEthernet();
  configuraEntradas();
   //delay(0);
  Serial.print("Tentando Sender.");
  while ((zabbix_sender("sender.uptime", "0")) == 0) {
      Serial.print(".");
      delay(1000);
      }
  Serial.println("\nComunicação ok!!");
  semConexaoZabbix = 0;
  semConexaoZabbixRst = 0;
  wdt_enable(WDTO_8S);
}

void loop() {
  dif = millis() - tempo1;
  if(dif > 60000) {
      enviaTodosValores();
      tempo1 = millis();
    }
    
  wdt_reset(); 
  verificaSemConexaoZabbix();
  verificaEntrada();
}

void configuraEntradas() {
  for (int thisPin = 0; thisPin < pinCount; thisPin++) {pinMode(entradas[thisPin], INPUT_PULLUP);}
}

void configEthernet() {
  Ethernet.begin(mac, ip, myDns, gateway, subnet);
  Serial.println("IP do Proxy: " + String(server));
  Serial.println("Hostname: " + String(clientHostName));
  Serial.println("Nome Visivel: " + String(senderHostname));
  Serial.println(senderVersion);    
  Serial.println(F("\nConfigurando Ethernet..."));
  Serial.println(Ethernet.localIP());
  Serial.println(Ethernet.subnetMask());
  Serial.println(Ethernet.gatewayIP());
}

void enviaTodosValores() {
  
    for (int thisPin = 0; thisPin < pinCount; thisPin++) {
        delay(2000);
        zabbix_sender(item[thisPin], String(valores[thisPin]));
        Serial.print(item[thisPin]);
        Serial.print(" Enviou para zabbix  ");
        Serial.println(valores[thisPin]);
      }
}

void verificaEntrada() {
  for (int thisPin = 0; thisPin < pinCount; thisPin++) {
    valores[thisPin] = digitalRead(entradas[thisPin]);
  }
  for (int thisPin = 0; thisPin < pinCount; thisPin++) {
    if (valores[thisPin] != valoresAnt[thisPin]) {
      valoresAnt[thisPin] = valores[thisPin];

        zabbix_sender(item[thisPin], String(valores[thisPin]));
              Serial.print(item[thisPin]);
              Serial.print(" Enviou alteracao! ");
              Serial.println(valores[thisPin]); 
    }
  }
  delay(100);
}

void software_Reset() {
  asm volatile ("  jmp 0");  
}

void (*funcReset)() = 0;
