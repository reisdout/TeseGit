#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 11:39:09 2024

@author: ns
"""

import xml.etree.ElementTree as ET


class FlowMonitor():

    #resultadoTreinamento = np.eye(10)

    def __init__(self,parXMLPath):
        
        self.xmlPath = parXMLPath
        self.tree = ET.parse(self.xmlPath)
        self.root = self.tree.getroot()
        self.lstFlowIds=[]
    
    def ShowFileInformation(self):
        
        print(self.root.tag)
        print("First Child:")
        print(self.root[0].tag)
    
    def GetFlowIds(self):
        for ipv4Attrib in self.root.iter('Ipv4FlowClassifier'):
            for child in ipv4Attrib:
                #print (child.tag, child.attrib['flowId'], child.attrib['sourceAddress'])
                if(child.attrib['sourceAddress'][0:4] == '10.0'):
                    self.lstFlowIds.append(child.attrib['flowId'])
        print(self.lstFlowIds)
        
    def GetRxBytes(self):
        for stats in self.root.iter('FlowStats'):
            for child in stats:
                if child.tag == 'Flow':
                    if child.attrib['flowId'] in self.lstFlowIds:
                        print (child.attrib['flowId'],",",child.attrib['rxBytes'])
                
        
        
objFlowMonitor =  FlowMonitor("/home/ns/ns3-workspace/source/ns-3.40/Bbr1L.xml")
objFlowMonitor.ShowFileInformation()
objFlowMonitor.GetFlowIds()
objFlowMonitor.GetRxBytes()