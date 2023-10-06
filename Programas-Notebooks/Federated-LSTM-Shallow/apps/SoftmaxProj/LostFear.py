# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:28:32 2023

@author: visitante
"""

   def NormalizeFeatures(self, data, parFromFile,par_exp_dir):
      
      print("Normalize do roteador!!!")
      
      ack_ewma_normalizer=1.0
      send_ewma_normalizer=1.0
      min_rtt=1.0
      rtt_ratio_normalizer=1.0
      cwnd_normalizer=1.0
      
      #Obtendo o RTT Ratio
   
      #data['rtt_ratio'] = data['rtt_ratio'].div(264)#264 é o rtt min do fluxo de treinamento.
       
      if(parFromFile):
         ack_ewma_normalizer, send_ewma_normalizer,min_rtt,rtt_ratio_normalizer,cwnd_normalizer = mrs.ReadNormalizationFactors(par_exp_dir)
 
       
      else: 
          ack_ewma_normalizer = data['ack_ewma(ms)'].max()
          send_ewma_normalizer=data['send_ewma(ms)'].max()
          min_rtt=data['rtt_ratio'].min()
          cwnd_normalizer=data['cwnd_(Bytes)'].max()

      data['rtt_ratio'] = data['rtt_ratio'].div(min_rtt)
      if(not (parFromFile)):
          rtt_ratio_normalizer = data['rtt_ratio'].max()
      #data['ack_ewma(ms)'] = data['ack_ewma(ms)'].div(ack_ewma_normalizer)
      #data['send_ewma(ms)'] = data['send_ewma(ms)'].div(send_ewma_normalizer)       
      data['rtt_ratio'] = data['rtt_ratio'].div(rtt_ratio_normalizer)
      #data['cwnd (Bytes)'] = data['cwnd (Bytes)'].div(cwnd_normalizer)
       
      if(not parFromFile):
          file1 = open(par_exp_dir+"/normalization_factors.txt", 'w')
          file1.writelines("ack_ewma: "+str(ack_ewma_normalizer)+"\n")
          file1.writelines("send_ewma: "+str(send_ewma_normalizer)+"\n")
          file1.writelines("rtt_min: "+str(min_rtt)+"\n")
          file1.writelines("rtt_ratio: "+str(rtt_ratio_normalizer)+"\n")
          file1.writelines("cwnd_(Bytes): "+str(cwnd_normalizer)+"\n")
          file1.close()
   
      print(ack_ewma_normalizer) 
      print(send_ewma_normalizer)
      print(min_rtt)
      print(rtt_ratio_normalizer)
      print(cwnd_normalizer) 
      print("Eis os normalizadores acima")
      #a=input("Eis os normalizadores acima")
      #seguir = input("Deseja Prosseguir? (N/n-->Sair)")
   
      #if(seguir == 'n' or seguir =='N'):
        #exit()


      return data