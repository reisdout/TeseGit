/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

 //=====================================================================================
  /*Os roteadores são alocados dianicamente em função do número de redes.
  //Considerando-se que cada roteador pode agregar até 4 redes
  //Assim seria a topologia para 6 redes, por exemplo:

  //Agora serão utilizados os arquivos model-flow e model-topology, gerados por
  topogen.py. Esses arquivos são da seguinte forma
model-topology:
0 1 1000Mb 2.377715e+01ms
1 2 1000Mb 1.089356e+01ms
2 3 1000Mb 4.997695e-01ms
3 4 1000Mb 1.312409e+01ms
5 0 1000Mb 5.714590e-01ms
6 3 1000Mb 9.470218e-01ms
7 1 1000Mb 7.801727e+00ms
cujas linhas são traduzidas da seguinte forma
linhas pares->São transmissores de pacores (sources (src)), portando devem ser dotados 
de aplicações clientes. 
linhas ímpares->São receptores de pacores (sources (src)), portando devem ser dotados 
de aplicações servidoras.

coluna 1->identifica os terminais, hosts
coluna2->identifica os rotadores, núcleo
coluna 3 e 4 -> velocidade e delay, respectivamente, da ligação entre o host 
e o rotrador

Seguindo o model-topology acima, teríamos:
  // 
  
(10.0.0.6)  (10.1.0.1)   (10.1.1.8)                  (10.3.1.7)
   H5           H0          H7                        H6 
     \            \         /  (10.2.0.2)  (10.3.0.3) /
      p2p         p2p    p2p    H1           H2      /     H3(10.4.0.5)
        \____        \____/       \____        \____/       \____
        |    |(20.1) |    |       |    |       |    |       |    |
        | R0 |--p2p--| R1 |--p2p--| R2 |--p2p--| R3 |--p2p--| R4 |
        |____|       |____|       |____|       |____|       |____|
                                                                                            
                                                                                               
  *A lógica dos rendereços é: 10."Roteador"."vertice do roteador"."x"
  Ex.: 10.0.0.6
          | | |
          | | |x -> distribuído automaticamente pelo ns3, dentro de cada rede
          | |
          | vértice 0
          R0
  Todos os enlaces serão p2p.
                               
  */

  //===================================================================================== 

//float time_cwd_size_change[2500];
//unsigned int num_time_cwd_size_change = 0.0;
//unsigned int cwd_size [2500];
//unsigned int num_cwd_size = 0;
//float last_measure = 0.0;

#include <fstream>
#include "ns3/core-module.h"
#include "ns3/config-store-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"

#include "ns3/tcp-option-ts.h"
#include "ns3/rtt-estimator.h"

#include "ns3/error-model.h"
#include "ns3/tcp-header.h"
#include "ns3/udp-header.h"
#include "ns3/enum.h"
#include "ns3/event-id.h"
#include "ns3/flow-monitor-helper.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/traffic-control-module.h"
#include "ns3/flow-monitor-helper.h"

/*My includes*/

#include <algorithm>
#include <string>
#include <vector>
#include "ns3/csma-module.h"
#include "ns3/point-to-point-module.h"
#include <iostream>
#include <sstream> 
#include <ctime>
#include <memory>
#include <map>


#include "./keras2cpp/src/model.h"



using keras2cpp::Model;
using keras2cpp::Tensor;





/*My defines*/
/*
Grupo é a rede que se forma, plugada no vétice do roteador, que por enquanto tem só um terminal e, potanto
dois devices, um no terminal e outro no roteador
A princípio, é um terminal por porta do roteador
*/

#define PARKINGLOT_TOPOLOGY 0

#define DUMBELL_TOPOLOGY 1


#define ROUTER_PORTS 100
#define MAX_ROUTERS 3
#define MAX_TERMINALS ROUTER_PORTS*MAX_ROUTERS
//#define MAX_NUM_CSMA_GROUPS 4*MAX_ROUTERS //Obsoleto, utilizado numa abordagem antiga
#define MAX_NUM_DEVICES 8*MAX_ROUTERS //Dois devices para cada cada grupo, "pendurados no vétice do roteador"
#define MAX_NUM_CSMA_INTERFACES 8*MAX_ROUTERS //Duas interfaces para cada cada grupo
//#define NUM_TERMINALS_REDE 1
#define UDP_PORT 9

#define MAXROUTERBUFFERSIZE 100





using namespace ns3;
using namespace std;


//Flow Types

#define VERYSHORT_FLOW 0
#define SHORT_FLOW 1
#define LONG_FLOW 2


//bool verboseSink = false;

//Experiment (exp) Parameters

char topology = DUMBELL_TOPOLOGY;//0-parking lot; 1-pincel

bool packetControl=true;

/*
A grande diferença em relação é que na DUMBELL, o Receptor pega a fila do terminal em que
está ligado. É por isso que é necessário fazer distinção quando se recupera as filas do roteador

*/

/*
  destination nodes link speed. Must be set in model flow
  essa variável é só para colocar no preambulo do arquivo de dados de treinamento
*/

std::string expBottleNeck = "2Mb"; //destination nodes link speed. Must be set in model flow
//float expWeightExpon = 1.0/8.0;//sampleRTT = (1-weightExpon)sampleRTT+weightExpon*RTT
float expWeightExpon = 1.0/8.0;//sampleRTT = (1-weightExpon)sampleRTT+weightExpon*RTT
uint32_t expPacketSize = 1040;
uint64_t expShortFileSize[] = {10000,100000}; // Amazon Total Page Size - 4.06MB, by https://gtmetrix.com
uint64_t expLongFileSize =  4000000000;/*40000;*/ //4GB
double expSimulationTime = 180*60.0;//120*60.0;
uint32_t expNumShortFlows = 100;
uint32_t expNumlongFlows = 40;
uint32_t expContNumShortFlows = 0;//controla a quantidade para que não ultrapasse a expNumShortFlows
uint32_t expContNumLongFlows = 0;////controla a quantidade para que não ultrapasse a expNumlongFlows
std::string expAppDataRate = "1Mbps"; //Datarate da Aplicação
//A quantidade de pacotes a ser enviada por aplicação (expMaxSentPacket) seria, teroricamente, a quantidade
//de dados a ser enviada distribuída pelos pacotes (expPacketSize)
uint64_t expMaxSentPacket = expLongFileSize/expPacketSize +1;
//Tempo entre envios, está obsoleto, pois agora o terminal envia até esgotar o buffer de transmissão
// ver comentário abaixo de MyApp::SendPacket
double expPacketSentSchedule = 2.0;
//bytes_to_transmit = datarate*similationTime/8
//expNPackets = bytes_to_Transmit/packet_size
//rtt.substr(0,rtt.length()-3)

//Seria o total de pacotes máximo enviado por uma aplicação, caso
//aproveitasse ao máximo toda possibilidade ao longo do tempo de experimento
//é calculado em  SetMaxPackets()
uint64_t expNPackets;

//Tamanho do SegmentSize. Por enquanto 24/02/2023 sem serventia, pois, de fato,
//se utiliza o default
uint32_t expSegSize;
//Seria o total de agendamentos de transmissão. Obsoleto devido a transmissão
//até esgotar o buffer
int globalSchedule = 0; 

NodeContainer routers; //É um gerador de nós a serem utilizados como roteadores
NodeContainer terminals; //É um gerador de nós a serem utilizados como terminais

//=====================================================================================
 /*
  O vetor a seguir faz associação entre o id da Aplicação e o fluxo por ela
  servido. hashIdAppAppFlow[2][0] hashIdAppAppFlow[2][1] guarda, respectivamente,
  o srcId e o destId do fluxo servido   
 */
//=====================================================================================
  
unsigned hashIdAppAppFlow[MAX_TERMINALS][2];

PointToPointHelper pointToPointEnlaceTerm[MAX_TERMINALS][MAX_ROUTERS]; //Define a quantidade de enlaces, em que cada um deles liga umpointToPointNodesPairsTerm
//NodeContainer pointToPointNodesPairsTerm[MAX_NUM_CSMA_GROUPS];
NodeContainer pointToPointNodesPairsTerm[MAX_TERMINALS][MAX_ROUTERS];
NetDeviceContainer pointToPointDevicesTerm[MAX_TERMINALS][MAX_ROUTERS];
Ipv4InterfaceContainer pointToPointInterfacesTerm[MAX_TERMINALS][MAX_ROUTERS];



PointToPointHelper pointToPointRouters[MAX_ROUTERS][MAX_ROUTERS];
NodeContainer pointToPointNodesPairsRouters[MAX_ROUTERS][MAX_ROUTERS];//[1][2] detem a ligação entre 
                                                                        //os roteadores 1 e 2
NetDeviceContainer pointToPointDevicesRouters[MAX_ROUTERS][MAX_ROUTERS];
Ipv4InterfaceContainer pointToPointInterfacesRouters[MAX_ROUTERS][MAX_ROUTERS];

int numTerminals;
int numRouters;
std::string bufferUnit;

int numInterfacesUsadasNoRoteador[MAX_ROUTERS];
InternetStackHelper stack;

char tipoFluxo[MAX_TERMINALS][MAX_TERMINALS];

bool verboseSink = false;

bool verboseFile = false;

bool verboseFileTreino = true;

bool verboseAllConfigParar = true;

int numActiveFlows = 0;

int activeFlows[MAX_TERMINALS*MAX_TERMINALS][2];

//State Variables. One of them for each flow

int64_t flowStartTime[MAX_TERMINALS][MAX_TERMINALS];

int64_t marcaTempoChegadaAckAnterior[MAX_TERMINALS][MAX_TERMINALS];

int64_t lastIntervalBetweenAcks[MAX_TERMINALS][MAX_TERMINALS];

int64_t marcaTempoRefletidaAckAnterior[MAX_TERMINALS][MAX_TERMINALS] ;//= Seconds(0.0).GetInteger();

int64_t lastIntervalBetweenTS[MAX_TERMINALS][MAX_TERMINALS];

int64_t minAckRtt[MAX_TERMINALS][MAX_TERMINALS];

uint32_t lastSeq[MAX_TERMINALS][MAX_TERMINALS];

//Guarta os instantes em que a cwnd é zero, para que no treino não sejam armazenados dados do slow start
int64_t lastTimeCwndIsZero[MAX_TERMINALS][MAX_TERMINALS];

unsigned globalAppId = 0;

unsigned numAckReceived[MAX_TERMINALS][MAX_TERMINALS];

double lastAck_ewma [MAX_TERMINALS][MAX_TERMINALS];

double lastSend_ewma [MAX_TERMINALS][MAX_TERMINALS];

double lastRouterQueue_ewma[MAX_TERMINALS][MAX_TERMINALS];

uint32_t lastCwnd[MAX_TERMINALS][MAX_TERMINALS];

uint32_t lastRouterOcupation[MAX_TERMINALS][MAX_TERMINALS];//Guada a última ocupação do roteado, a fim de obter a sia variação

int assTerminalRoteador[MAX_TERMINALS];//Guarda a associação entre terminais e roteadores

float online = true; // utilizando algum modelo efetivamente.

std::string workDir = "/home/visitante/ns-3.35/bake/source/ns-3.35/scratch/TCP-Evaluation-Suite/TCP-Evaluation-Suite-Topology-TCP-cwd";


// Initialize model.
auto model = Model::load(workDir+"/models/training_client01_01_40L_180_min_1M_250K_150K_100K.model"); //código inspirado no keras2cpp

// Create a 1D Tensor on length 4 for input data.
Tensor in{4};


void print_map(std::string comment, const std::map<uint32_t, uint32_t>& m)
{
    std::cout << comment;
    // iterate using C++17 facilities
    //for (const auto& [key, value] : m)
        //std::cout << '[' << key << "] = " << value << "; ";
 
// C++11 alternative:
  for (const auto& n : m)
      std::cout << n.first << " = " << n.second << "; ";
//
// C++98 alternative
//  for (std::map<std::string, int>::const_iterator it = m.begin(); it != m.end(); it++)
//      std::cout << it->first << " = " << it->second << "; ";
 
    std::cout << '\n';
}



void InitStateVariables()
{

  for (int i=0; i < MAX_TERMINALS; i++)
    for (int j=0; j < MAX_TERMINALS; j++)
    {
      flowStartTime[i][j] = MilliSeconds(0.0).GetInteger();
      marcaTempoChegadaAckAnterior[i][j] = MilliSeconds(0.0).GetInteger();
      lastIntervalBetweenAcks[i][j] = MilliSeconds(0.0).GetInteger();
      marcaTempoRefletidaAckAnterior[i][j] = MilliSeconds(0.0).GetInteger();
      lastIntervalBetweenTS[i][j] = MilliSeconds(0.0).GetInteger();
      lastTimeCwndIsZero[i][j] = MilliSeconds(0.0).GetInteger();
      minAckRtt[i][j] = MilliSeconds (30000.0).GetInteger();//Para garantir que o primeiro é mínimo
      numAckReceived[i][j] = 0;
      lastAck_ewma[i][j] = 0.0;
      lastSend_ewma[i][j] = 0.0;
      lastRouterQueue_ewma[i][j] = 0.0;
      lastCwnd[i][j] = 0;
      lastSeq[i][j] = 0;
      lastRouterOcupation[i][j] = 0;
      activeFlows[i*MAX_TERMINALS+j][0]=-1;
      activeFlows[i*MAX_TERMINALS+j][1]=-1;

    }

  for(int i =0; i < MAX_TERMINALS;i++)
    assTerminalRoteador[i]=-1;//Valor default. Quem é -1 não está associado a roteador algum.

  for(int i = 0; i < MAX_ROUTERS; i++)
  {
    numInterfacesUsadasNoRoteador[i] = 0;
  }


}

void myPause()
{
  cin.clear();
  std::cout << "\n" << "Pressione qualquer Tecla para continuar";
  cin.ignore();
}

  




NS_LOG_COMPONENT_DEFINE ("FifthScriptExample");




/*
class MySocket : public Socket
{
public:

  MySocket ();
  virtual ~MySocket();
  void ProcessAck(const SequenceNumber32 & ackNumber,		
                  bool  	scoreboardUpdated,
		              uint32_t  	currentDelivered,
		              const SequenceNumber32 &  	oldHeadSequence );
  void Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate);


  int GetIdSrc(){return idSrc;};

  int GetidDestination(){return idDestination;};

  void SetIdSrc(int parIdSrc){idSrc = parIdSrc;}

  void SetIdDestination(int parIdDestiantion){idDestination = parIdDestiantion;};

  
private:
  int idSrc, idDestination;
  
};

MySocket::MySocket ()
  : idSrc (0), 
    idDestination (0)
{
}
*/

/*
class MySocket : public TcpSocketBase
{
public:

  MySocket (TcpSocketBase parSocket);
  virtual ~MySocket();  
  Ptr< TcpCongestionOps > getCongestionControlAlgorithm() const;
};


MySocket::MySocket (TcpSocketBase parSocket) : TcpSocketBase(parSocket)
{
}

 Ptr< TcpCongestionOps > MySocket::getCongestionControlAlgorithm() const
 {
   return this->m_congestionControl;
 
 }

MySocket::~MySocket(){}

*/

//Observar como fica vários arquivos no ns3

void ReturnTx(Ptr<Socket> localSocket, uint32_t parIdApp);

uint64_t WriteUntilBufferFull (Ptr<Socket> parSocket,  uint64_t parPacketSent,  
                           uint64_t parNPacket, uint32_t parPacketSize, uint32_t txSpace)
{

  //cout << "inside WriteUntilBufferFull parPacketSent: " << parPacketSent << "\n";
  //cout << "inside WriteUntilBufferFull parNPacket: " << parNPacket << "\n";
  uint64_t packetSent = parPacketSent;
  uint64_t npacket = parNPacket;
  int amountSent;
  
  while (packetSent < npacket && parSocket->GetTxAvailable () > 0) 
  {
    //cout << "inside WriteUntilBufferFull packetSent: " << packetSent << "\n";
    //cout << "inside WriteUntilBufferFull npacket: " << npacket << "\n";
    //cout << "inside WriteUntilBufferFull GetTxAvailable: " << parSocket->GetTxAvailable () << "\n";
    
    Ptr<Packet> packet = Create<Packet> (parPacketSize);
    amountSent = parSocket->Send (packet);
    //cout << "inside WriteUntilBufferFull amountSent: " << amountSent << "\n";
    if(amountSent < 0)
    {
       // we will be called again when new tx space becomes available.
       //cout << "inside WriteUntilBufferFull packetSent: " << packetSent << "\n";
       //return packetSent;
       break;
    }

    packetSent++;
  }
  return packetSent; //nothing sent....
}



class MyApp : public Application 
{
public:

  MyApp ();
  virtual ~MyApp();

  void Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, DataRate dataRate, uint64_t parFileSize);
  void ScheduleTx (void);

  uint64_t getNPacket()
  {
    return m_npackets;
  }

  void setNPacket(uint64_t parNpacket)
  {
    m_npackets = parNpacket;
  }

  uint64_t getPacketSent()
  {
    return m_packetsSent;
  }

  void setPacketSent(uint64_t parPacketSent)
  {
    m_packetsSent = parPacketSent;
  }

  Ptr<Socket> getSocket()
  {
       return m_socket;
  }    


  uint32_t getPacketSize()
  {
    return m_packetSize;
  }

  void setPacketSize(uint32_t parpacketSize)
  {
    m_packetSize = parpacketSize;
  }

//pendingTransmission

  bool getPendingTransmission()
  {
    return pendingTransmission;
  }

  void setPendingTransmission(bool parPendingTransmission)
  {
    pendingTransmission = parPendingTransmission;
  }

//pendingTransmission




  int getFlowType()
  {
    return m_flow_type;
  }

  void setFlowType(int parFlowType)
  {
    m_flow_type = parFlowType;
  }


  unsigned getAppId()
  {
    return m_appid;
  }


//m_stopTime

  Time getStopTime()
  {
    return m_stopTime;
  }


//m_stopTime



  void AssociateSeqQueueSize(uint32_t parSeq, uint32_t parQueueSize)
  {
     //cout << "Associando " << "("<< parSeq<<","<< parQueueSize<<")\n";
     m_seq_queue[parSeq] = parQueueSize;
  }
  uint32_t GetAssociateQueueSize(uint32_t parSeq)
  {
    //cout << "Getting " << parSeq << "\n";
    uint32_t router_queue_size = m_seq_queue[parSeq];
    for (auto it = m_seq_queue.begin(); it != m_seq_queue.end();)
    {
        if (it->first <= parSeq)
            it = m_seq_queue.erase(it);
        else
            ++it;
    }
    //print_map("\n\nMais uma deleção: ",m_seq_queue);
    return router_queue_size;


  }

  void SendPacket (void);
        
private:
  virtual void StartApplication (void);
  virtual void StopApplication (void);

  

  //void SendPacket (void);

  Ptr<Socket>     m_socket;
  Address         m_peer;
  uint32_t        m_packetSize;
  uint64_t        m_npackets;
  DataRate        m_dataRate;
  EventId         m_sendEvent;
  bool            m_running;
  uint64_t        m_packetsSent;
  uint64_t        m_fileSize; //given in Bytes
  unsigned        m_appid;
  uint64_t        m_packet_sent_last_round;
  int             m_flow_type; //0-very low; 1-low; 2-high
  // Create a map of three (uint32_t, float) pairs to save the time a package is sent
  std::map<uint32_t, uint32_t> m_seq_queue;
  bool pendingTransmission;
};

MyApp::MyApp ()
  : m_socket (0), 
    m_peer (), 
    m_packetSize (0), 
    m_npackets (0), 
    m_dataRate (0), 
    m_sendEvent (), 
    m_running (false), 
    m_packetsSent (0),
    m_fileSize(0),
    m_appid(0),
    m_packet_sent_last_round(0),
    m_flow_type(0),
    pendingTransmission(false)

{
}

MyApp::~MyApp()
{
  m_socket = 0;
}

void
MyApp::Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, DataRate dataRate,uint64_t parFileSize)
{
  m_socket = socket;
  m_peer = address;
  m_packetSize = packetSize;
  m_dataRate = dataRate;
  m_fileSize = parFileSize;
  m_npackets = (m_fileSize/m_packetSize)+1;
  m_appid = globalAppId;
  globalAppId++;
  /*cout  << "m_packetsize: "  << m_packetSize << "\n";
  cout  << "m_filesize: "  << m_fileSize << "\n";
  cout  << "m_npackets: "  << m_npackets << "\n";
  cout  << "bitRate: "  << m_dataRate.GetBitRate() << "\n";
  myPause();*/
}

void
MyApp::StartApplication (void)
{
  m_running = true;
  m_packetsSent = 0;
  m_socket->Bind ();
  m_socket->Connect (m_peer);
  std::cout <<this->GetNode()->GetId()<<" ," << Simulator::Now().GetSeconds()<< " ," <<  "Tx Available: " << m_socket->GetTxAvailable() << "\n";
  SendPacket ();
  
}



void 
MyApp::StopApplication (void)
{
  m_running = false;



  if (m_sendEvent.IsRunning ())
    {
      Simulator::Cancel (m_sendEvent);
    }

  if (m_socket)
    {
      m_socket->Close ();
    }

    std::cout <<"Aplicação em " <<this->GetNode()->GetId()<<"  terminou em " << Simulator::Now().GetSeconds()<< "\n";
}

void 
MyApp::SendPacket (void)
{
  //Ptr<Packet> packet = Create<Packet> (m_packetSize);
 // m_socket->Send (packet);
  cout << "Nó " <<this->GetNode()->GetId() << "Enviando pacotes...\n";
  //myPause();
  if(packetControl)
  {
    if (++m_packetsSent < m_npackets)
    {
      m_packet_sent_last_round=m_packetsSent;
      //cout << "App " << m_appid << "enviando\n";
      m_packetsSent = WriteUntilBufferFull (m_socket, m_packetsSent, m_npackets, m_packetSize, m_socket->GetTxAvailable ());
      m_socket->SetSendCallback (MakeCallback (&ReturnTx));
    }
  
    else
    {
      cout << "Nó " <<this->GetNode()->GetId() << "enviou todos os seus" << m_packetsSent <<  "pacotes...\n";
      m_socket->ShutdownSend();
      //myPause();
    }
  }

  else
  {
    m_packet_sent_last_round=m_packetsSent;
    //cout << "App " << m_appid << "enviando\n";
    m_packetsSent = m_packetsSent + WriteUntilBufferFull (m_socket, m_packetsSent, m_npackets, m_packetSize, m_socket->GetTxAvailable ());
    m_socket->SetSendCallback (MakeCallback (&ReturnTx));

  }

}

  
/*=====================================================================================
 O código acima foi substutuída pelas linhas abaixo, retiradas de  
 https://www.nsnam.org/docs/release/3.25/doxygen/tcp-large-transfer_8cc_source.html,
 que promete simular uma transmissão
 de arquivo, enviando pacotes enquanto o buffer permitir.
 Interessante notar o método SetSendCallback, que, segundo
 https://www.nsnam.org/docs/release/3.25/doxygen/classns3_1_1_socket.html#a85ff5c8cc7d242823f301b49264c68a4
 notifica a aplicação quando há buffer disponível
 =====================================================================================
NS_LOG_LOGIC ("Starting flow at time " <<  Simulator::Now ().GetSeconds ());
// tell the tcp implementation to call WriteUntilBufferFull again
// if we blocked and new tx buffer space becomes available
m_socket->SetSendCallback (MakeCallback (&WriteUntilBufferFull));
m_packetsSent += WriteUntilBufferFull (m_socket, m_packetsSent,m_npackets, m_packetSize, m_socket->GetTxAvailable ());
*/
 //if (++m_packetsSent < m_npackets)
 /*
   if (m_packetsSent < m_npackets)
   {
    cout << "App " << m_appid << " lastRound: "  << m_packet_sent_last_round << "\n"; 
    cout << "App " << m_appid << " agendando o pacote " << m_packetsSent << "\n"; 
     ScheduleTx ();
   }
 */
   


 //ScheduleTx ();



void 
MyApp::ScheduleTx (void)
{
  Time tNext;
  std::cout << "App " << m_appid << " Inside ScheduleTx lastRound: "  << m_packet_sent_last_round << "\n"; 
  std::cout << "App " << m_appid << " Inside ScheduleTx agendando o pacote " << m_packetsSent << "\n"; 

  if (m_running)
    {
 
     //ScheduleTx ();
     //Time tNext (Seconds (m_packetSize * 8 / static_cast<double> (m_dataRate.GetBitRate ())));
     if(m_packetsSent > m_packet_sent_last_round)
      tNext =  Seconds ((m_packetsSent-m_packet_sent_last_round) * m_packetSize * 8 / static_cast<double> (m_dataRate.GetBitRate ()));
     else
      tNext =  Seconds (m_packetsSent * m_packetSize * 8 / static_cast<double> (m_dataRate.GetBitRate ()));
     //if((Simulator::Now() + tNext) < Seconds(expSimulationTime))
     m_sendEvent = Simulator::Schedule (tNext, &MyApp::SendPacket, this);
      
    }
}



class AppPool  
{
public:

  AppPool ();
  ~AppPool();
  /*=====================================================================================
  ######################SonumInterfacesUsadasNoRoteadorpois cada fluxo corresponde a uma aplicação. Além disso a ideia
  é mapear  os fluxos na matriz, de forma que a linha é o source e a coluna é o destination.
  Essa será a regra geral em todas as marizes que agregarem nós
  Deve-se lembrar, entretanto, que é no destin  que se deve instalar o servidor
  Por exemplo, se tivermos a seguinte linha de configuração no model-flow
  5 6 3 1
  será instanciado um serverApps[5][6] e um UdpEchoServerHelper[5][6], que serão
  instalados no nó 6.
  Essa filosofia também rege o preenchimento do vetor tipoFluxo[MAX_TERMINALS][MAX_TERMINALS]
  Essa lógica está a partir da linha abaixo do seguinte comentário

  //#00000001
  =====================================================================================*/

  ApplicationContainer serverApps[MAX_TERMINALS][MAX_TERMINALS];
  PacketSinkHelper *tcpSinkServer[MAX_TERMINALS][MAX_TERMINALS];

/*=====================================================================================
 Mesma lógica dos servidores
 Não se deve esquecer que na instanciação dos clientes,
 deve-se dizer o endereço do servidor
 //UdpEchoClientHelper echoClient (csmaInterfaces[idRedeServidor].GetAddress(idServidorNaRede), UDP_PORT);
=====================================================================================*/
  //ApplicationContainer clientApps[MAX_TERMINALS][MAX_TERMINALS];

/*=====================================================================================
 Agora, os Apps dos clientes serão da classe myApp, é equivalente a aplicação
=====================================================================================*/
  Ptr<MyApp> clientApps[MAX_TERMINALS][MAX_TERMINALS];


 // UdpEchoClientHelper *echoClient[MAX_TERMINALS][MAX_TERMINALS];//Every packet sent should be returned by the server and received here
 /*=====================================================================================
 Agora, em vez de funcionar o UdpEchoClientHelper funcionará um  ns3TcpSocket 
 nos cliente, que passa a ser equivalente ao helper
=====================================================================================*/ 
  Ptr<Socket> tcpClientSocket [MAX_TERMINALS][MAX_TERMINALS];

  void FinalizarEchoServer();
  //void InicializarTCPSinkServers(/*PacketSinkHelper *parTCPSinkServer[][MAX_TERMINALS]*/);
  void InicializarTCPSinkServers();
  void ScheduleTx();  


};

AppPool::AppPool()
{
  InicializarTCPSinkServers();
  //ScheduleTx();
}

AppPool::~AppPool()
{
  //FinalizarEchoServer(netApps.tcpSinkServer);
  FinalizarEchoServer();
  std::cout << "Servidores finalizados com Sucesso!!"<<"\n";

}

void AppPool::InicializarTCPSinkServers()
{

  for(int i=0; i < MAX_TERMINALS; i++)
    for(int j=0; j < MAX_TERMINALS; j++)
      this->tcpSinkServer[i][j]=0;

  std::cout << "InicializarTCPSinkServers OK\n";
}

void AppPool::FinalizarEchoServer()
{
  
 for(int i=0; i < MAX_TERMINALS; i++)
  for(int j=0; j < MAX_TERMINALS; j++)
  {
    if(tcpSinkServer [j][i])
    {
      delete tcpSinkServer[j][i];
      break;
    }
  }
   
}

void AppPool:: ScheduleTx()
{
  
  globalSchedule++;
  std::cout << "GlobalSchedule: " << globalSchedule << "\n";
  
  if(Simulator::Now().GetSeconds() > 5.0 && Simulator::Now() < Seconds(expSimulationTime))
  {
      for (int i=0; i < numActiveFlows;i++)
        for(int j = 0; j<1000; j++)
        {
          this->clientApps[activeFlows[i][0]][activeFlows[i][1]]->ScheduleTx();
        }
      std::cout << "Agendada Transmissões!!!\n";
  }

  Time tNextScheduleTx (Seconds (expPacketSentSchedule));
  if(Simulator::Now()+tNextScheduleTx < Seconds(expSimulationTime))
  {
    Simulator::Schedule (tNextScheduleTx, &AppPool::ScheduleTx, this);
    std::cout << "Agendada Previsao de Transmissão!!!\n";

  }

}

AppPool netApps;


void TranmissionTrigger(MyApp * parMyApp)
{
  //uint32_t transmissionNode = parMyApp->GetNode()->GetId();
  //if(transmissionNode==2)
    //cout << "Transmission  in " << Simulator::Now().GetSeconds() << "\n";
  parMyApp->SendPacket();
  parMyApp->setPendingTransmission(false);
}


void ReturnTx(Ptr<Socket> parSocket, uint32_t parBufferTx)
{
  uint32_t AppsSrc = parSocket->GetNode()->GetNApplications();
  uint32_t idNode = parSocket->GetNode()->GetId();
  //if(idNode ==2)
    //cout << "Nó " << parSocket->GetNode()->GetId() << " voltando a transmitir\n"; 
  Ptr<Application> ptrApp;
  //Ptr<MyApp> ptrMyApp;
  /*=====================================================================================
    Acrescentando um tempo aleatório para se evitar monopolização
  =====================================================================================*/ 
  Time tNext = MilliSeconds(100);
  //EventId         m_sendEvent;
  MyApp *ptMyApp;

  for(uint32_t i = 0; i < AppsSrc; i++) //Buscando todas as aplicações, a princípio é só uma ???
  {
    ptrApp = parSocket->GetNode()->GetApplication(i);
    //ptrMyApp = static_cast<MyApp>(ptrApp->GetObject<ns3::Application>(ptrApp->GetTypeId()));
    //ptrMyApp = static_pointer_cast<MyApp>(ptrApp);
    //ptMyApp = static_cast<MyApp *>(ptrApp->GetObject())
    ptMyApp = static_cast<MyApp *>(PeekPointer(ptrApp));
    //ptrMyApp =  DynamicCast<Ptr<MyApp>>(ptrApp->GetObject<ns3::Application>(ptrApp->GetTypeId()));
    //ptrMyApp =  DynamicCast<Ptr<MyApp>>(parSocket->GetNode()->GetApplication(i));
    //cout << "Reativada App" << ptrMyApp->getAppId() << "do nó " <<  parSocket->GetNode()->GetId();
    //ptrMyApp->SendPacket();
    //cout << "Reativada App " << ptMyApp->getAppId() << " do nó " <<  parSocket->GetNode()->GetId() << "\n";
    // Providing a seed value
    if(ptMyApp->getPendingTransmission())
      return;
	  srand((unsigned) Simulator::Now().GetMilliSeconds());
	  // Get a random number
    //cout<< "Numero Gerado " << rand()%50 << "\n";

	  double decRandomTime = double((rand()%100))/1000.0;

    //cout<<"Numero Normalizado " << randomTime <<"\n";

    double intRandomTime = (rand()%100);
  
    /*
      pendingTransmission foi criado para evitar que se 
      agende mais de uma transmissão, tendo em vista que o 
      SetSendCallback é chamado sempre que o nível do buffer decrementa

    */
    if(!ptMyApp->getPendingTransmission()){ //se for o no zero mantem-se o valor inicial 100ms
      tNext =  Seconds (intRandomTime+decRandomTime);
      if(ptMyApp->getStopTime().GetSeconds() >=  (Simulator::Now().GetSeconds() + tNext.GetSeconds()))
      {
        cout << "Nó " << idNode << " voltará a transmitir em " << tNext.GetSeconds()<<" s tendo em vista " << intRandomTime<<" e "<< decRandomTime <<" \n"; 
        cout << "Transmissão ocorrerá em: " << Simulator::Now().GetSeconds() + tNext.GetSeconds() << "s\n";
        Simulator::Schedule (tNext, &TranmissionTrigger,ptMyApp);
        ptMyApp->setPendingTransmission(true);
      }
    }
    
   
    //ptMyApp->SendPacket();
  }
  
 
}

/*
static void
PrintTimeCwd ()
{
  
  std::cout << "Mudancas: "<< num_time_cwd_size_change << "\n\n";
  std::cout << "[";
  for (unsigned int i=0; i < num_time_cwd_size_change; i++)
    std::cout << time_cwd_size_change[i] << ",";
  std::cout <<"]";

  std::cout <<"\n\n\n";

  std::cout << "[";
  for (unsigned int i=0; i < num_cwd_size; i++)
    std::cout << cwd_size[i] << ",";
  std::cout <<"]";
}*/


bool GetIdFromContext(std::string parContext, int &parIdSrc, int &parIdDestination)
{
  std::string terminalsId = parContext;
  std::string delimiter = ">";
  size_t pos = 0;
  std::string strNodeId;
  pos = terminalsId.find(delimiter);
  strNodeId = terminalsId.substr(0, pos);
  parIdSrc=stoi(strNodeId);
  terminalsId.erase(0, pos + delimiter.length());
  parIdDestination=stoi(terminalsId);
  if(parIdDestination < MAX_TERMINALS && parIdSrc < MAX_TERMINALS)
    return true;
  
  return false;

}


static void CwndChange (std::string context, uint32_t oldCwnd, uint32_t newCwnd)
{
  
  //pelo que está em https://www.nsnam.org/docs/models/html/tcp.html
  //e pela experiência, as cwnd são dadas em bytes. 
  //cout << context << "\n";

  //cout << "oldCwnd:" << oldCwnd << "\n";

  //cout << "newCwnd"  << newCwnd << "\n";

  //std::cout << idSrc << " > " << idDest << std::endl;
  int idSrc, idDest;

  if(GetIdFromContext(context, idSrc, idDest))
    lastCwnd[idSrc][idDest] = newCwnd;

  else{
    
    std::cout << "Corrupted ID's";
    exit(0);

  }

  //Armazenando o instante em que a cwnd é zero, em que a princípio vai se 
  //iniciar o SlowStart. Assim pode-se desprezar os dados desta fase.
  if (!newCwnd)
  {
    lastTimeCwndIsZero[idSrc][idDest] = Simulator::Now().GetSeconds();

  }
    

  /*
  //Para capturar os tempos e fazêlos no formato desejado
  if(!num_cwd_size)
  {
      NS_LOG_UNCOND("\n\n" << "Janela Inicial" << oldCwnd<<"\n\n\n");
      time_cwd_size_change[0]=0.0;
      num_time_cwd_size_change++;
      cwd_size[num_cwd_size]=oldCwnd;
      num_cwd_size++;
  }
  time_cwd_size_change[num_time_cwd_size_change]=Simulator::Now ().GetSeconds ();
  num_time_cwd_size_change++;
  cwd_size[num_cwd_size]=newCwnd;
  num_cwd_size++;

  //NS_LOG_UNCOND (Simulator::Now ().GetSeconds () << "\t" << newCwnd);

  if( num_cwd_size==1 || (time_cwd_size_change[num_time_cwd_size_change-1]-last_measure) > 0.04)
  {
    NS_LOG_UNCOND (time_cwd_size_change[num_time_cwd_size_change-1]<< "\t" << cwd_size[num_cwd_size-1]);
    last_measure = time_cwd_size_change[num_time_cwd_size_change-1];
  }*/
}





//static void RxDrop (Ptr<const Packet> p)
//{
  //NS_LOG_UNCOND ("RxDrop at " << Simulator::Now ().GetSeconds ());
  //return;
//}


//Simulation Time

 //double startingHour = 0.0;
 //double startingminute = 0.0;
 string strStartingTime;
 //uint64_t  startTime; Seria o inicio do programa, e não da simulação.

 

void SetStartSimulationTime()
{
  
  //startingHour = simulationStart.GetHours();
  //startingminute = simulationStart.GetMinutes();
  time_t now = time(0);
  strStartingTime.append(ctime(&now));
  //startTime = Simulator::Now().GetMilliSeconds();
 
}



void
 ChangeNetworkParameters (int parRot1, int parRot2,int parFaseEnlace)
 {
   NS_LOG_INFO ("event a time :" << Simulator::Now ().GetSeconds () );
   //cout << "Parameter Changed in link "<<parRot1<<" >>> " << parRot2 << "\n";

   if(Simulator::Now().GetSeconds() < 200)
   {
      //pointToPointRouters[parRot1][parRot2].SetDeviceAttribute ("DataRate",StringValue("1000Mbps"));//Para 20L e 10L
      pointToPointRouters[parRot1][parRot2].SetDeviceAttribute ("DataRate",StringValue("1Mbps"));//Para 1L
      pointToPointRouters[parRot1][parRot2].SetChannelAttribute ("Delay", TimeValue(MilliSeconds(10.0)));
      cout << "Parameter Changed in link "<<parRot1<<" >>> " << parRot2 <<" "<<">>Fase 3 " <<  "\n";
      //Simulator::Schedule (Seconds(1200.0) ,&ChangeNetworkParameters,parRot1,parRot2,0);
      Simulator::Schedule (Seconds(3200.0) ,&ChangeNetworkParameters,parRot1,parRot2,0);
      return;

   }

   if(parFaseEnlace == 0)
   {

      //pointToPointRouters[parRot1][parRot2].SetDeviceAttribute ("DataRate",StringValue("1Mbps"));////Para 20L e 10L
      pointToPointRouters[parRot1][parRot2].SetDeviceAttribute ("DataRate",StringValue("250Kbps"));////Para 20L e 10L
      pointToPointRouters[parRot1][parRot2].SetChannelAttribute ("Delay", TimeValue(MilliSeconds(1000.0)));
      cout << "Parameter Changed in link "<<parRot1<<"---" << parRot2 <<" "<< ">>Fase 0 " <<  "\n";
      Simulator::Schedule (Seconds(120.0) ,&ChangeNetworkParameters,parRot1,parRot2,1);

   }

   else if(parFaseEnlace == 1)
   {
      //pointToPointRouters[parRot1][parRot2].SetDeviceAttribute ("DataRate",StringValue("500Kbps"));//Para 20L e 10L
      pointToPointRouters[parRot1][parRot2].SetDeviceAttribute ("DataRate",StringValue("150Kbps"));//Para 1L
      pointToPointRouters[parRot1][parRot2].SetChannelAttribute ("Delay", TimeValue(MilliSeconds(2000.0)));
      cout << "Parameter Changed in link "<<parRot1<<"---" << parRot2 <<" "<<">>Fase 1" <<  "\n";
      Simulator::Schedule (Seconds(120.0) ,&ChangeNetworkParameters,parRot1,parRot2,2);

   }

   else if(parFaseEnlace == 2)
   {
     
      //pointToPointRouters[parRot1][parRot2].SetDeviceAttribute ("DataRate",StringValue("150Kbps"));//Para 20L e 10L
      pointToPointRouters[parRot1][parRot2].SetDeviceAttribute ("DataRate",StringValue("100Kbps"));//Para 1L
      pointToPointRouters[parRot1][parRot2].SetChannelAttribute ("Delay", TimeValue(MilliSeconds(3000.0)));
      cout << "Parameter Changed in link "<<parRot1<<"---" << parRot2 <<" "<<">>Fase 2" <<  "\n";
      Simulator::Schedule (Seconds(120.0) ,&ChangeNetworkParameters,parRot1,parRot2,0);


   }


   else if(parFaseEnlace == 3)
   {

      //pointToPointRouters[parRot1][parRot2].SetDeviceAttribute ("DataRate",StringValue("1000Mbps"));//Para 20L e 10L
      pointToPointRouters[parRot1][parRot2].SetDeviceAttribute ("DataRate",StringValue("1000Kbps"));//Para 1L
      pointToPointRouters[parRot1][parRot2].SetChannelAttribute ("Delay", TimeValue(MilliSeconds(10.0)));
      cout << "Parameter Changed in link "<<parRot1<<"---" << parRot2 <<" "<<">>Fase 3 " <<  "\n";
      Simulator::Schedule (Seconds(120.0) ,&ChangeNetworkParameters,parRot1,parRot2,0);
 
   }


   
 }
 



bool AjustarAplicacaoServidorTCP(ApplicationContainer parServerApps[][MAX_TERMINALS],
                                 PacketSinkHelper *parTCPSinkServer[][MAX_TERMINALS], 
                                 NodeContainer parPointToPointNodesPairsTerm[][MAX_ROUTERS],
                                 Ipv4InterfaceContainer parPointToPointInterfacesTerm[][MAX_ROUTERS], 
                                 int parIdSrc,
                                 int parIdDesination
                                 );


void AjustarAplicacaoClienteTCP(Ptr<MyApp> parClientApps[][MAX_TERMINALS],
                                Ptr<Socket> parTCPClientSocket[][MAX_TERMINALS],  
                                NodeContainer parPointToPointNodesPairsTerm[][MAX_ROUTERS],
                                Ipv4InterfaceContainer parPointToPointInterfacesTerm[][MAX_ROUTERS],
                                int parIdSrc,
                                int parIdDesination
                                );

void AjustarInicioTerminoServidor(ApplicationContainer parServerApps[][MAX_TERMINALS],
                                  int parIdSrc, 
                                  int parIdDesination,
                                  float t_0, 
                                  float t_f);

void AjustarInicioTerminoCliente(Ptr<MyApp> parClienterApps[][MAX_TERMINALS],
                                 int parIdSrc, 
                                 int parIdDesination,
                                 float t_0, 
                                 float t_f );



void AjustarOrigemEDestinoDosFluxos(vector <string> parVetFlows, 
                                    PacketSinkHelper *parTCPSinkServer[][MAX_TERMINALS],
                                    Ptr<Socket> parTCPClientSocket[][MAX_TERMINALS], 
                                    ApplicationContainer parServerApps[][MAX_TERMINALS],
                                    Ptr<MyApp> parClientApps[][MAX_TERMINALS]);


//Recebe o caminho do arquivo e extrai as configurações para config
void ExtrairConfiguracoes (string parPathTopology, string parPathFlow, vector <string>& parVetTopology, vector <string>& parVetFlows); 

void CriarLigacoesTerm(vector <string> parVetTopology);

void CriarLigacoesRouters(vector <string> parVetTopology);

//Ver comentário na chamada, também comentada.
//void InicializarTCPSocketClients(UdpEchoClientHelper *parEchoClient[][MAX_TERMINALS]);



 //from packet-sink.cc line 191 para fazer os eventos. Ver também myfifth.cpp

void FinalizarEchoClient(UdpEchoClientHelper *parEchoClient[][MAX_TERMINALS]);



void ImprimirVetorString(vector<string> parVetString);
void ImprimirVetorInteiros(int* parVetor, int parSize);

void InstalarPilhaDeProtocolos();

void RegistrarEmArquivo(uint8_t* parBufEndSrc, uint8_t *parBufEndDest,char parOrig)
{
  string strSrcAddres = to_string(parBufEndSrc[0])+"_"+
                      to_string(parBufEndSrc[1])+"_"+
                      to_string(parBufEndSrc[2])+"_"+
                      to_string(parBufEndSrc[3]);

  
  string strDestAddres = to_string(parBufEndDest[0])+"_"+
                      to_string(parBufEndDest[1])+"_"+
                      to_string(parBufEndDest[2])+"_"+
                      to_string(parBufEndDest[3]);
  
  //cout << strDestAddres;

  string filepath = workDir+"/"+strSrcAddres+"to"+strDestAddres+"."+"txt";
  std::ofstream file;
  //can't enable exception now because of gcc bug that raises ios_base::failure with useless message
  //file.exceptions(file.exceptions() | std::ios::failbit);
  file.open(filepath, std::ios::out | std::ios::app);
  if (file.fail())
  {
    std::cout << "Erro ao registrar Transmissão";
    exit(0);
  }
  //make sure write fails with exception if something is wrong
  if(parOrig == 'R')//originou-se no Receive
  {
    file << "At time " << Simulator::Now ().GetSeconds ()
         << "s sink "
         << to_string(parBufEndDest[0])+"."+
            to_string(parBufEndDest[1])+"."+
            to_string(parBufEndDest[2])+"."+
            to_string(parBufEndDest[3])
         << " received from "
         //<<  packet->GetSize () << " bytes from "
         << to_string(parBufEndSrc[0])+"."+
            to_string(parBufEndSrc[1])+"."+
            to_string(parBufEndSrc[2])+"."+
            to_string(parBufEndSrc[3])
         << "\n";
         //<< " port " << InetSocketAddress::ConvertFrom (srcAddress).GetPort ();
  }

  else if (parOrig == 'S')//originou-se no Send
  {
      file << "At time "
                  << Simulator::Now ().GetSeconds ()
                  << "s client " 
                  <<to_string(parBufEndSrc[0])+"."+
                    to_string(parBufEndSrc[1])+"."+
                    to_string(parBufEndSrc[2])+"."+
                    to_string(parBufEndSrc[3])
                  <<" sent a package to "  
                  <<to_string(parBufEndDest[0])+"."+
                    to_string(parBufEndDest[1])+"."+
                    to_string(parBufEndDest[2])+"."+
                    to_string(parBufEndDest[3])
                  << "\n";
                  
  }
  else
    std::cout << "Fonte de evento desconhecida";
          
  file.close();
}

void RegistraDadosTreino(unsigned int parNumAckFlow, 
                         double parAck_ewma, 
                         double parSend_ewma, 
                         double parRtt_ratio,
                         uint32_t parCwnd,
                         int parBuffeSizeVariation,
                         double parRouterQueue_ewma,
                         uint32_t parRouterBufferSizeValueAckArrival,
                         uint32_t parRouterBufferSizeValuePacketSent,
                         uint64_t parTSAckArrival,
                         uint32_t parTSInsideAck,
                         uint64_t parMimRTTAck,
                         uint8_t* parBufEndSrc, 
                         uint8_t* parBufEndDest,
                         int parFlowType,
                         int parIdSrc,
                         int parIdDest,
                         bool parUnicFile)
{



  //escapando do slowStart
  //if((Simulator::Now().GetSeconds() - lastTimeCwndIsZero[parIdSrc][parIdDest] <=50) && parFlowType == LONG_FLOW)
    //return;
  bool cabecalho = false; //Cabecalho só no primeiro registro. Então, a princípio é falso.
  int networkSituation;
  string filepath;
  string flowType;

  if(parFlowType == VERYSHORT_FLOW)
    flowType = "VS"; //VeryShort
  else if(parFlowType == SHORT_FLOW)
    flowType="S";
  else if (parFlowType == LONG_FLOW)
    flowType="L";
  else{
    std::cout << "Undefined Flow Type";
    exit(0);
    
  }
  

  /*
  if (parRouterBufferSizeValueAckArrival <= 60)
    networkSituation = 1;
  else if (parRouterBufferSizeValueAckArrival >= 80 && parRouterBufferSizeValueAckArrival <= 95)
    networkSituation = 2;
  //else if (parRouterBufferSizeValueAckArrival >= 70 && parRouterBufferSizeValueAckArrival <= 95)
  //  networkSituation = 3;
  else
    return;
  */


  if (parRouterQueue_ewma <= 60)
    networkSituation = 1;
  else if (parRouterQueue_ewma >= 70 && parRouterQueue_ewma <= 95)
    networkSituation = 2;
  //else if (parRouterBufferSizeValueAckArrival >= 70 && parRouterBufferSizeValueAckArrival <= 95)
  //  networkSituation = 3;
  else
    return;
  



  
  if(parUnicFile)
    filepath = workDir+"/output/"+"training_"+strStartingTime.substr(0,strStartingTime.length()-5)+"."+"csv";

  else
  {
    string strSrcAddres = to_string(parBufEndSrc[0])+"_"+
                      to_string(parBufEndSrc[1])+"_"+
                      to_string(parBufEndSrc[2])+"_"+
                      to_string(parBufEndSrc[3]);

  
    string strDestAddres = to_string(parBufEndDest[0])+"_"+
                      to_string(parBufEndDest[1])+"_"+
                      to_string(parBufEndDest[2])+"_"+
                      to_string(parBufEndDest[3]);
  
    //cout << strDestAddres;
    //deletar rtt.substr(0,rtt.length()-3)
    filepath = workDir+"/output/"+strSrcAddres+"to"+strDestAddres+"_"+flowType+"_"+strStartingTime.substr(0,strStartingTime.length()-5)+"."+"csv";
  }
  std::replace(filepath.begin(),filepath.end(),':','_');
  std::ofstream file;
  std::ifstream testfile;
  //can't enable exception now because of gcc bug that raises ios_base::failure with useless message
  //file.exceptions(file.exceptions() | std::ios::failbit);
  testfile.open(filepath, std::ios::in);
  if (testfile.fail())
  {
    cabecalho = true;
  }
  else
    testfile.close();


  file.open(filepath, std::ios::out | std::ios::app);
  if (file.fail())
  {
    std::cout << "Erro ao registrar Dados de Treinamento";
    exit(0);
  }
  if(cabecalho)
  {
    /*
    file << "Bottleneck" << "," 
         << "Weight" << ","
         << "App Packet Size" << ","
         << "Max Sent Packets" << ","
         << "App Data Rate" << ","
         << "MSS" << "\n";
      
    file <<expBottleNeck << "," 
         << expWeightExpon << ","
         << expPacketSize << ","
         << expNPackets << ","
         << expAppDataRate << ","
         << expSegSize << "\n";

    file << ",\n";
    */


    file <<"#Ack" << "," 
         << "ack_ewma(ms)" << ","
         << "send_ewma(ms)" << ","
         << "rtt_ratio" << ","
         << "cwnd (Bytes)" << ","
         //<< "Buffer variation(%)" << ","
         //<< "queue_ewma" << ","
         << "Last Router Ocupation Ack Arriaval" << "(" <<bufferUnit<< ")"<<  ","
         << "Last Router Ocupation Packet Sent" << "(" <<bufferUnit<< ")"<<  ","
         << "Network Situation" <<  ","
         << "AckArrival(ms)" << ","
         << "TSInsideAck(ms)" << "," 
         << "RTTAck(ms)" << "\n";
  }
  //make sure write fails with exception if something is wrong
  file << parNumAckFlow << ","
       <<parAck_ewma << "," 
       << parSend_ewma << "," 
       << parRtt_ratio << ","
       << parCwnd << ","
       //<< (float)parBuffeSizeVariation/MAXROUTERBUFFERSIZE << ","
       << (float)parRouterQueue_ewma/MAXROUTERBUFFERSIZE << ","
       //<< (float)parRouterBufferSizeValueAckArrival/MAXROUTERBUFFERSIZE << ","
       << (float)parRouterBufferSizeValuePacketSent/MAXROUTERBUFFERSIZE << ","
       << networkSituation << ","
       << parTSAckArrival << ","
       << parTSInsideAck  << "," 
       << parMimRTTAck << "\n";
         //<< " port " << InetSocketAddress::ConvertFrom (srcAddress).GetPort ();
  
  file.close();

}
//Server side
static void
ReceivePackage (const Ptr< const Packet > packet, const Address &parSrcAddress, const Address &parDestAddress)
{    
  
  if(verboseSink)
  {
    //from packet-sink.cc line 191 
    //std::cout << "package_content:\n";
    //packet->Print(cout);
    std::cout << "At time " << Simulator::Now ().GetSeconds ()
         << "s sink "
         << InetSocketAddress::ConvertFrom(parDestAddress).GetIpv4 ()
         << " received from "
         //<<  packet->GetSize () << " bytes from "
         << InetSocketAddress::ConvertFrom(parSrcAddress).GetIpv4 ()
         << "\n"
         //<< " port " << InetSocketAddress::ConvertFrom (srcAddress).GetPort ()
         ; 
  }
  if(verboseFile)
  {
    uint8_t bufEndSrc[4], bufEndDest[4];  
    InetSocketAddress::ConvertFrom(parSrcAddress).GetIpv4().Serialize(bufEndSrc);
    InetSocketAddress::ConvertFrom(parDestAddress).GetIpv4().Serialize(bufEndDest);
    RegistrarEmArquivo(bufEndSrc,bufEndDest,'R'); //'R' para saber q veio de uma recepção. 'S' envio "send"
  }

  return;
}


//Client Side
static void
SentPackage (std::string context,const Ptr< const Packet > packet, const TcpHeader &header, const Ptr< const TcpSocketBase > socket)
{
  //Ptr<Ipv4> sentAddr =socket->GetNode()->GetObject<Ipv4>();
  Address sourceAddress, destinationAddress;
  socket->GetSockName(sourceAddress);
  socket->GetPeerName(destinationAddress);



  int idSrc, idDest;

  if (GetIdFromContext(context, idSrc, idDest)){
    //if(idSrc == 0)
    //{
    //cout <<"Sequence Numbers "<< header.GetSequenceNumber().GetValue()<<"\n";
    //deve-se ajustar para a rede pincel
    Ptr<PointToPointNetDevice> anteriorRouterDevice;
    uint32_t previousRouterBufferSizeValuePacketSent;

    /*=============================================================================================
    Em princípio não há diferença entre PARKINGLOT_TOPOLOGY e DUMBELL_TOPOLOGY, mas já fica preparado
    ==============================================================================================*/
    if(topology == PARKINGLOT_TOPOLOGY)
    {
      anteriorRouterDevice = DynamicCast<PointToPointNetDevice>(pointToPointDevicesRouters[assTerminalRoteador[idDest]-1][assTerminalRoteador[idDest]].Get(0));//the router is the first (find "@Ptr<PointToPointNetDevice> anteriorRouterDevice = DynamicCast<PointToPointNetDevice>(pointToPointDevicesRouters[assTerminalRoteador[idAckSender]-1][assTerminalRoteador[idAckSender]].Get(0)))"
                                                                                           // assTerminalRoteador[idDest] é o Roteador do terminal de destinp
                                                                                           //por iso pegamos -1 R*---R---|Dest|
      previousRouterBufferSizeValuePacketSent = DynamicCast<Queue<Packet>>(anteriorRouterDevice->GetQueue())->GetNPackets();
      netApps.clientApps[idSrc][idDest]->AssociateSeqQueueSize(header.GetSequenceNumber().GetValue(),previousRouterBufferSizeValuePacketSent);
    }
    /*
      A grande diferença em relação é que na DUMBELL, o Receptor pega a fila do terminal em que
      está ligado. É por isso que é necessário fazer distinção quando se recupera as filas do roteador

    */
    else if (topology == DUMBELL_TOPOLOGY)
    {
      //anteriorRouterDevice = DynamicCast<PointToPointNetDevice>(pointToPointDevicesTerm[idSrc][assTerminalRoteador[idSrc]].Get(0));//the router is the first (find "@Ptr<PointToPointNetDevice> anteriorRouterDevice = DynamicCast<PointToPointNetDevice>(pointToPointDevicesRouters[assTerminalRoteador[idAckSender]-1][assTerminalRoteador[idAckSender]].Get(0)))"
      anteriorRouterDevice = DynamicCast<PointToPointNetDevice>(pointToPointDevicesRouters[assTerminalRoteador[idDest]-1][assTerminalRoteador[idDest]].Get(0));//the router is the first (find "@Ptr<PointToPointNetDevice> anteriorRouterDevice = DynamicCast<PointToPointNetDevice>(pointToPointDevicesRouters[assTerminalRoteador[idAckSender]-1][assTerminalRoteador[idAckSender]].Get(0)))"

      previousRouterBufferSizeValuePacketSent = DynamicCast<Queue<Packet>>(anteriorRouterDevice->GetQueue())->GetNPackets();
      //cout << "Buffer on Sent:" << previousRouterBufferSizeValuePacketSent <<"\n";
      netApps.clientApps[idSrc][idDest]->AssociateSeqQueueSize(header.GetSequenceNumber().GetValue(),previousRouterBufferSizeValuePacketSent);
    }
    //}
  }
  else{

    std::cout << "Undefigned Source Sender";
    exit(0);

  }

  if(verboseSink)
  {
 
    //cout << "Envio!!!\n";
    NS_LOG_UNCOND ("At time "
                  << Simulator::Now ().GetSeconds ()
                  << "s"
                  << " client " 
                  //<< sentAddr->GetAddress(1,0).GetLocal() 
                  << InetSocketAddress::ConvertFrom(sourceAddress).GetIpv4 ()
                  <<" sent a package to "  
                  << InetSocketAddress::ConvertFrom(destinationAddress).GetIpv4 ()
                  );
  }

  if(verboseFile)
  {  
    uint8_t bufEndSrc[4], bufEndDest[4];  
    InetSocketAddress::ConvertFrom(sourceAddress).GetIpv4().Serialize(bufEndSrc);
    InetSocketAddress::ConvertFrom(destinationAddress).GetIpv4().Serialize(bufEndDest);
    RegistrarEmArquivo(bufEndSrc,bufEndDest,'S');//'R' para saber q veio de uma recepção. 'S' envio "send"
  }
  return;
}


int RetrieveIdFromIPBufferAddress(uint8_t* parBufKeyAddres)
{

  /*
    A ideia será iterar entre os nós de  NodeContainer terminals,  compararnado os endereços
    por meio de //Ptr<Ipv4> sentAddr =socket->GetNode()->GetObject<Ipv4>();//
    e comparar o parSocket->GetPeerName() com o  sentAddr->GetAddress(1,0).GetLocal() 
    o que der igual é o id do servidor
    
    
    
  */

  uint8_t bufNodeAddres[4];
  
  int numActiveNodes = terminals.GetN();

  for (int i=0; i < numActiveNodes; i++)
  {
    terminals.Get(i)->GetObject<Ipv4>()->GetAddress(1,0).GetLocal().Serialize(bufNodeAddres);
    if(parBufKeyAddres[0] == bufNodeAddres[0] &&
       parBufKeyAddres[1] == bufNodeAddres[1] &&
       parBufKeyAddres[2] == bufNodeAddres[2] &&
       parBufKeyAddres[3] == bufNodeAddres[3] 
    )
    {

      /*NS_LOG_UNCOND ("At time "
                  << Simulator::Now ().GetSeconds ()
                  << " Terminal "
                  << i
                  << " was associated\n"
                  );*/
        return i;
    }
  }
  return -1;//invalid address
}



//Client Side
static void
ReceivedFromServer(std::string context,const Ptr< const Packet > parPacket, const TcpHeader &parHeader, const Ptr< const TcpSocketBase > parSocket)
{


   /*
    A ideia será iterar entre os nós de  NodeContainer terminals,  compararnado os endereços
    por meio de //Ptr<Ipv4> sentAddr =socket->GetNode()->GetObject<Ipv4>();//
    e comparar o parSocket->GetPeerName() com o  sentAddr->GetAddress(1,0).GetLocal() 
    o que der igual é o id do servidor
    
    
  */



  

  //Ptr<Packet> copy = parPacket->Copy();
  //SocketPriorityTag priorityTag;
 // copy->RemovePacketTag (priorityTag);

  /*
  // Headers must be removed in the order they're present.
  PppHeader pppHeader;
  
  Ipv4Header ipHeader;
  copy->RemoveHeader(ipHeader);

  std::cout << "Source IP: ";
  ipHeader.GetSource().Print(std::cout);
  std::cout << std::endl;

  std::cout << "Destination IP: ";
  ipHeader.GetDestination().Print(std::cout);
  std::cout << std::endl;*/

  //TcpHeader receivedTCPPckHeader; 
  //copy->RemoveHeader(receivedTCPPckHeader);

  //cout << "Recebeu Feedback";
  //myPause();

  int idSrc, idDest, flowType;

  if(GetIdFromContext(context, idSrc, idDest))

    flowType = netApps.clientApps[idSrc][idDest]->getFlowType();
    

  else{
    
    std::cout << "Corrupted ID's";
    exit(0);

  }

  uint32_t previousRouterBufferSizeValuePacketSent=0;




/*=====================================================================================
  Código baseado em  tcp-socket-base.cc, linha 3538
=====================================================================================*/
  if(parHeader.GetFlags() & TcpHeader::ACK)
  {
    //std::cout << "Recebeu Ack!!";
    //myPause();
    Address ackSenderAddress, ackReceiverAddress;
    parSocket->GetSockName(ackReceiverAddress);
    parSocket->GetPeerName(ackSenderAddress);
    int idAckReceiver = parSocket->GetNode()->GetId()-numRouters;//Retira-se os numRouters, 
                                                                 //pois são os primeiros a serem
                                                                 //inseridos

    //Getting the Ack Receivercwnd
    /*
     A ideia da linha abaixo foi abortada pelo fado de o método window ser protegido.
    */
    //uint32_t cwndSize = parSocket->Window();

   
    //Getting the ack sender address as string
    //std::ostream streamAckSenderAddress;



    uint32_t seqReceived = parHeader.GetAckNumber().GetValue();

    //if(lastSeq[idSrc][idDest] >= seqReceived)//Se está recebendo um ack já processado, ele está bagunçado, daí aborta-se
      //return;
    //else
    lastSeq[idSrc][idDest] = seqReceived;

    //if(idSrc == 0)
      previousRouterBufferSizeValuePacketSent=netApps.clientApps[idSrc][idDest]->GetAssociateQueueSize(seqReceived);



    uint8_t ipAckReceiver[4];
    InetSocketAddress::ConvertFrom(ackSenderAddress).GetIpv4().Serialize(ipAckReceiver);
    int idAckSender = RetrieveIdFromIPBufferAddress(ipAckReceiver);
    if(idAckSender == -1)
    {
      std::printf("Unrecognized AckSender\n");
      exit(0);
    }

    //Comprovação que ambos os métodos estão certos!!!
    //printf("idAckSender: %d\n",idAckSender);//Ok
    //printf("idAckReceiver: %d\n",idAckReceiver);

    //printf("idDest: %d\n",idDest);//Ok
    //printf("idSrc: %d\n",idSrc);


    numAckReceived[idAckReceiver][idAckSender]++;


    uint64_t  marcaTempoChegadaAck = Simulator::Now().GetMilliSeconds();
    //cout <<"Chegou Ack em " << Simulator::Now() << "\n";
    //marcaTempoChegadaAckAnterior é global;

    //marcaTempoChegadaAckAnterior[idAckReceiver][idAckSender] está com o início da tranmissão ver AjustarInicioTerminoCliente
    uint64_t intervalFromPreviousAck = marcaTempoChegadaAck - marcaTempoChegadaAckAnterior[idAckReceiver][idAckSender];
    double ack_ewma = 0.0;
    if(numAckReceived[idAckReceiver][idAckSender] > 2)//desprezando o primeiro ack que parece vir alterado
    {
      
      if(numAckReceived[idAckReceiver][idAckSender] == 3)
        ack_ewma = (double)(intervalFromPreviousAck);
      //else if(numAckReceived[idAckReceiver][idAckSender] == 2)
        //ack_ewma = (double)(intervalFromPreviousAck)-ack_ewma;
      else
        ack_ewma = (double)((1-expWeightExpon )*(lastAck_ewma[idAckReceiver][idAckSender]) + expWeightExpon *(intervalFromPreviousAck));
    }
    //preparando para o próximo ack.
    marcaTempoChegadaAckAnterior[idAckReceiver][idAckSender] = marcaTempoChegadaAck;
    lastIntervalBetweenAcks[idAckReceiver][idAckSender] =  intervalFromPreviousAck;
    lastAck_ewma[idAckReceiver][idAckSender] = ack_ewma;

    /*código Temporário......
    if(numAckReceived[idAckReceiver][idAckSender] < 3)
    {
      printf("rodada: %d--> aack_ewma= %f, marcaTenpoAnt[%d][%d] = %ld, Intervalo=%ld\n",
            numAckReceived[idAckReceiver][idAckSender],
            ack_ewma,idAckReceiver,idAckSender,
            marcaTempoChegadaAckAnterior[idAckReceiver][idAckSender], 
            intervalFromPreviousAck);
    }
    else 
     exit(0);
    */
    
    Time timeFromTS = Seconds (0.0);
    Ptr<const TcpOptionTS> ts;
    if (parHeader.HasOption (TcpOption::TS))
    {
      
      ts = DynamicCast<const TcpOptionTS> (parHeader.GetOption (TcpOption::TS));
      timeFromTS = TcpOptionTS::ElapsedTimeFromTsValue (ts->GetEcho ());
      if (timeFromTS.IsZero ())
      {
        NS_LOG_LOGIC ("TcpSocketBase::EstimateRtt - RTT calculated from TcpOption::TS is zero, approximating to 1us.");
        std::cout << "TcpSocketBase::EstimateRtt - RTT calculated from TcpOption::TS is zero, approximating to 1us.\n";
        timeFromTS = MicroSeconds (1);
      }
      //if(marcaTempoRefletidaAckAnterior[idAckReceiver][idAckSender] == MilliSeconds(0.0).GetInteger()) //primeiro pacote
        //marcaTempoRefletidaAckAnterior[idAckReceiver][idAckSender] = ts->GetEcho();
      //Tudo baseado no tempo decorrido, por isso o tempo desde marcaTempoRefletidaAckAnterior é maior
      /*if(send_ewma.IsZero())
      {
        cout << "Marca Tempo 0\n";
      }*/
      //tempoDecorridoDesdemarcaTempoRefletidaAckAnterior é global
    //marcaTempoChegadaAckAnterior é global; 
      /*
      send_ewma
      An exponentially-weighted moving average of the time between
      TCP sender timestamps reflected in those acknowledgments
      (send_ewma). A weight of 1/8 is given to the new
      sample in both EWMAs.
      */   

      //A variável a seguir se tornou desnecessária, pois  precisamos dos intervalos entre os TS 
      //uint64_t intervalFromPreviousTS = ts->GetEcho() - (marcaTempoRefletidaAckAnterior[idAckReceiver][idAckSender] & 0xFFFFFFFF);
      uint64_t arrivalTS = ts->GetEcho(); 
      uint64_t intervalbetweenTS = arrivalTS - (marcaTempoRefletidaAckAnterior[idAckReceiver][idAckSender] & 0xFFFFFFFF);
      
      
      double send_ewma;
      if(numAckReceived[idAckReceiver][idAckSender] == 1)
      {
        //intervalFromPreviousTS = arrivalTS - (startTime & 0xFFFFFFFF);
        //send_ewma = (double)(intervalFromPreviousTS);
          send_ewma = 0.0;
        //send_ewma = (double)(arrivalTS);
      }
      else
      {
        //intervalFromPreviousTS = arrivalTS - (marcaTempoRefletidaAckAnterior[idAckReceiver][idAckSender] & 0xFFFFFFFF);
        if(numAckReceived[idAckReceiver][idAckSender] == 2)
          send_ewma = intervalbetweenTS;
        else
        send_ewma = (double)((1-expWeightExpon )*lastSend_ewma[idAckReceiver][idAckSender] + (expWeightExpon )*intervalbetweenTS); 

      }
      marcaTempoRefletidaAckAnterior[idAckReceiver][idAckSender] = arrivalTS;
      //A variável a seguir se tornou desnecessária, pois  precisamos dos intervalos entre os TS 
      //lastIntervalBetweenTS[idAckReceiver][idAckSender] =  intervalFromPreviousTS;
      lastSend_ewma[idAckReceiver][idAckSender] = send_ewma;     

      if(minAckRtt[idAckReceiver][idAckSender] == MilliSeconds(0.0).GetInteger())
      {
        std::cout << "First min ack\n";
        minAckRtt[idAckReceiver][idAckSender] = timeFromTS.GetMilliSeconds();
      }
      if(minAckRtt[idAckReceiver][idAckSender] > timeFromTS.GetMilliSeconds())
        minAckRtt[idAckReceiver][idAckSender] = timeFromTS.GetMilliSeconds();
      
      /*=====================================================================================
      Antes (1) dvidia-se pelo min ack, que poderia variar ao longo da conexão. 
      Agora, amazenamenos o valor puro para dividir pelo menor no CSV.
      =====================================================================================*/

      //(1)double rtt_ratio = (double)timeFromTS.GetMilliSeconds()/minAckRtt[idAckReceiver][idAckSender];
      double rtt_ratio = (double)timeFromTS.GetMilliSeconds();

      


      //cout << "Clinete recebeu ack, que demorou" << m.GetSeconds() << " segundos\n";

      //pointToPointDevicesTerm[stoi(term)][stoi(rot)]

      //cout << "End Term: " << idAckSender << "\n";

      //cout << "End Router: " << assTerminalRoteador[idAckSender] << "\n";

      //~ 2 Linhas: Fila na porta do Roteador, ligada ao terminal.
      //Ptr<PointToPointNetDevice> endRouterDevice = DynamicCast<PointToPointNetDevice>(pointToPointDevicesTerm[idAckSender][assTerminalRoteador[idAckSender]].Get(0));//the router is the first (line 1479)
      
      //uint32_t routerBufferSizeValue = DynamicCast<Queue<Packet>>(endRouterDevice->GetQueue())->GetNPackets();
   
    /*=====================================================================================
        Tomando a fila na interface que liga o roteador anterior, ilustrando:

        ------> Sentido do fluxo
        
        T1----R1*---R2----T2
             /        \
            /          \
          T0            T3 

        Assim, se os fluxos são para 2, deve-se tomar a fila na interface de rotradores
        no roteador1 (R1).Com isso, em um fluxo positivo (do menor roteador para o maior), 
        a interface desejada está no rotreador anterior, ou seja, se o terminal Sink está 
        no roteador 2 a interface desejada está no roteador 1. Além disso, o Device, no
        "pointToPointDevicesRouters" é sempre o zero, uma vez que o roteador anterior é
        inserido primeiro. Resumindo:
        1) Sabemos o roteador do terminal destino, por meio do  rotDest = assTerminalRoteador[idAckSender]
           (R2) no esquema acima
        2) A interface do roteador do hop anterior (R1 no esquema) é rotDest-1
           por construção da topologia (model-topology)
        3) A interface desejada (* no esquema) será 
           pointToPointDevicesRouters[rotDest-1][rotDest].Get(0);
    =====================================================================================*/

      //~ 2 Linhas: Fila na porta do Roteador, ligada ao rotteador do terminal. Ver ilustração acima.
      //cout << "idAckSender: " << idAckSender << "\n";

      Ptr<PointToPointNetDevice> anteriorRouterDevice;
      uint32_t previousRouterBufferSizeValueAckArrival;


/*=====================================================================================
  Na verdade, na hora de pegar a fila do roteador, não há diferença, pois
  tanto na DUMBELL comop na PARKINGLOT, deve-se buscar o enlace entre o rotrador do
  acksender e do ackreceiver. Cuidado! se buscar o enlace entre o roteador e o
  terminal, vai dar sempre zero!
=====================================================================================*/      
      
      if(topology == PARKINGLOT_TOPOLOGY) //0 é parking Lot
      {
        anteriorRouterDevice = DynamicCast<PointToPointNetDevice>(pointToPointDevicesRouters[assTerminalRoteador[idAckSender]-1][assTerminalRoteador[idAckSender]].Get(0));//the router is the first (find "@Ptr<PointToPointNetDevice> anteriorRouterDevice = DynamicCast<PointToPointNetDevice>(pointToPointDevicesRouters[assTerminalRoteador[idAckSender]-1][assTerminalRoteador[idAckSender]].Get(0)))"
      
        previousRouterBufferSizeValueAckArrival = DynamicCast<Queue<Packet>>(anteriorRouterDevice->GetQueue())->GetNPackets();
      }

      /*
        A grande diferença em relação é que na DUMBELL, o Receptor pega a fila do terminal em que
        está ligado. É por isso que é necessário fazer distinção quando se recupera as filas do roteador

      */

      else if(topology == DUMBELL_TOPOLOGY)//1 é pincel
      {
     
        //std::cout << "Entrou DUMBELL" <<"\n";

        //std::cout << idAckReceiver <<" , " << assTerminalRoteador[idAckReceiver]<<"\n";
        
        anteriorRouterDevice = DynamicCast<PointToPointNetDevice>(pointToPointDevicesRouters[assTerminalRoteador[idAckSender]-1][assTerminalRoteador[idAckSender]].Get(0));//the router is the first (find "@Ptr<PointToPointNetDevice> anteriorRouterDevice = DynamicCast<PointToPointNetDevice>(pointToPointDevicesRouters[assTerminalRoteador[idAckSender]-1][assTerminalRoteador[idAckSender]].Get(0)))"
      
        previousRouterBufferSizeValueAckArrival = DynamicCast<Queue<Packet>>(anteriorRouterDevice->GetQueue())->GetNPackets();
      }
      int buffeSizeVariation = (int)previousRouterBufferSizeValueAckArrival - lastRouterOcupation[idAckReceiver][idAckSender];
      lastRouterOcupation[idAckReceiver][idAckSender] = previousRouterBufferSizeValueAckArrival;
      
      ////////////////////////////////////////////////////////////////////////
      double router_queue_ewma;
      if(numAckReceived[idAckReceiver][idAckSender] == 1)
      {
        //intervalFromPreviousTS = arrivalTS - (startTime & 0xFFFFFFFF);
        //send_ewma = (double)(intervalFromPreviousTS);
          router_queue_ewma = previousRouterBufferSizeValueAckArrival;
        //send_ewma = (double)(arrivalTS);
      }
      else
      {

        //router_queue_ewma = (double)((1-expWeightExpon )*lastRouterQueue_ewma[idAckReceiver][idAckSender] + (expWeightExpon )*previousRouterBufferSizeValueAckArrival); 
        router_queue_ewma = (double)((1-0.10)*lastRouterQueue_ewma[idAckReceiver][idAckSender] + (0.10)*previousRouterBufferSizeValueAckArrival); 


      }
      lastRouterQueue_ewma[idAckReceiver][idAckSender] = router_queue_ewma;     


/////////////////////////////////////////////////////////////////////////
      
      
      
      
      
      
      
      //std::cout << previousRouterBufferSizeValueAckArrival << "\n";
      //std::cout << lastRouterOcupation[idAckReceiver][idAckSender] << "\n";
      //std::cout << buffeSizeVariation << "\n";
      //myPause();

      
      //cout << "tempo" << Simulator::Now().GetMilliSeconds()<<"\n";
      //cout << "previousRouterBufferSizeValue: " << previousRouterBufferSizeValue << "\n";

     // The code above (~6 lines) is based on 
     //https://www.nsnam.org/doxygen/classns3_1_1_ipv4_interface_container.html#a827aefba768082758a8e74f752e0d915
     //presented in Get() function explanation     
    /*
     std::pair<Ptr<Ipv4>, uint32_t> returnValue = pointToPointInterfacesTerm[idAckSender][assTerminalRoteador[idAckSender]].Get (0);
     Ptr<Ipv4> ipv4 = returnValue.first;
     uint32_t index = returnValue.second;
     Ptr<Ipv4Interface> iface =  DynamicCast<Ipv4L3Protocol> (ipv4)->GetInterface (index);
     Ptr<Queue<Packet>> q =  DynamicCast<Queue<Packet>>(DynamicCast<PointToPointNetDevice>(iface->GetDevice())->GetQueue());
     uint32_t routerBufferSizeValue =  DynamicCast<DropTailQueue<Packet>>(q)->GetNPackets();
     */
    

      if(numAckReceived[idAckReceiver][idAckSender] == 1)
      {
         QueueSizeUnit enumRouterBufferUnit = DynamicCast<PointToPointNetDevice> (pointToPointDevicesTerm[idAckSender][assTerminalRoteador[idAckSender]].Get(0))->GetQueue()->GetCurrentSize().GetUnit();
         if(enumRouterBufferUnit == PACKETS)
            bufferUnit = "Packets";
         else if(enumRouterBufferUnit == BYTES)
            bufferUnit = "Bytes";
      }

      //routers.Get(assTerminalRoteador[idAckSender])->GetDevice(1);

      if(verboseFileTreino  && numAckReceived[idAckReceiver][idAckSender] > 10) //Procurar fugir do slowstart. 
      {
        uint8_t bufEndSrc[4], bufEndDest[4]; //Endereços IP bufferizados
        InetSocketAddress::ConvertFrom(ackReceiverAddress).GetIpv4().Serialize(bufEndSrc);
        InetSocketAddress::ConvertFrom(ackSenderAddress).GetIpv4().Serialize(bufEndDest);
        //RegistraDadosTreino(ack_ewma.GetMicroSeconds(), send_ewma.GetMicroSeconds(),rtt_ratio,bufEndSrc,bufEndDest);
        //if(numAckReceived[idAckReceiver][idAckSender] > 2)//Desprezando as duas primeiras medidas por parecerem, sempre espúrias.

        /*
        if(online and !idSrc and !(numAckReceived[idAckReceiver][idAckSender]%100))
        {

            cout << "Antes do registro do treino"<<"\n";
            cout << lastSeq[idAckReceiver][idAckSender]<<"\n";
            cout << ack_ewma<<"\n";
            cout << send_ewma<<"\n";
            cout << rtt_ratio<<"\n";
            cout << lastCwnd[idAckReceiver][idAckSender]<<"\n";
          
        }
        */

        RegistraDadosTreino(lastSeq[idAckReceiver][idAckSender], //numAckReceived[idAckReceiver][idAckSender], 
                                ack_ewma, 
                                send_ewma,
                                rtt_ratio,
                                lastCwnd[idAckReceiver][idAckSender],
                                buffeSizeVariation,
                                router_queue_ewma,
                                previousRouterBufferSizeValueAckArrival,
                                previousRouterBufferSizeValuePacketSent,
                                marcaTempoChegadaAck, 
                                ts->GetEcho(),
                                timeFromTS.GetMilliSeconds(),
                                bufEndSrc,
                                bufEndDest,
                                flowType,
                                idSrc,
                                idDest,
                                false);

          
        //if(online && !idSrc && !( numAckReceived[idAckReceiver][idAckSender]%100))
        if(online)
        {
            
            
            //cout << "ackReceived "<< numAckReceived[idAckReceiver][idAckSender] << "\n";

            //cout << idSrc<< ","<<idAckReceiver<<"\n";

            /*
            cout << "Antes da Normalizacao"<<"\n";
            cout << ack_ewma<<"\n";
            cout << send_ewma<<"\n";
            cout << rtt_ratio<<"\n";
            cout <<lastCwnd[idAckReceiver][idAckSender]<<"\n";
            */



            
            in.data_[0] = (float)ack_ewma/(12285.7);// é o maior ack_ewma  ao longo obtido 
            in.data_[1] = (float)send_ewma/(12285.7);// é o maior ack_ewma  ao longo obtido 
            in.data_[2] = (float)rtt_ratio/(241*9.98);// o menor, que deve dividir todos os rtt para obter o rtt_tatio; é o maior rtt_ratio
            in.data_[3] = (float)lastCwnd[idAckReceiver][idAckSender]/(32120.0);//  é o maior ack_ewma  ao longo obtido

            /*
            cout << "Antes da Norma"<<"\n";
            cout << in.data_[0]<<"\n";
            cout << in.data_[1]<<"\n";
            cout << in.data_[2]<<"\n";
            cout << in.data_[3]<<"\n";
            */

            
            //myPause();
            
            float norma = std::sqrt(std::pow(in.data_[0],2) +std::pow(in.data_[1],2)+std::pow(in.data_[2],2)+std::pow(in.data_[3],2));

            in.data_[0] = in.data_[0]/(norma);// 2770.7 é o maior ack_ewma  ao longo obtido 
            in.data_[1] = in.data_[1]/(norma);// 2814.05 é o maior ack_ewma  ao longo obtido 
            in.data_[2] = in.data_[2]/(norma);//240 é o menor, que deve dividir todos os rtt para obter o rtt_tatio; 2833 é o maior rtt_ratio
            in.data_[3] = in.data_[3]/(norma);// 32120 é o maior ack_ewma  ao longo obtido

            /*
            cout << "depois da Norma"<<"\n";
            cout << norma<<"\n";
            cout << in.data_[0]<<"\n";
            cout << in.data_[1]<<"\n";
            cout << in.data_[2]<<"\n";
            cout << in.data_[3]<<"\n";
            */
            // Run prediction.
            //myPause();
            Tensor out = model(in);
            

          Ptr<TcpSocket> ptrTcpSocket = DynamicCast< TcpSocket >(netApps.tcpClientSocket[idSrc][idDest]);
          Ptr<TcpSocketBase> ptrTcpSocketBase =DynamicCast<TcpSocketBase >(ptrTcpSocket);
          Ptr<TcpCongestionOps> ptrOps = ptrTcpSocketBase->GetCongestionControlAlgorithm();
          Ptr<TcpVegas> ptrVegas = DynamicCast<TcpVegas > (ptrOps);
          
          if(out.data_[0] >= out.data_[1] && !idSrc)
          {
            /*
            cout << "Antes da divisao pela constante"<<"\n";
            cout << lastSeq[idAckReceiver][idAckSender]<<"\n";
            cout << ack_ewma<<"\n";
            cout << send_ewma<<"\n";
            cout << rtt_ratio<<"\n";
            cout << lastCwnd[idAckReceiver][idAckSender]<<"\n";
            
            */
            //out.print();
            ptrVegas->UpdateNetworkState(1);
            //myPause();
          }
          else
            ptrVegas->UpdateNetworkState(2);

          }

      }
 
    }
  }



  else 
    std::cout << "Not an ACK";

  return;

}

void SetMaxPackets()
{
  uint32_t intRate = stoul(expAppDataRate.substr(0,expAppDataRate.length()-4));
  std::cout <<  expAppDataRate << "\n";
  std::cout << "intDataRate: "<< intRate<< "\n";

  double preExpNPackets = ((intRate*expSimulationTime/8)/expPacketSize +1);
  
  if (expAppDataRate.find("Gbps")!=std::string::npos)
  {
    std::cout << "Gbps" << "\n";
    preExpNPackets=preExpNPackets*1000000000;
  }
  else if (expAppDataRate.find("Mbps")!=std::string::npos)
  {
    std::cout << "Mbps" << "\n";
    preExpNPackets=preExpNPackets*1000000;
  }
  else if (expAppDataRate.find("Kbps")!=std::string::npos)
  {
    std::cout << "Kbps" << "\n";
    preExpNPackets=preExpNPackets*1000;
  }
  expNPackets = (uint64_t) preExpNPackets;
  std::cout << "Espected Packet: "<< preExpNPackets << "\n";
  std::cout << "Espected Packet: "<< expNPackets << "\n";

  //exit(0);

}

void OutputConfigParam()
{
 
 //See options in https://www.nsnam.org/doxygen/d0/d02/_type_id_list.html
/*ns3::TcpBbr
ns3::TcpBic
ns3::TcpClassicRecovery
ns3::TcpCongestionOps
ns3::TcpCubic
ns3::TcpDctcp
ns3::TcpHeader
ns3::TcpHighSpeed
ns3::TcpHtcp
ns3::TcpHybla
ns3::TcpIllinois
ns3::TcpL4Protocol
ns3::TcpLedbat
ns3::TcpLinuxReno
ns3::TcpLp
ns3::TcpNewReno 
ns3::TcpVegas*/
 Config::SetDefault ("ns3::TcpL4Protocol::SocketType", StringValue ("ns3::TcpVegas"));
 Config::SetDefault("ns3::TcpSocket::SegmentSize", UintegerValue (1460));
// Output config store to txt format
  Config::SetDefault ("ns3::ConfigStore::Filename", StringValue ("output-attributes.txt"));
  Config::SetDefault ("ns3::ConfigStore::FileFormat", StringValue ("RawText"));
  Config::SetDefault ("ns3::ConfigStore::Mode", StringValue ("Save"));
  ConfigStore outputConfig2;
  outputConfig2.ConfigureDefaults ();
  outputConfig2.ConfigureAttributes ();
}


bool neural_mode = true;


void SetNeuralMode(bool par_neural_mode, int parIdSrc, int parIdDestination)
{
    Ptr<TcpSocket> ptrTcpSocket = DynamicCast< TcpSocket >(netApps.tcpClientSocket[parIdSrc][parIdDestination]);
    Ptr<TcpSocketBase> ptrTcpSocketBase =DynamicCast<TcpSocketBase >(ptrTcpSocket);
    Ptr<TcpCongestionOps> ptrOps = ptrTcpSocketBase->GetCongestionControlAlgorithm();
    Ptr<TcpVegas> ptrVegas = DynamicCast<TcpVegas > (ptrOps);
    ptrVegas->SetNeuralMode(par_neural_mode);

}

void TotalizarBytesTransmitidos()
{
  u_int64_t totalBytesTransmitidos = 0;

  for (int i = 0; i < numActiveFlows; i++)
  {
    //cout << lastSeq[activeFlows[i][0]][activeFlows[i][1]] << "\n";
    if(netApps.clientApps[activeFlows[i][0]][activeFlows[i][1]]->getFlowType() == LONG_FLOW)
      totalBytesTransmitidos = totalBytesTransmitidos + lastSeq[activeFlows[i][0]][activeFlows[i][1]];
    //cout << totalBytesTransmitidos << "\n";
    //myPause();
  }

  cout << "Goodput Global: " << totalBytesTransmitidos/std::pow(2,20)<<"MB\n";
  //cout << "Goodput Global: " << totalBytesTransmitidos <<"MB\n";
}

int 
main (int argc, char *argv[])
{

  
  
  /*Este programa recebe como parametros o numero de redes (numRedes) (argv[1])
    Daí deve-se criar o número de roteadores (numRedes/2+numRedes%2) e o número
    de nodes, considerando dois por redes numNodes=2*numRedes  
  */
  if(argc != 2)
  {
    std::printf("Informe o numero de roteadores, conforme exemplo abaixo:\n");
    std::printf("./waf --run \"TCP-Evaluation-Suite:TCP-Evaluation-Suite-Topology --numRouters=2\"\n");
    exit(0);
  }



  SetMaxPackets();
  std::cout << "SetMaxPackets OK \n";
  InitStateVariables();
  std::cout << "InitStateVariables OK\n";
  SetStartSimulationTime();
  std::cout << "SetStartSimulationTime OK\n";
  //cout << "weight: " << weightExpon <<"\n";
  if(verboseSink)
    LogComponentEnable ("PacketSink", LOG_LEVEL_INFO);

  if(verboseAllConfigParar)
  {
    OutputConfigParam();
  }
  CommandLine cmd (__FILE__);
  cmd.AddValue("numRouters", "#Roteadores do experimento", numRouters);
  //cmd.AddValue("numFlows", "#Fluxos do experimento", numFlows);
  cmd.Parse (argc, argv);

  //CsmaHelper csma[MAX_TERMINALS];
  //NodeContainer csmaNodesPairs[MAX_NUM_CSMA_GROUPS];
  //NetDeviceContainer csmaDevices[MAX_NUM_DEVICES];
  //Ipv4InterfaceContainer csmaInterfaces[MAX_NUM_CSMA_INTERFACES];

  //Como é ppp, o point to point helper também será uma matriz. Deve ser avaliado os demais
  /*=====================================================================================
  * A ideia das matrizes abaixo é que cada, enlace, conjunto de nós desse enlace, devices desses nós
  e as interfaces desses devices sejam endereçadas pelo identificador do terminal e do roteador
  Assim, se no model-topology.txt houver uma linha 
  1 2 1000Mb 1.089356e+01ms

  serão criados os seguintes objetos:
   1. pointToPointEnlaceTerm[1]][2] 
      o enlace ao qual será associado o terminal 1 e o roteador 2
   2. pointToPointNodesPairsTerm[1][2]
      O container dos nós 1 e 2, que serão associados ao enlace acima. 
      Ao pointToPointNodesPairsTerm[1][2] serão adicionados os nós 1 e 2, por meio dos 
      comandos
      pointToPointNodesPairsTerm[1][2].Add (parRouters.Get (2));  
      pointToPointNodesPairsTerm[1][2].Add (parRouters.Get (1));
      Lembrando que o roteador é adicionado primeiro.
    3. pointToPointDevicesTerm[1][2]
       Devices que serão instalados nos nós presentes em pointToPointNodesPairsTerm[1][2], que por
       sua vez serão ligados ao pointToPointEnlaceTerm, tudo isso por meio do comando:
        pointToPointDevicesTerm[1][2] = pointToPointEnlaceTerm[1]][2].Install (pointToPointNodesPairsTerm[1][2]);
    4. pointToPointInterfacesTerm[1][2]
      Interfaces que serão atribuídas aos devices de pointToPointDevicesTerm[1][2], permitindo a associação
      de endereços de forma automática, dentre outras coisas, por meio do comando:
        pointToPointInterfacesTerm[1][2] = address.Assign( pointToPointDevicesTerm[1][2]);

  *======================================================================================*/ 

  vector <string> vetTopology; //Vetor para armazenar as configurações
  vector <string> vetFlows; //Vetor para armazenar as configurações
 
  //Guarda a associação entre os terminais e os roteadores assTerminalRoteador[2]=5
  //indicaria que o terminal 2 está ligado ao roteador 5
  //para maiores informações sobre o porquê desse vetor ber comentário na função
  //AjustarAplicacaoClienteUDP 
 
/*=====================================================================================
  O vetor a seguir se destina a armazenar o número de interfaces usadas em
  cada roteador, o que facilita a geração dos endereços, pois, na montagem da
  topologia, cada interface de roteador é uma rede com prefixo próprio no endereço.
=====================================================================================*/


  //UdpEchoServerHelper echoServer (UDP_PORT); #levado para perto do vetor de aplicações
 

  /*===================================================================================
    O comentário da linha abaixo se deve ao fato de os clientes serem, agora MyApp, inicializados por CreateObject<MyApp> ();
    que, por fim serão liberados pelo Destroy()
  =====================================================================================*/
  //InicializarTCPSocketClient(echoClient); 



  //Talvez também seja interessante um vetor de clientes.
  

  Time::SetResolution (Time::MS);
  //LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
  //LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);

/*=====================================================================================
Foi constatado que o topogen.py insere nas primeiras linhas do "model-topology.txt" a ligação 
entre os roteadores e depois começa a ligação dos terminais com os roteadores.
Dessa forma, após sua leitura e armazenamento no vetConf, o VetConf deverá ser partido
da seguinte forma:
as numRoteadors primeiras linhas devem ser usadas para estabelecer a ligação entre os 
rodeadores, o que requer adaptação das funções CriarLigacoesTerm e tavez nos programa como um todo. 
=====================================================================================*/


  

  ExtrairConfiguracoes((workDir+"/model-topology-pincel-40L.txt").c_str(),
                       (workDir+"/model-flow-pincel-40L.txt").c_str(),
                       vetTopology,
                       vetFlows);
  std::cout << "ExtrairConfiguracoes OK\n";

  //ImprimirVetorString(vetTopology);

  std::cout << "Número de roteadores " << numRouters<<"\n";

  //myPause();
  
  numTerminals = ROUTER_PORTS*numRouters; //Cada Fluxo dois terminais
  
  
  routers.Create(numRouters);//Agora sim, efetivamente, são criados os roteadores 
  terminals.Create(numTerminals);//Agora sim, efetivamente, são criados os terminais


/*  A filosofia do ns3 é inserir em cada link todos os nós que o compartilharão,
    incluindo os devices correspondentes. Observe o comando abaixo:

    csmaDevices = csma.Install (csmaNodes); 

    csma é um enlace; csmaNodes é o conjunto de nós que estarão no csma que receberão
    os csmaDevices correspondnetes

    Daí é importante pensar os nós por enlace

    Assim, teríamos R1---R2; R1---T1; R2---T5
    
   */
  


  InstalarPilhaDeProtocolos();
  std::cout << "InstalarPilhaDeProtocolos Fev OK\n";
  

/*=====================================================================================
Funções Topológicas
=====================================================================================*/

  CriarLigacoesTerm(vetTopology);
  std::cout << "CriarLigacoesTerm OK\n";
    
  CriarLigacoesRouters(vetTopology);
  std::cout << "CriarLigacoesRouters OK\n";
  
  //AppPool netApps;

 
  //Agora as aplicações servidoras devem ser instaladas nos terminais destinations
  //presente no model-flow.txt

  //#00000001
  //Prepara os terminais destinos para os fluxos, instalando servidores nos terminais
  //da coluna 2 do model-flow.txt


  //AjustarOrigemEDestinoDosFluxos(vetFlows,tcpSinkServer,tcpClientSocket,serverApps,clientApps);
  AjustarOrigemEDestinoDosFluxos(vetFlows, netApps.tcpSinkServer,
                                           netApps.tcpClientSocket,
                                           netApps.serverApps,
                                           netApps.clientApps);



  //Agora as aplicações clientes devem ser instaladas nos terminais source
  //presente no model-flow.txt

  Ptr<FlowMonitor> flowMonitor;
  FlowMonitorHelper flowHelper;
  flowMonitor = flowHelper.InstallAll();


  std::cout << "Aplicações Servidoras e Clientes Instanciadas com sucesso!!" <<"\n\n\n";


  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

 
 // Ptr<RateErrorModel> em = CreateObject<RateErrorModel> ();
 // em->SetAttribute ("ErrorRate", DoubleValue (0.00001));
 // devices.Get (1)->SetAttribute ("ReceiveErrorModel", PointerValue (em));

 // InternetStackHelper stack;
 // stack.Install (nodes);

 // Ipv4AddressHelper address;
 // address.SetBase ("10.1.1.0", "255.255.255.252");
 // Ipv4InterfaceContainer interfaces = address.Assign (devices);*/

  /*Ajustando uma aplicação para receber conexões TCP (packetSinkHelper) */

  
  //uint16_t sinkPort = 8080;
  //Address sinkAddress (InetSocketAddress (interfaces.GetAddress (1), sinkPort));
  //PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort));
  //ApplicationContainer sinkApps = packetSinkHelper.Install (nodes.Get (1));
  //sinkApps.Start (Seconds (0.));AjustarOrigemEDestinoDosFluxos

  /*Criando o socket e estabelecendo o trace. 
  Veja que o socket será passado para o app
  segundo 
  https://www.nsnam.org/docs/models/html/tcp.html

  o CUBIC é o default

  */

  //TypeId tid = TypeId::LookupByName ("ns3::TcpHtcp");
  //std::stringstream nodeId;
  //nodeId << nodes.Get (0)->GetId ();
  //std::string specificNode = "/NodeList/" + nodeId.str () + "/$ns3::TcpL4Protocol/SocketType";
  //Config::Set (specificNode, TypeIdValue (tid));
  
  //Ptr<Socket> ns3TcpSocket = Socket::CreateSocket (nodes.Get (0), TcpSocketFactory::GetTypeId ());
  //ns3TcpSocket->TraceConnectWithoutContext ("CongestionWindow", MakeCallback (&CwndChange));

  //Ptr<MyApp> app = CreateObject<MyApp> ();
  /*
  Dentre outras coisas, a aplicação recebe sua taxa de transmissão, que não tem uma ligação
  direta com a taxa do canal. Mas deve ser menor que a do canal, pois não se considera os 
  cabeçalhos dos protocolos, que exigem do canal.
  */
  //app->Setup (ns3TcpSocket, sinkAddress, 1040, 1000, DataRate ("1Mbps"));
  //app->Setup (ns3TcpSocket, sinkAddress, 1040, 100000, DataRate ("1Mbps"));
  //nodes.Get (0)->AddApplication (app);
  //app->SetStartTime (Seconds (1.));
  //app->SetStopTime (Seconds (20.));
  //app->SetStopTime (Seconds (30.));

  //devices.Get (1)->TraceConnectWithoutContext ("PhyRxDrop", MakeCallback (&RxDrop));

  std::cout << "expSimulationTime: " << expSimulationTime << "\n";
  Simulator::Stop (Seconds (expSimulationTime));

  //Simulator::Stop (Seconds (20));
  //Simulator::Stop (Seconds (30));
  
  std::printf("========================Iniciando a Simulação===============================\n");
  Simulator::Run (); 
  flowMonitor->SerializeToXmlFile("Bbr1L.xml", true, true);
  Simulator::Destroy ();
  std::printf("===========================Fim da Simulação=================================\n");
  //FinalizarEchoClient(echoClient);
  std::cout << "Clientes finalizados com Sucesso!!"<<"\n";
  //PrintTimeCwd();
  TotalizarBytesTransmitidos();
  
  return 0;
}

void InstalarPilhaDeProtocolos()
{
  stack.Install (routers);
  stack.Install (terminals);
}

 /*=====================================================================================/
  Observe que no conjunto de nós da rede (parNosRede, que vem de terminals), cada nó é 
  identificado por um inteiro. O progrma está tratando os identificadors de nó dos ar-
  quivos model-topology.txt e model-flow de forma a corresponder o respectivo identifi-
  cador no Get do NodeContainer, que contém todos os nós da rede. Dessa forma, se  hou-
  ver  uma linha no model-topology, da forma 
   6 3 1000Mb 9.470218e-01ms
  os nós 6 e 3 do NodeContainer* parNosRede e parRouters serão acionados para:
  
  *Criação  de um  NodeContainer pointToPointNodesPairsTerm[6][3], aos quais serão adi-
  cionados os nós 6 e 3, conforme as linhas a seguir:
  pointToPointNodesPairsTerm[term][rot].Add (parRouters.Get (stoi(rot))); 
  pointToPointNodesPairsTerm[term][rot].Add (parTerminals.Get (stoi(term))); 

   Já se no model-flow.txt aparecer 
    5 6 3 1
   isso será interpretado que há um fluxo do nó 5 (obitido por parNosRede.Get(6)) para o 
   nó 6 (obtido por parNosRede.Get(6)). Sendo assim, essa linha desencadeará:
  
  *Criação de um   UdpEchoClientHelper echoClient[5][6] e ApplicationContainer clientApps[5][6];
  para cuidar da aplicação cliente, que deverá ser instalada no nó 5, por ser a origem, por 
  meio  das seguintes instruções:  
  parEchoClient[parIdSrc][parIdDestination].SetAttribute("RemoteAddress",parNosRede[parIdSrc][parIdDesination].GetAddress(1));
  parEchoClient[parIdSrc][parIdDestination].SetAttribute("RemotePort",UDP_PORT);
  parEchoClient[parIdSrc][parIdDestination]..SetAttribute ("MaxPackets", UintegerValue (1));
  parEchoClient[parIdSrc][parIdDestination]..SetAttribute ("Interval", TimeValue (Seconds (1.0)));
  parEchoClient[parIdSrc][parIdDestination]..SetAttribute ("PacketSize", UintegerValue (1024));
  parClientApps[parIdSrc][parIdDestination]. = parEchoClient[parIdSrc][parIdDestination].Install (parNosRede.Get(parIdSrc));

  A exceção à regra do Get se dá dentro do NodeContainer pointToPointNodesPairsTerm[6][3], por exemplo.
  Nesse cado, como sempre o roteador será inserido primeiro, ele será obtido da forma:
  pointToPointNodesPairsTerm[6][3].Get(0)
  e o terminal
  pointToPointNodesPairsTerm[6][3].Get(1)



  Toda essa esquematização permite que aturemos em pares de aplicações (servidoras e cliente) 
  e enlaces de forma indicidualizada
 
  
 =====================================================================================*/
 


 
void AjustarOrigemEDestinoDosFluxos(vector <string> parVetFlows, 
                                    PacketSinkHelper *parTCPSinkServer[][MAX_TERMINALS],
                                    Ptr<Socket> parTCPClientSocket[][MAX_TERMINALS], 
                                    ApplicationContainer parServerApps[][MAX_TERMINALS],
                                    Ptr<MyApp> parClientApps[][MAX_TERMINALS] 
                                    )
                                    
{
  //||

  std::istringstream *tokenStream;
  string token;
  string src;
  string dest;
  string hops;
  string strTipoFluxo;
  bool novoServidor;
  float t_start;
  float t_end;
  

  for (std::size_t i = 0; i < parVetFlows.size(); ++i)//i linha a linha
  {    
    srand((unsigned) time(NULL));
    tokenStream = new std::istringstream(parVetFlows[i]);
    //lendo terminal src da linha
    std::getline(*tokenStream, src, ' ');
    //lendo terminal destino da linha
    std::getline(*tokenStream, dest, ' ');
    //lendo os hops 
    std::getline(*tokenStream, hops, ' ');
    //lendo o tipo de fluxo
    std::getline(*tokenStream, strTipoFluxo, ' ');

    tipoFluxo[stoi(src)][stoi(dest)] = strTipoFluxo.c_str()[0];

    

  /*=====================================================================================/
   A rede agora será identificada pelo id do terminal e o id do roteador. Ver
   o pointToPointEnlaceTerm. Além disso, é uma aplicação para cada linha do arquivo de
   configuração, com vistas a estabelecer os devidos fluxos. Observe que um mesmo terminal
   pode ser source e destination, ou ser source em mais de um fluxo. Por isso o ideal é
   identificar a cada rede e cada fluxo pelo roteador e terminal, pois, uma vez dado o 
   terminal, não importa quantas vezes ele aparece nas linha de configuração, nós sempre vamos nele.
  =====================================================================================*/
 

   //AjustarAplicacaoServidorUDP(serverApps[i], echoServer[i], pointToPointNodesPairsTerm, idRedeServidor,idServidorNaRede);
    
   novoServidor=AjustarAplicacaoServidorTCP(parServerApps, 
                              parTCPSinkServer, 
                              pointToPointNodesPairsTerm,
                              pointToPointInterfacesTerm, 
                              stoi(src), 
                              stoi(dest)
                              );

    //cout << "Aplicações Servidoras Instanciadas com sucesso!!" <<"\n";


  /*=====================================================================================/
   Na função AjustarAplicacaoServidorTCP, a aplicação servidora (TCPSinkServer) só é criada
   se dento do nó destino não existe um TCPSinkServer Prévio. Caso contrário, o fluxo
   em criação apenas apontará para o TCPSinkServer já existente. Em caso de mero
   apontamento, não se deve mexer no início e/ou término do servidor, que deve permanecer
   com período de funcionamento a partir da  criação efetiva do TCPSinkServer.
   Assim, o Ajuste do início e término do servidor, só deve ser realizado se 
   foi efetivamente criada uma aplicação servidora. Caso contrário
   essa etapa deve ser omitida. Por isso a variável booleana novoServidor.
   Este detalhe foi observado quando da criação de 140 fluxos para um mesmo tcpSink. A 
   cada fluxo o início do servidor era ajustado para um tempo a frente, deixando os 
   fluxos iniciais sem resposta ao seu envio. Por exemplo consideremos o fluxo do 
   termonal 0 para o 140, em que há o único de TCPSinkServer. Quando chega-se, por exemplo
   ao terminal 135, se não plularmos o AjustarInicioTerminoServidor, o servidor será ajustado
   para iniciar em 136 segundos, quando o terninal 0 já enviou seus pacotes, que, neste caso,
   ficaram no vazio.
  =====================================================================================*/
   if(novoServidor)
    AjustarInicioTerminoServidor(parServerApps, 
                                stoi(src),
                                stoi(dest),
                                1.0+i,
                                //1.0+4*i+3.0);
                                expSimulationTime);
    //cout << "Aplicações Servidoras agendadas com sucesso!!" <<"\n";

   AjustarAplicacaoClienteTCP(parClientApps, 
                              parTCPClientSocket, 
                              pointToPointNodesPairsTerm,
                              pointToPointInterfacesTerm, 
                              stoi(src), 
                              stoi(dest));

    //cout << "Aplicações Clientes Instanciadas com sucesso!!" <<"\n";


    if(!stoi(src))// Nó zero é o mestre para levantar dados
    {

      t_start = 1.0;
      t_end = expSimulationTime; //gera um número entre zero e expSimulationTime-t_start,ou seja,
                                                     //ao se somar t_start,ele vai no máximo a expSimulationTime
    }

    else if(parClientApps[stoi(src)][stoi(dest)]->getFlowType() == LONG_FLOW)
    {
      //Fazendo a senoide....
      t_start = 30.0+i*25;
      //t_end = expSimulationTime;
      t_end = 4000+i*25; 
    }    

    else
    {
      srand((unsigned) time(NULL));
      t_start = 5.0 + (2*expSimulationTime/3) + i + (float)((rand()%10000)/100000);
      srand((unsigned) time(NULL));
      t_end = rand()%(int)(expSimulationTime-t_start); //gera um número entre zero e expSimulationTime-t_start,ou seja,
                                                     //ao se somar t_start,ele vai no máximo a expSimulationTime
      t_end =t_start+t_end;
    }
    std::cout << "Fluxo: " << stoi(src)<<"-->"<< stoi(dest)<<"\n";

    std::cout << "t_start: " << t_start << ", t_end: " << t_end << "\n";

   AjustarInicioTerminoCliente(parClientApps,
                               stoi(src),
                               stoi(dest),
                               //5.0+i+((rand()%10)/10),
                               //2.0+4*i+1.0);
                               t_start,
                               //expSimulationTime,
                               t_end);
    //cout << "Aplicações Clientes agendadas com sucesso!!" <<"\n";
   
  }

  //myPause();

}

bool AjustarAplicacaoServidorTCP(ApplicationContainer parServerApps[][MAX_TERMINALS],
                                 PacketSinkHelper *parTCPSinkServer[][MAX_TERMINALS], 
                                 NodeContainer parPointToPointNodesPairsTerm[][MAX_ROUTERS],
                                 Ipv4InterfaceContainer parPointToPointInterfacesTerm[][MAX_ROUTERS],
                                 int parIdSrc,
                                 int parIdDestination)
{
  uint16_t sinkPort = 8080;


 /*=====================================================================================
  11 Out 22:
  Aparentemente não é possível mais de um sinkServer em um mesmo host. Por isso as 9 linhas abaixo

  *=====================================================================================*/

  for (int i = 0; i< MAX_TERMINALS; i++)
  {
    if(parTCPSinkServer[i][parIdDestination])
    {
      parTCPSinkServer[parIdSrc][parIdDestination] = parTCPSinkServer[i][parIdDestination];
      parServerApps[parIdSrc][parIdDestination] = parServerApps[i][parIdDestination];
      return false;
    }


  }
    

  parTCPSinkServer[parIdSrc][parIdDestination] = new PacketSinkHelper ("ns3::TcpSocketFactory",
                                            InetSocketAddress (Ipv4Address::GetAny (), sinkPort)); //Na dúvida do GetAny...É recebe de qualquer endereço
  parServerApps[parIdSrc][parIdDestination] = 
                                            parTCPSinkServer[parIdSrc][parIdDestination]->
                                            Install(pointToPointNodesPairsTerm[parIdDestination][assTerminalRoteador[parIdDestination]].Get(1));
                                            // 1 é o terminal pelo fato de o roteador ser
                                            //Assim, o roteador  seria Get(0)

  std::cout <<"=========" << "[" << parIdDestination<<"]"<<"["<<assTerminalRoteador[parIdDestination]<<"]"<<"\n";
  /*=====================================================================================
  *A linha abaixo, inicializando a variável numAplic, que recupera a última aplicação, 
  *que é aquela instalada acima, foi concebida depois de um erro em que o TraceConnectWithoutContext
  *não funcionava para alguns nós. Isso acontecia por que antes a linha de comando era conforme 
  *a seguir:
  *StaticCast <PacketSink>(parPointToPointNodesPairsTerm[parIdDestination][assTerminalRoteador[parIdDestination]]
  *.Get(1)->GetApplication(0))->TraceConnectWithoutContext("RxWithAddresses", MakeCallback(&ReceivePackage));
  *O que fazia com que sempre a aplicação (0) fosse o traceSource, o que na verdade poderia, por exemplo,
  *estar retornando um socket e não um PacketSink, caso o nó já tivesse aparecido como origem de tráfego
  *em alguma linha anterior. Daí a necessidade se recuperar a última aplicação, que, com certeza é a que
  *é a fonte dos sinais de recepção.
  *=====================================================================================*/
  
  int numAplic = pointToPointNodesPairsTerm[parIdDestination][assTerminalRoteador[parIdDestination]].Get(1)->GetNApplications();
  StaticCast <PacketSink>(pointToPointNodesPairsTerm[parIdDestination][assTerminalRoteador[parIdDestination]]
                                    .Get(1)->GetApplication(numAplic-1))->
                                    TraceConnectWithoutContext("RxWithAddresses", MakeCallback(&ReceivePackage));

  return true;
}


void AjustarAplicacaoClienteTCP(Ptr<MyApp> parClientApps[][MAX_TERMINALS],
                                Ptr<Socket> parTCPClientSocket[][MAX_TERMINALS], 
                                NodeContainer parPointToPointNodesPairsTerm[][MAX_ROUTERS], 
                                Ipv4InterfaceContainer parPointToPointInterfacesTerm[][MAX_ROUTERS],
                                int parIdSrc,
                                int parIdDestination
                                )
{

  //UdpEchoClientHelper echoClient (csmaInterfaces[idRedeServidor].GetAddress(idServidorNaRede), UDP_PORT);
 

  //parEchoClient[parIdSrc][parIdDestination].SetAttribute("RemoteAddress",parNosRede[parIdSrc][parIdDestination].GetAddress(1));
  //parEchoClient[parIdSrc][parIdDestination].SetAttribute("RemotePort",UDP_PORT);

/*=====================================================================================/
 * Observe que as aplicações são endereçadas fim-a-fim, ou seja, um
 parClientApps[3][2] indica que haverá um fluxo com origem em 3 e destino em 2,
 portanto, haverá um cliente no nó 3 (src) e um servidor no nó 2. 
 A seguinte conotação pode ser dada a um parClientApps[3][2]:
 "Eu sou um cliente para suportar o tráfego com origem em 3 e destino em 2"

 Já os enlaces são endereçados entre os terminais e os roteadores. Dessa forma, não
 há uma correspondencia direta entre 
 parClientApps[3][2], que indica um fluxo entre os terminais 3  e 2
 e
 parPointToPointNodesPairsTerm[3][2], que indica que o nó 3 está ligado ao
 ROTEADOR 2. Por isso precisamos do assTerminalRoteador.
======================================================================================*/
 
  uint16_t sinkPort = 8080;
  
  Address sinkAddress = (InetSocketAddress(parPointToPointInterfacesTerm[parIdDestination][assTerminalRoteador[parIdDestination]].GetAddress (1), sinkPort));

  //TypeId tid = TypeId::LookupByName ("ns3::TcpNewReno");
  //Config::Set ("/NodeList/*/$ns3::TcpL4Protocol/SocketType", TypeIdValue (tid));
  parTCPClientSocket[parIdSrc][parIdDestination] = Socket::CreateSocket(pointToPointNodesPairsTerm[parIdSrc][assTerminalRoteador[parIdSrc]].Get(1),
                                                                        TcpSocketFactory::GetTypeId ());


  //default
  //parTCPClientSocket[parIdSrc][parIdDestination] = Socket::CreateSocket(pointToPointNodesPairsTerm[parIdSrc][assTerminalRoteador[parIdSrc]].Get(1),TcpSocketFactory::GetTypeId ());
 
 
  //DynamicCast <TcpSocketBase> (parTCPClientSocket[parIdSrc][parIdDestination])->SetInitialCwnd(1);
  
  //parTCPClientSocket[parIdSrc][parIdDestination]->TraceConnectWithoutContext ("Tx", MakeCallback(&SentPackage));
  parTCPClientSocket[parIdSrc][parIdDestination]->TraceConnect ("Tx",to_string(parIdSrc)+">"+to_string(parIdDestination), MakeCallback(&SentPackage));
  
  //parTCPClientSocket[parIdSrc][parIdDestination]->TraceConnectWithoutContext ("Rx", MakeCallback(&ReceivedFromServer));
  parTCPClientSocket[parIdSrc][parIdDestination]->TraceConnect("Rx",to_string(parIdSrc)+">"+to_string(parIdDestination), MakeCallback(&ReceivedFromServer));
  parTCPClientSocket[parIdSrc][parIdDestination]->TraceConnect("CongestionWindow", to_string(parIdSrc)+">"+to_string(parIdDestination) ,MakeCallback (&CwndChange));
  if(online)
  {
    SetNeuralMode(neural_mode,parIdSrc,parIdDestination);
    cout << "\n nó " << parIdSrc << " inteligente\n";
    //myPause();
  }
   
  /*
  //from  https://intronetworks.cs.luc.edu/current2/mobile/ns3.html 
  int tcpSegmentSize = 1000;
  Config::SetDefault ("ns3::TcpSocket::SegmentSize", UintegerValue (tcpSegmentSize));
  Config::SetDefault ("ns3::TcpSocket::DelAckCount", UintegerValue (0));
  Config::SetDefault ("ns3::TcpL4Protocol::SocketType", StringValue ("ns3::TcpReno"));
  Config::SetDefault ("ns3::RttEstimator::MinRTO", TimeValue (MilliSeconds (500)));

  */

  expSegSize=1500;//Descobrir como pegar o default
  /*=====================================================================================/
 Aparentemente o TimeStamp é default, diante do que está escrito em 
   96 .AddAttribute ("Timestamp", "Enable or disable Timestamp option",
   97                    BooleanValue (true),

   Arquivo tcp-socket-base.cc
======================================================================================*/
  
  parClientApps[parIdSrc][parIdDestination] = CreateObject<MyApp> ();
  //Arnazenando os fluxos ativos
  activeFlows[numActiveFlows][0]=parIdSrc;
  activeFlows[numActiveFlows][1]=parIdDestination;
  numActiveFlows++;
 
  if(expContNumLongFlows <= expContNumShortFlows && expContNumLongFlows < expNumlongFlows)
  {
    parClientApps[parIdSrc][parIdDestination]->Setup(parTCPClientSocket[parIdSrc][parIdDestination],
                                                   sinkAddress,expPacketSize,DataRate (expAppDataRate), expLongFileSize);

    

    expContNumLongFlows++;
    parClientApps[parIdSrc][parIdDestination]->setFlowType(LONG_FLOW);
    std::cout << "Criado Longo "<< expContNumLongFlows << "\n";
  }

  else
  {
    parClientApps[parIdSrc][parIdDestination]->Setup(parTCPClientSocket[parIdSrc][parIdDestination],
                                                   sinkAddress,expPacketSize,DataRate (expAppDataRate), expShortFileSize[expContNumShortFlows%2]);

    if(!(expContNumShortFlows%2))
      parClientApps[parIdSrc][parIdDestination]->setFlowType(VERYSHORT_FLOW);
    else
      parClientApps[parIdSrc][parIdDestination]->setFlowType(SHORT_FLOW);
    
    expContNumShortFlows++;
    std::cout << "Criado Curto "<< expContNumShortFlows << "\n";
  }
  pointToPointNodesPairsTerm[parIdSrc][assTerminalRoteador[parIdSrc]].Get(1)->AddApplication(parClientApps[parIdSrc][parIdDestination]);
 //Associando a aplicação ao fluxo
  hashIdAppAppFlow[parClientApps[parIdSrc][parIdDestination]->getAppId()][0] = parIdSrc;
  hashIdAppAppFlow[parClientApps[parIdSrc][parIdDestination]->getAppId()][1] = parIdDestination;

    
}



void AjustarInicioTerminoServidor(ApplicationContainer parServerApps[][MAX_TERMINALS], int parIdSrc, int parIdDestination,float t_0, float t_f)
{
    
    cout << "Programou Servidor\n";
    myPause();
    parServerApps[parIdSrc][parIdDestination].Start(Seconds (t_0));//Todos começamdo e terminando no mesmo instante, mas é possível onfigurar 
    parServerApps[parIdSrc][parIdDestination].Stop(Seconds (t_f));//qualquer tempo para cada fluxo.

}

void AjustarInicioTerminoCliente(Ptr<MyApp> parClienterApps[][MAX_TERMINALS],int parIdSrc, int parIdDestination,float t_0, float t_f)
{

  parClienterApps[parIdSrc][parIdDestination]->SetStartTime(Seconds (t_0));
  lastTimeCwndIsZero[parIdSrc][parIdDestination]=Seconds(t_0).GetSeconds();
  parClienterApps[parIdSrc][parIdDestination]->SetStopTime(Seconds (t_f));
  marcaTempoChegadaAckAnterior[parIdSrc][parIdDestination] = MilliSeconds(t_0*1000).GetInteger();
  marcaTempoRefletidaAckAnterior[parIdSrc][parIdDestination] = MilliSeconds(t_0*1000).GetInteger();
  //printf("marcaChegadaAck inicial[%d][%d]=%ld\n", parIdSrc, parIdDestination, marcaTempoChegadaAckAnterior[parIdSrc][parIdDestination]);

}
/*================================================================================================ 
Criando as ligações LAN. Em princípio, esse  é o tipo de ligação entre os terminais. Então 
criou-se um vetor  de numRedes PointToPointHelper.
O princípio é configurar um tipo de enlace para cada rede a ser formada. No nosso caso, 
um elace csma para cada terminal e o respectivo roteador (CsmaHelper csma[MAX_TERMINALS]).
Posteriomente, os nós são grupados pelos enlaces que vão utilizar. No nosso caso, formou-se 
grupos(pares), com um terminal e um rotador (csmaNodesPairs).
Depois associa-se os devices com o respectivo enlace e o grupo de nós que compartilha aquele 
enlace (csmaDevices[i] = csma[i].Install (csmaNodesPairs[i])).
Observe que é csmaDevices, no plural. No caso foram criados dois, pois for parassado um  grupo, 
contendo um par de nós (csmaNodesPairs[i])
Por fim,  associa-se esses devices a interfaces com os respectivos endereços, por meio] do 
comando csmaInterfaces[i] = address.Assign(csmaDevices[i]);
======================================================================================================*/
 /*============================================================================================
     Os devices devem ser configurados por redes. Todos os devices de uma mesma rede
     devem formar um grupo a ser configurado pela chamada de um conjunto de comandos
     semelhantes aos seguintes:
     Ipv4AddressHelper address;
     address.SetBase ("10.1.1.0", "255.255.255.0");
     Ipv4InterfaceContainer p2pInterfaces;
     p2pInterfaces = address.Assign (p2pDevices);
     Observe que assim os endereço (address) são associados a interfaces (p2interfaces), associadas a devices,
     associadas a nós e enlaces.
  ============================================================================================*/

  
void CriarLigacoesTerm(vector <string> parVetTopology)
  
{
  
  Ipv4AddressHelper address;
  std::string baseAddress;
  std::string sufixAddress;
  //para extração dos tokens
  std::istringstream *tokenStream;
  string token;
  string term;
  string rot;
  string bw;
  string rtt;
  //float realRtt;
  int quantLigacoes;
  
  
  quantLigacoes = parVetTopology.size();
  /*============================================================================================
  numRouters-1 primeiras linhas são ligações do roteador
  Observe que, se são numRouters-1, não deve existir ligação do último roteador com o primeiro.
  ============================================================================================*/

  for (int i = numRouters-1; i < quantLigacoes; ++i)//i linha a linha
  {
    tokenStream = new std::istringstream(parVetTopology[i]);
  /*============================================================================================
   Agora, nas ~oito linhas a seguir, vamos para a ligação entre os terminais e os roteadores, que nesse caso
   serão sempre p2p. Se a linha 1 começar com "2 1", isso indica
   que deve haver um enlace enre o roteador 1 e o terminal 2. Daí o pointToPointNodesPairsTerm[2][1]
   guardará a ligação entre o terminal 2 e o roteador 1. Observe que o endereçamento dos pares
   de nós é em função da ordem em que aparecem na configuração.
   as linhas abaixo tentam configurar 
   o link[1] (pointToPointNodesPairsTerm[2][1]) será entre R1--T2
   O vetor "pointToPointNodesPairsTerm" abaixo destina-se a concentrar os roteadores e terminais
   interligados por p2p. 
   O vetor pointToPointEnlaceTerm é o enlace da ligação enre o terminal e o roteador.
   Conforme comentário acima (R1--T1), R1--T2, conforme arquivo de configuração...
   ============================================================================================*/
    //lendo terminal da linha
    std::getline(*tokenStream, term, ' ');
    std::cout << "term: " << term << "\n";    
    //lendo roteador da linha
    std::getline(*tokenStream, rot, ' ');
    std::cout << "rot: " << rot << "\n";

   
    //lendo velocidade da linha
    std::getline(*tokenStream, bw, ' ');
    bw=bw+"ps";//"ps", pois do arquivo já vem  o "Mb" 
    std::cout << bw << "\n";
    //lendo rtt da linha
    std::getline(*tokenStream, rtt, ' ');
    //cout << rtt << "\n";
    //cout << rtt.length() << "\n";
    //cout << rtt.substr(0,rtt.length()-2)<< "\n";
    //realRtt = std::stof(rtt.substr(0,rtt.length()-2));
    //cout << "real" << realRtt << "\n";

    /*============================================================================================
     ###################CUIDADO#############################
     *O dataRate é atributo do device
     *O delay é atributi do canal...
     *Daí essas grandezas serem ajustadas por métodos diferentes nas duas linas abaixo ()
    ============================================================================================*/

    pointToPointEnlaceTerm[stoi(term)][stoi(rot)].SetDeviceAttribute ("DataRate", StringValue (bw.c_str()));
    //-3, due blank space at the end of rtt string                
    pointToPointEnlaceTerm[stoi(term)][stoi(rot)].SetChannelAttribute("Delay", TimeValue(MilliSeconds(stod(rtt.substr(0,rtt.length()-3)))));
    pointToPointNodesPairsTerm[stoi(term)][stoi(rot)].Add (routers.Get (stoi(rot))); //adicionando o roteador 
    pointToPointNodesPairsTerm[stoi(term)][stoi(rot)].Add (terminals.Get (stoi(term))); //adicionando o tetminal.
    assTerminalRoteador[stoi(term)] = stoi(rot);

    //printf("passou!!\n");

  /*============================================================================================
     Agora é a vez dos devices, que serão instalados dois por grupo de ligações
     acima criados
  ============================================================================================*/
  std::cout << "passou Delay Rate!!"<<"\n";
  pointToPointDevicesTerm[stoi(term)][stoi(rot)] = pointToPointEnlaceTerm[stoi(term)][stoi(rot)].Install (pointToPointNodesPairsTerm[stoi(term)][stoi(rot)]);
  
/*
  if(stoi(rot) == numRouters-1)
  {
      cout << "Ajustando erro\n";
      Ptr<RateErrorModel> em = CreateObject<RateErrorModel>();
      em->SetAttribute("ErrorRate", DoubleValue(0.00001));
      pointToPointDevicesTerm[stoi(term)][stoi(rot)].Get(1)->SetAttribute("ReceiveErrorModel", PointerValue(em));
  }
  
*/




  //myPause();
  /*A lógica dos endereços é: 10."Roteador"."vertice do roteador"."x"
    Ex.: 10.0.0.x
            | | |
            | | |(distribuído automaticamente pelo ns3)
            | |
            | vértice 0
            R0
  */
   //cout << "passou!!"<<"\n";
    baseAddress = string("10") +string(".") +rot + string(".") +to_string(numInterfacesUsadasNoRoteador[stoi(rot)])+".";
    std::cout << "baseAdd "<< baseAddress<<"\n";
    numInterfacesUsadasNoRoteador[stoi(rot)]++;
    //sufixAddress = std::__cxx11::to_string(term+1);
    baseAddress = baseAddress+ string("0");
    address.SetBase(baseAddress.c_str(), "255.255.255.0");
    pointToPointInterfacesTerm[stoi(term)][stoi(rot)] = address.Assign(pointToPointDevicesTerm[stoi(term)][stoi(rot)]);

    
    delete tokenStream;    

  }
  //myPause();
 
}


/*===================================================================================
    Criando as ligações ponto-a-ponto. Em princípio, esse é o tipo de ligação entre os 
    roteadores. Então, criou-se um vetor de numRouters-1 PointToPointHelper.
  =====================================================================================*/

void CriarLigacoesRouters(vector <string> parVetTopology)                          
{
  Ipv4AddressHelper address;
  std::string baseAddress;
  std::string sufixAddress;
  std::istringstream *tokenStream;
  string token;
  string rot1;
  string rot2;
  string bw;
  string rtt;
  string rtt_value;
    
  for(int i = 0; i < numRouters-1; i++)
  {
    tokenStream = new std::istringstream(parVetTopology[i]);
    // lendo roteador 1 da linha
    std::getline(*tokenStream, rot1, ' ');
    std::cout << "rot01: " << rot1 << "stoi\n";    
    //lendo roteador  2 da linha
    std::getline(*tokenStream, rot2, ' ');
    std::cout << "rot02: " << rot2 << "stoi\n"; 
/*===================================================================================
    Observe que, para numRouters roteadores, há numRouters-1 ligações, uma vez que
    assume-se uma única ligação entre os roteadores. É bom prestar atenção
    neste detalhe, pois há model-topologies com ligações de ida e volta.
    Manter a ligação uma singular entre os roteadores facilida na captura da
    fila da interface.
  =====================================================================================*/
    
    if(stoi(rot1) >= stoi(rot2))
    {
      std::cout << "Not a foward router link. Please review model-topology.txt\n";
      exit(0);
    }
    //std::cout << "rot02: " << rot2 << "\n";
    //lendo velocidade da linha
    std::getline(*tokenStream, bw, ' ');
    bw=bw+"ps";
    //std::cout << bw << "\n";
    //lendo rtt da linha
    std::getline(*tokenStream, rtt, ' ');
    std::cout << rtt << "\n"; 
    //std::cout << rtt.substr(0,rtt.length()-3)<< "\n";
    rtt_value = rtt.erase(rtt.length()-2,rtt.length());
    std::cout << rtt_value<< "\n";
    //myPause();
    pointToPointRouters[stoi(rot1)][stoi(rot2)].SetDeviceAttribute ("DataRate", StringValue (bw.c_str()));
    pointToPointRouters[stoi(rot1)][stoi(rot2)].SetChannelAttribute ("Delay", TimeValue(MilliSeconds(stod(rtt_value))));

    if(stoi(rot1) == numRouters-2 && stoi(rot2) == numRouters-1)
    {
      Simulator::Schedule (Seconds(3.0) ,&ChangeNetworkParameters,stoi(rot1),stoi(rot2),0);
    }

    //Ajustando erro entre o penúltimo e o último roteador

    //@Ptr<PointToPointNetDevice> anteriorRouterDevice = DynamicCast<PointToPointNetDevice>(pointToPointDevicesRouters[assTerminalRoteador[idAckSender]-1][assTerminalRoteador[idAckSender]].Get(0))
    pointToPointNodesPairsRouters[stoi(rot1)][stoi(rot2)].Add (routers.Get (stoi(rot1)));//Adding first
    pointToPointNodesPairsRouters[stoi(rot1)][stoi(rot2)].Add (routers.Get (stoi(rot2)));

    
  
  
   /*===================================================================================
     Agora é a vez dos devices, que serão instalados dois por grupo de roteadores
     acima criados.
     A linha abaixo pode ser interpretada da seguinte forma:
     Instale (install) um emlace p2p entre os nós presentes em pointToPointNodesPairsRouters,
     ligando-os por meio de dois devices, com as características presentes em pointToPointRouters
     e armazene os devices da ligação em pointToPointDevicesRouters
  =====================================================================================*/
    pointToPointDevicesRouters[stoi(rot1)][stoi(rot2)] = pointToPointRouters[stoi(rot1)][stoi(rot2)].Install (pointToPointNodesPairsRouters[stoi(rot1)][stoi(rot2)]);    




    std::string baseAddress = "20.1.";
    sufixAddress = std::__cxx11::to_string(i);
    baseAddress = baseAddress+sufixAddress+".0";
    //cout << "addr: " << baseAddress << "\n";
    address.SetBase(baseAddress.c_str(), "255.255.255.0");
    pointToPointInterfacesRouters[stoi(rot1)][stoi(rot2)] = address.Assign(pointToPointDevicesRouters[stoi(rot1)][stoi(rot2)]);

    delete tokenStream;

    //myPause();

  }    
  
  std::cout << "Rede de Roteadores configurada com sucesso!!" <<"\n";
  //myPause();
}



void ExtrairConfiguracoes (string parPathTopology, string parPathFlow, vector <string>& parVetTopology, vector <string>& parVetFlows) 
{
    std::string linhaTopology, linhaFlow;

    //cout << parPathTopology << "\n";
    //cout << parPathFlow << "\n";

    ifstream topology (parPathTopology);
    ifstream flow(parPathFlow);

    if (topology.is_open() and flow.is_open())
    {
        while ( getline (topology,linhaTopology) )
        {
            if(linhaTopology[0]!='#')//evitar comentários
              parVetTopology.push_back(linhaTopology);          
        }
        topology.close();

        while ( getline (flow,linhaFlow) )
        {
            if(linhaFlow[0]!='#')//evitar comentários
              parVetFlows.push_back(linhaFlow);
          
        }
        flow.close();


  
    }

    else
    { 
      std::cout << "Unable to open file\n"; 
      exit(0);
    }
}







/*===================================================================================
    Agora, o os clientes serão MyApp, inicializados por CreateObject<MyApp> ();
    que, por fim serão liberados pelo Destroy()
  =====================================================================================*/
/*
void InicializarEchoClient(UdpEchoClientHelper *parEchoClient[][MAX_TERMINALS])
{
 for(int i=0; i < MAX_TERMINALS; i++)
  for(int j=0; j < MAX_TERMINALS; j++)
   parEchoClient [i][j]=0; 
}
*/
void FinalizarEchoClient(UdpEchoClientHelper *parEchoClient[][MAX_TERMINALS])
{
 for(int i=0; i < MAX_TERMINALS; i++)
  for(int j=0; j < MAX_TERMINALS; j++)
  {
    if(parEchoClient[i][j])
    {
      //cout << "Liberando echoClinte " <<"("<< i<<"," << j <<")"<<"\n";
      delete parEchoClient[i][j];
      
    }
  }
   
}

void ImprimirVetorString(vector<string> parVetString)
{
  int sizeVet = parVetString.size();

  for(int i=0; i < sizeVet; i++)
  {
    std::cout << i <<": "<< parVetString[i] << "\n";
  }
  
}

 void ImprimirVetorInteiros(int * parVetor, int parSize)
 {
    for(int i=0; i < parSize; i++)
    {
      std::cout << i <<": "<< parVetor[i] << "\n";
    }
  
 }

