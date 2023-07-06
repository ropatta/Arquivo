void verificaSemConexaoZabbix(){
    if (semConexaoZabbix != semConexaoZabbixAnt){
      zabbix_sender("sender.semConexao", String(semConexaoZabbix));
      semConexaoZabbixAnt = semConexaoZabbix;
    }
}

// Zabbix Sender ===============================================================
bool zabbix_sender(String item, String value) {
  int firstLengthByte = 0;
  int secondLengthByte = 0;
  timeout = millis();

  //=========  Concatenação do Payload Json  ==============    
  String zabbixMessagePayload = "{ \"request\":\"sender data\", \"data\":[ ";
  
  zabbixMessagePayload = zabbixMessagePayload +   "{\"host\":\"" + String(clientHostName) + "\",\"key\":\"" + item + "\",\"value\":\"" + String(value) + "\"} ";
  
  zabbixMessagePayload = zabbixMessagePayload + "] }";
  
  for (int tentativa = 1; tentativa <= senderTentativas; tentativa++) {
    // Conecta com Server
    if (client.connect(server, port) == 1) {
      enviado = true;
      
      // Envia cabeçalho
      firstLengthByte = 0;
      secondLengthByte = 0;
      char txtHeader[5] = {'Z', 'B', 'X', 'D', 1};     //ZBXD<SOH>
      client.print(txtHeader);
      
      // Trata e verifica tamanho
      if (zabbixMessagePayload.length() >= 256) {
        if (zabbixMessagePayload.length() >= 65536)  { 
          return;
        }
        else {
          secondLengthByte = zabbixMessagePayload.length() / 256;
          firstLengthByte = zabbixMessagePayload.length() % 256 ;
        }
      }
      else {
        secondLengthByte = 0;
        firstLengthByte = zabbixMessagePayload.length();
      }
      
      // Envia tamanho:
      client.write((byte)firstLengthByte);
      client.write((byte)secondLengthByte);
      client.write((byte)0);
      client.write((byte)0);
      client.write((byte)0);
      client.write((byte)0);
      client.write((byte)0);
      client.write((byte)0);
      client.print(zabbixMessagePayload);
      
      // Timeout =========================================
      while (!(client.available())) {
        unsigned long clientmillis = millis();  
        if (clientmillis - timeout > 5000) {
          timeoutConexaoZabbix++; 
          client.stop();
          return 0;
        }
      } // Fim de Timeout
      
      // Conexão ok ====================================
      while (client.available())    {
        String response = client.readStringUntil('}');  
        tentativa = senderTentativas;
      } // Fim de Conexão ok ===========================
      
    client.stop();  
    }// Fim de Conexão
    
    //No Connection ================================ 
    else  {
      semConexaoZabbix++;
      semConexaoZabbixRst++;
      if (tentativa >= senderTentativas) {
          client.stop(); 
          return 0;
          }
    } //Fim de sem conexão =========================
  
  } // Fim de FOR tentativas
  
  //Desconecta o cliente
  client.stop();
  unsigned long clientmillis = millis(); 
  sender_resp_time = (clientmillis - timeout);
  delay(delayZabbixSender); 
} // Fim de Sender
