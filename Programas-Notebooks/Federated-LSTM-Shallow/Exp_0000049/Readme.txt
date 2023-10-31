Aumentando a margem de segurança 40X70


if(router_queue_ewma <= 40 && Samples1 < max1Samples )
  {
    networkSituation = 1;
    get_1sample_interval = 0;
    srand((unsigned) time(0)+rand());
    flagToGet1Sample = rand()%20;
      
  }

  else if(router_queue_ewma >= 70 && Samples2 < max2Samples)
  {
    networkSituation = 2;
    get_2sample_interval = 0;    
    srand((unsigned) time(0)+rand());
    flagToGet2Sample = rand()%20;
    
  }


td::string expBottleNeck = "2Mb"; //destination nodes link speed. Must be set in model flow
//float expWeightExpon = 1.0/8.0;//sampleRTT = (1-weightExpon)sampleRTT+weightExpon*RTT
float expWeightExpon = 80.0/100.0;//95.0/100.0;//sampleRTT = (1-weightExpon)sampleRTT+weightExpon*RTT
float expWeightExponQueue = 80.0/100.0;
uint32_t expPacketSize = 1040;
uint64_t expShortFileSize[] = {10000,100000}; // Amazon Total Page Size - 4.06MB, by https://gtmetrix.com
uint64_t expLongFileSize =  4000000000;/*40000;*/ //4GB
double expSimulationTime =120*60.0;//120*60.0; para treinamento 600(10h)
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


conclusões

Ficou ótimo

[[234   1]
 [ 17 208]


Posteriormente foi retirado o DeleteInconsistence. Os resultados permaneceram bons!!!

[[560  51]
 [ 38 778]]

[[600  15]
 [ 43 769]]

[[557  38]
 [ 53 779]]
#############################DATAMINING##########################################################################################


float expWeightExpon = 60.0/100.0;//95.0/100.0;//sampleRTT = (1-weightExpon)sampleRTT+weightExpon*RTT
float expWeightExponQueue = 60.0/100.0;
uint32_t expPacketSize = 1040;
uint64_t expShortFileSize[] = {10000,100000}; // Amazon Total Page Size - 4.06MB, by https://gtmetrix.com
uint64_t expLongFileSize =  4000000000;/*40000;*/ //4GB
double expSimulationTime =120*60.0



/*Rerirado pois as inconsistencias estão sendo feitas no python
        if(!online) //A princípio o trecho dentro deste if só deve ser ativado se online é false, pois os returns podem
                    //restrinir a atualização do estado.
        {
          if(numAckReceived[idAckReceiver][idAckSender] > 21)
          {
.
.
.
.
.





Início e término dos fluxos!!!!


if(!stoi(src))// Nó zero mono. Nó 1 era o mestre para levantar dados, ficando toda simulação
    {

      t_start = 30.0;
      t_end = expSimulationTime; //gera um número entre zero e expSimulationTime-t_start,ou seja,
                                                     //ao se somar t_start,ele vai no máximo a expSimulationTime
      //t_end = 36000;

    }

    else if(parClientApps[stoi(src)][stoi(dest)]->getFlowType() == LONG_FLOW)
    {
      //cout << Fazendo a senoide....
      cout << "Ajustando início e término aplicação: " <<parClientApps[stoi(src)][stoi(dest)]->GetNode()->GetId() <<"\n";
      //t_start = 30.0+(i-1)*7200;
      t_start = 30.0+i*10;
      t_end = expSimulationTime;
      //t_end = 30000+(i-1)*10000; 
      //t_end = 33000;
        //myPause();
    }    






defaultCongestion = "ns3::TcpNewReno";



  ExtrairConfiguracoes((workDir+"/model-topology-pincel-20CL-20S.txt").c_str(),
                       (workDir+"/model-flow-pincel-20CL-20S.txt").c_str(),
                       vetTopology,
                       vetFlows);














#Lembre que não se pode pular números na sequencia de terminais;
#se hover  porexemplo  5 terminais  devem ser designados 0 1 2 3 4e não 1 4 6... ou de qualquer outra forma que
#pule números
0 1 10Mb 100ms
0 0 1000Mb 10ms
1 0 1000Mb 10ms
2 0 1000Mb 10ms
3 0 1000Mb 10ms
4 0 1000Mb 10ms
5 0 1000Mb 10ms
6 0 1000Mb 10ms
7 0 1000Mb 10ms
8 0 1000Mb 10ms
9 0 1000Mb 10ms
10 0 1000Mb 10ms
11 0 1000Mb 10ms
12 0 1000Mb 10ms
13 0 1000Mb 10ms
14 0 1000Mb 10ms
15 0 1000Mb 10ms
16 0 1000Mb 10ms
17 0 1000Mb 10ms
18 0 1000Mb 10ms
19 0 1000Mb 10ms
20 1 1000Mb 100ms
21 1 1000Mb 100ms
22 1 1000Mb 100ms
23 1 1000Mb 100ms
24 1 1000Mb 100ms
25 1 1000Mb 100ms
26 1 1000Mb 100ms
27 1 1000Mb 100ms
28 1 1000Mb 100ms
29 1 1000Mb 100ms
30 1 1000Mb 100ms
31 1 1000Mb 100ms
32 1 1000Mb 100ms
33 1 1000Mb 100ms
34 1 1000Mb 100ms
35 1 1000Mb 100ms
36 1 1000Mb 100ms
37 1 1000Mb 100ms
38 1 1000Mb 100ms
39 1 1000Mb 100ms











####################################################################################################################################
