#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 11:39:09 2024

@author: ns
"""
import os

import xml.etree.ElementTree as ET


class FlowMonitor():

    #resultadoTreinamento = np.eye(10)

    def __init__(self,parXMLPath,parTcpVariante,parNumFluxos,parOutputDir):
    
        self.xmlPath = parXMLPath
        self.tcpVariante = parTcpVariante
        self.numFluxos = parNumFluxos
        self.outputDir=parOutputDir
        self.tree = ET.parse(self.xmlPath)
        self.root = self.tree.getroot()
        self.lstFlowIds=[]
    
    def ShowFileInformation(self):
        
        print(self.root.tag)
        print("First Child:")
        print(self.root[0].tag)
    
    def GetFlowIds(self):
        self.lstFlowIds.clear()
        for ipv4Attrib in self.root.iter('Ipv4FlowClassifier'):
            for child in ipv4Attrib:
                #print (child.tag, child.attrib['flowId'], child.attrib['sourceAddress'])
                if child.tag == 'Flow':
                    if(child.attrib['sourceAddress'][0:4] == '10.0'):
                        self.lstFlowIds.append(child.attrib['flowId'])
        #print(self.lstFlowIds)
    
    def GetLstRxBytes(self):
        lstRxBytes = ["0"]*len(self.lstFlowIds)
        #print(len(self.lstFlowIds))
        #print(len(lstRxBytes))
        for stats in self.root.iter('FlowStats'):
           for child in stats:
               if child.tag == 'Flow':
                   if child.attrib['flowId'] in self.lstFlowIds:
                       #print("index ", self.lstFlowIds.index(child.attrib['flowId']))
                       lstRxBytes[self.lstFlowIds.index(child.attrib['flowId'])] = child.attrib['rxBytes'] #Fazendo um hash
                       #print (child.attrib['flowId'],",",child.attrib['rxBytes'])
        return lstRxBytes
            
    def UpdateCsvFlowFile(self):
        self.GetFlowIds()
        lstRxBytes = self.GetLstRxBytes()
        #print(lstRxBytes)
        #print("numFlows: ", len(lstRxBytes))
        if(not os.path.isfile(self.outputDir+"/FlowsRx.csv")):              
            with open(self.outputDir+"/FlowsRx.csv", "a") as f:
                f.write("Tcp_Variante, ")
                f.write("Num_Fluxos, ")
                f.write("Flow_Id, ")
                f.write("Rx (bytes), ")
                f.write("Rx (Mbytes), ")
                f.write("TPut Med, ")
                f.write("TPut Med Norm\n")
                

        tputMB=0.0
        tputMed=0.0
        tputNorm=0.0
        tputBytesTotal=0.0
        tputMBTotal = 0.0
        tputMedTotal=0.0
        tputNormTotal=0.0

        with open(self.outputDir+"/FlowsRx.csv", "a") as f:
            for i in range(len(lstRxBytes)):                
                f.write(self.tcpVariante+", ")
                f.write(self.numFluxos+", ")
                f.write(self.lstFlowIds[i]+", ")
                f.write(lstRxBytes[i]+", ")
                tputMB = float(lstRxBytes[i])/2**20
                f.write(str(tputMB)+", ")
                tputMed = float(tputMB)/1800
                f.write(str(tputMed)+", ")
                tputNorm = tputMed/9.5366 #(9.5366 e o Tput esperedo, bem proximo da taxa de gargalo, da qula foi subtraida o erro)
                f.write(str(tputNorm)+"\n")
                tputBytesTotal = tputBytesTotal + float(lstRxBytes[i])
                tputMBTotal = tputMBTotal + tputMB
                tputMedTotal = tputMedTotal+tputMed
                tputNormTotal = tputNormTotal + tputNorm
    
            f.write(self.tcpVariante+", ")
            f.write(self.numFluxos+", ")
            f.write("Total_"+self.tcpVariante+"_"+self.numFluxos+", ")
            f.write(str(tputBytesTotal)+", ")
            f.write(str(tputMBTotal)+", ")
            f.write(str(tputMedTotal)+", ")
            f.write(str(tputNormTotal)+"\n")
        
     
        
objFlowMonitor =  FlowMonitor("/home/ns/ns3-workspace/source/ns-3.40/Bbr1L.xml","TcpNewReno","20",".")
objFlowMonitor.ShowFileInformation()
objFlowMonitor.GetFlowIds()
print(objFlowMonitor.GetLstRxBytes())
objFlowMonitor.UpdateCsvFlowFile()