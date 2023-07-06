/*Considerações:


SAF_rev4  - implementado rotina de testes para TORRE ciclando o item CONHECE a cada 7 minutos

Host´s TORRE(Testes), BEL, TAT, CAR, PEN, VTD, VPA, PCA, ART

Os numeros MAC vão de 0x74, 0xFE, 0x48, 0x00, 0x01, 0x00 para TORRE
                      0x74, 0xFE, 0x48, 0x00, 0x0A, 0x00 para ITQ
*/


#define TORRE 
// #define BLOCO B                                             
// #define BEL                                              
// #define TAT
//#define CAR
// #define PEN
// #define VTD
// #define VPA
// #define PCA
// #define ART
 //#define ITQ
      
const String senderVersion = "Arduino Zabbix Sender v1.23"; 

#ifdef TORRE
 const byte mac[] = {0x74, 0xFE, 0x48, 0x00, 0x01, 0x00};       
 IPAddress ip(192, 168, 201, 115);                               
 IPAddress gateway(192, 168, 201, 1);                           
 IPAddress subnet(255, 255, 255, 128);                          
 IPAddress myDns(10, 254, 32, 22);                            
 const char* server = "192.168.0.100";                         
 const String clientHostName = "Chiller";              
 const String senderHostname = "PAT-bl B"; 
 int testes = 1;      
#endif  

#ifdef BLOCO B
 const byte mac[] = {0x74, 0xFE, 0x48, 0x00, 0x01, 0x00};       
 IPAddress ip(192, 168, 201, 12);                               
 IPAddress gateway(192, 168, 201, 1);                           
 IPAddress subnet(255, 255, 255, 192);                          
 IPAddress myDns(10, 254, 32, 22);                            
 const char* server = "10.254.32.33";                         
 const String clientHostName = "L03_BEL_SAF";              
 const String senderHostname = "L03_BEL_SAF"; 
 int testes = 0;      
#endif 

#ifdef BEL
 const byte mac[] = {0x74, 0xFE, 0x48, 0x00, 0x02, 0x00};      
 IPAddress ip(10, 254, 44, 215);                               
 IPAddress gateway(10,254,44,193);                           
 IPAddress subnet(255, 255, 255, 192);                         
 IPAddress myDns(10, 254, 32, 22);                              
 const char* server = "10.254.32.33";                          
 const String clientHostName = "L03_BEL_SAF";                
 const String senderHostname = "L03_BEL_SAF"; 
 int testes = 0;      
#endif  

#ifdef TAT
 const byte mac[] = {0x74, 0xFE, 0x48, 0x00, 0x03, 0x00};       
 IPAddress ip(10, 254, 45, 23);                                 
 IPAddress gateway(10, 254, 45, 01);                             
 IPAddress subnet(255, 255, 255, 192);                            
 IPAddress myDns(10, 254, 32, 22);                               
 const char* server = "10.254.32.33";                           
 const String clientHostName = "L03_TAT_SAF";                  
 const String senderHostname = "L03_TAT_SAF"; 
 int testes = 0;      
#endif  

#ifdef CAR
 const byte mac[] = {0x74, 0xFE, 0x48, 0x00, 0x04, 0x00};       
 IPAddress ip(10, 254, 45, 87);                                
 IPAddress gateway(10, 254, 45, 65);                           
 IPAddress subnet(255, 255, 255, 192);                          
 IPAddress myDns(10, 254, 32, 22);                             
 const char* server = "10.254.32.33";                           
 const String clientHostName = "L03_CAR_SAF";                 
 const String senderHostname = "L03_CAR_SAF"; 
 int testes = 0;
#endif  

#ifdef PEN
 const byte mac[] = {0x74, 0xFE, 0x48, 0x00, 0x05, 0x00};     
 IPAddress ip(10, 254, 46, 23);                               
 IPAddress gateway(10, 254, 46, 01);                           
 IPAddress subnet(255, 255, 255, 192);                          
 IPAddress myDns(10, 254, 32, 22);                             
 const char* server = "10.254.32.33";                         
 const String clientHostName = "L03_PEN_SAF";                
 const String senderHostname = "L01_JAB_X01_SMA_ELP_001_TESTE";
 int testes = 0;
#endif

#ifdef VTD
 const byte mac[] = {0x74, 0xFE, 0x48, 0x00, 0x06, 0x00};     
 IPAddress ip(10, 254,46, 87);                               
 IPAddress gateway(10, 254, 46, 65);                           
 IPAddress subnet(255, 255, 255, 192);                          
 IPAddress myDns(10, 254, 32, 22);                             
 const char* server = "10.254.32.33";                         
 const String clientHostName = "L03_VTD_SAF";                
 const String senderHostname = "L03_VTD_SAF";
 int testes = 0;
#endif

#ifdef VPA
 const byte mac[] = {0x74, 0xFE, 0x48, 0x00, 0x07, 0x00};     
 IPAddress ip(10, 254, 46, 151);                               
 IPAddress gateway(10, 254, 46, 129);                           
 IPAddress subnet(255, 255, 255, 192);                          
 IPAddress myDns(10, 254,32,22);                             
 const char* server = "10.254.32.33";                         
 const String clientHostName = "L03_VPA_SAF";                
 const String senderHostname = "L03_VPA_SAF";
 int testes = 0;
#endif

#ifdef PCA
 const byte mac[] = {0x74, 0xFE, 0x48, 0x00, 0x08, 0x00};     
 IPAddress ip(10, 254, 46, 215);                               
 IPAddress gateway(10, 254, 46, 193);                           
 IPAddress subnet(255, 255, 255, 192);                        
 IPAddress myDns(10, 254, 32, 22);                       
 const char* server = "10.254.32.33";             
 const String clientHostName = "L03_PCA_SAF";          
 const String senderHostname = "L03_PCA_SAF";
 int testes = 0;
#endif

#ifdef ART
 const byte mac[] = {0x74, 0xFE, 0x48, 0x00, 0x09, 0x00};     
 IPAddress ip(10, 254, 47, 23);                               
 IPAddress gateway(10, 254, 47, 1);                           
 IPAddress subnet(255, 255, 255, 192);                         
 IPAddress myDns(10, 254, 32, 22);                             
 const char* server = "10.254.32.33";                         
 const String clientHostName = "L03_ART_SAF";                
 const String senderHostname = "L03_ART_SAF";
 int testes = 0;
#endif

#ifdef ITQ
 const byte mac[] = {0x74, 0xFE, 0x48, 0x00, 0x0A, 0x00};     
 IPAddress ip(10, 254, 47, 87);                               
 IPAddress gateway(10, 254, 47, 65);                           
 IPAddress subnet(255, 255, 255, 192);                         
 IPAddress myDns(10, 254, 32, 22);                             
 const char* server = "10.254.32.33";                         
 const String clientHostName = "L03_ITQ_SAF";                
 const String senderHostname = "L03_ITQ_SAF";
 int testes = 0;
#endif


