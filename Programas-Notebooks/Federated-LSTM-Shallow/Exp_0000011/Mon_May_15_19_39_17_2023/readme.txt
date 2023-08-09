Epocas: 50
Units: 100
Batch Size:1
Janela Previsao: 30
Ahead Steps:5
Terminais: 40, 20 longos (4GB), 10 Very Short (10KB) e 10 Short (100KB), entrando no terço final da simulação.
Topologia: Dumbell (1000MB,1MB de bottleneck), Terminal base 10ms; servidor 100ms;  RTT1=100ms, Salto RTT= 50ms.
Tempo de Simulação:60min.
Nos experimentos, o protocolo fixado foi o BBR. Ficou comprovado que o BBR privilegia os fluxos mais recentes 
Para evitar isso, foi necessário estreitar o gargalo para 1M. Essa solução foi pensada, pois supõe-se que, se a banda é grande, o probe do BBR acaba achando mais banda para os fluxos tardios que entram na retração dos anteriores
Mesmo assim, os tardios ficaram muito próximos. Lembrando que o Fluxo inicial fica, inicialmente, pelo menos 30s transmitindo exclusivamente.
Outro fato interessante é que parece que o BBR, na abundância de banda, acaba estabilizando as taxas, mantendo o buffer do roteado sempre aliviado, o que é ruim para as previsões, que usam como texte o final dos registros.
.
{Epoch: 0} loss: 0.023299, mean_absolute_error: 0.090664
{Epoch: 1} loss: 0.020622, mean_absolute_error: 0.084314
{Epoch: 2} loss: 0.020584, mean_absolute_error: 0.084712
{Epoch: 3} loss: 0.020363, mean_absolute_error: 0.084160
{Epoch: 4} loss: 0.020082, mean_absolute_error: 0.084384
{Epoch: 5} loss: 0.020170, mean_absolute_error: 0.083964
{Epoch: 6} loss: 0.019836, mean_absolute_error: 0.083371
{Epoch: 7} loss: 0.018698, mean_absolute_error: 0.080698
{Epoch: 8} loss: 0.017706, mean_absolute_error: 0.078802
{Epoch: 9} loss: 0.017202, mean_absolute_error: 0.077090
{Epoch: 10} loss: 0.016800, mean_absolute_error: 0.076142
{Epoch: 11} loss: 0.016336, mean_absolute_error: 0.075638
{Epoch: 12} loss: 0.015049, mean_absolute_error: 0.072377
{Epoch: 13} loss: 0.013659, mean_absolute_error: 0.069418
{Epoch: 14} loss: 0.014210, mean_absolute_error: 0.069993
{Epoch: 15} loss: 0.013832, mean_absolute_error: 0.070229
{Epoch: 16} loss: 0.014240, mean_absolute_error: 0.070622
{Epoch: 17} loss: 0.013310, mean_absolute_error: 0.069111
{Epoch: 18} loss: 0.013390, mean_absolute_error: 0.069506
{Epoch: 19} loss: 0.013292, mean_absolute_error: 0.068813
{Epoch: 20} loss: 0.013672, mean_absolute_error: 0.069042
{Epoch: 21} loss: 0.012494, mean_absolute_error: 0.066559
{Epoch: 22} loss: 0.013222, mean_absolute_error: 0.068699
{Epoch: 23} loss: 0.013198, mean_absolute_error: 0.068619
{Epoch: 24} loss: 0.012382, mean_absolute_error: 0.066766
{Epoch: 25} loss: 0.012217, mean_absolute_error: 0.066416
{Epoch: 26} loss: 0.012145, mean_absolute_error: 0.066460
{Epoch: 27} loss: 0.011980, mean_absolute_error: 0.065560
{Epoch: 28} loss: 0.012073, mean_absolute_error: 0.065167
{Epoch: 29} loss: 0.011092, mean_absolute_error: 0.063547
{Epoch: 30} loss: 0.011427, mean_absolute_error: 0.064382
{Epoch: 31} loss: 0.011123, mean_absolute_error: 0.063909
{Epoch: 32} loss: 0.010956, mean_absolute_error: 0.064028
{Epoch: 33} loss: 0.011241, mean_absolute_error: 0.063926
{Epoch: 34} loss: 0.010327, mean_absolute_error: 0.062106
{Epoch: 35} loss: 0.010442, mean_absolute_error: 0.063180
{Epoch: 36} loss: 0.010567, mean_absolute_error: 0.061631
{Epoch: 37} loss: 0.010265, mean_absolute_error: 0.061248
{Epoch: 38} loss: 0.010313, mean_absolute_error: 0.062085
{Epoch: 39} loss: 0.010050, mean_absolute_error: 0.061276
{Epoch: 40} loss: 0.009735, mean_absolute_error: 0.060491
{Epoch: 41} loss: 0.009874, mean_absolute_error: 0.060761
{Epoch: 42} loss: 0.009531, mean_absolute_error: 0.059579
{Epoch: 43} loss: 0.009678, mean_absolute_error: 0.059038
{Epoch: 44} loss: 0.009454, mean_absolute_error: 0.059775
{Epoch: 45} loss: 0.008898, mean_absolute_error: 0.058738
{Epoch: 46} loss: 0.009409, mean_absolute_error: 0.059207
{Epoch: 47} loss: 0.008948, mean_absolute_error: 0.057626
{Epoch: 48} loss: 0.008788, mean_absolute_error: 0.058428
{Epoch: 49} loss: 0.008731, mean_absolute_error: 0.057629
{Epoch: 0} loss: 0.008588, mean_absolute_error: 0.057364
{Epoch: 1} loss: 0.009987, mean_absolute_error: 0.059092
{Epoch: 2} loss: 0.009351, mean_absolute_error: 0.057467
{Epoch: 3} loss: 0.008249, mean_absolute_error: 0.056424
{Epoch: 4} loss: 0.008886, mean_absolute_error: 0.057725
{Epoch: 5} loss: 0.007826, mean_absolute_error: 0.055349
{Epoch: 6} loss: 0.007941, mean_absolute_error: 0.055523
{Epoch: 7} loss: 0.007703, mean_absolute_error: 0.054877
{Epoch: 8} loss: 0.006844, mean_absolute_error: 0.053098
{Epoch: 9} loss: 0.008745, mean_absolute_error: 0.057196
{Epoch: 10} loss: 0.007927, mean_absolute_error: 0.055753
{Epoch: 11} loss: 0.006893, mean_absolute_error: 0.053446
{Epoch: 12} loss: 0.006784, mean_absolute_error: 0.052644
{Epoch: 13} loss: 0.007078, mean_absolute_error: 0.053527
{Epoch: 14} loss: 0.006143, mean_absolute_error: 0.051595
{Epoch: 15} loss: 0.006842, mean_absolute_error: 0.052176
{Epoch: 16} loss: 0.006111, mean_absolute_error: 0.051651
{Epoch: 17} loss: 0.006290, mean_absolute_error: 0.051353
{Epoch: 18} loss: 0.005544, mean_absolute_error: 0.049832
{Epoch: 19} loss: 0.005614, mean_absolute_error: 0.049627
{Epoch: 20} loss: 0.005488, mean_absolute_error: 0.049714
{Epoch: 21} loss: 0.006840, mean_absolute_error: 0.052326
{Epoch: 22} loss: 0.005302, mean_absolute_error: 0.048899
{Epoch: 23} loss: 0.005948, mean_absolute_error: 0.049772
{Epoch: 24} loss: 0.004827, mean_absolute_error: 0.047799
{Epoch: 25} loss: 0.007037, mean_absolute_error: 0.052311
{Epoch: 26} loss: 0.004636, mean_absolute_error: 0.046769
{Epoch: 27} loss: 0.004491, mean_absolute_error: 0.046237
{Epoch: 28} loss: 0.004689, mean_absolute_error: 0.046023
{Epoch: 29} loss: 0.004417, mean_absolute_error: 0.045184
{Epoch: 30} loss: 0.004626, mean_absolute_error: 0.046489
{Epoch: 31} loss: 0.005222, mean_absolute_error: 0.047968
{Epoch: 32} loss: 0.004208, mean_absolute_error: 0.044824
{Epoch: 33} loss: 0.004209, mean_absolute_error: 0.045606
{Epoch: 34} loss: 0.003926, mean_absolute_error: 0.044197
{Epoch: 35} loss: 0.004894, mean_absolute_error: 0.046289
{Epoch: 36} loss: 0.003729, mean_absolute_error: 0.043410
{Epoch: 37} loss: 0.003746, mean_absolute_error: 0.043330
{Epoch: 38} loss: 0.003562, mean_absolute_error: 0.043129
{Epoch: 39} loss: 0.004328, mean_absolute_error: 0.044622
{Epoch: 40} loss: 0.003844, mean_absolute_error: 0.042247
{Epoch: 41} loss: 0.003983, mean_absolute_error: 0.042775
{Epoch: 42} loss: 0.004083, mean_absolute_error: 0.043716
{Epoch: 43} loss: 0.003240, mean_absolute_error: 0.040566
{Epoch: 44} loss: 0.004071, mean_absolute_error: 0.043097
{Epoch: 45} loss: 0.003775, mean_absolute_error: 0.042114
{Epoch: 46} loss: 0.003516, mean_absolute_error: 0.041239
{Epoch: 47} loss: 0.002907, mean_absolute_error: 0.039600
{Epoch: 48} loss: 0.003188, mean_absolute_error: 0.041115
{Epoch: 49} loss: 0.003466, mean_absolute_error: 0.040979
Teste de Aderencia: 
40, 20 longos (4GB), 10 Very Short (10KB) e 10 Short (100KB), entrando no terço final da simulação
Topologia: Parking Lot (1000MB entre os terminias e os roteadores , 1MB de bottleneck), RTT Terminal base 0,5ms; RTT servidor 10ms; RTT1=5ms; salto RTT= 5ms.
Tempo de Simulação:60min.
Este experimento visa medir a aderência do modelo gerado na dumbell do experimento anterior na parkinglot aqui descrita
Sendo assim, o test_client01 foi originado com dados levantados da parkinglot, que serão previstos pelos pesos treinados com os dados da dumbell anterior.
Na topologia considerada, ajustou-se os RTT entre os roteadores de 5ms, de forma que desse os 100ms das dumbell consideradas nos experimentos anteriores. Colocando 100ms para cada roteador ficou muito lenta a troca de pacortes e, consequentemnete, a geração dos arquivos .
Também foi retirada a calda de zeros no final do test_client01.
Teste de Aderencia: 
40, 20 longos (4GB), 10 Very Short (10KB) e 10 Short (100KB), entrando no terço final da simulação
Topologia: Parking Lot (1000MB entre os terminias e os roteadores , 1MB de bottleneck), RTT Terminal base 0,5ms; RTT servidor 10ms; RTT1=5ms; salto RTT= 5ms.
Tempo de Simulação:60min.
Este experimento visa medir a aderência do modelo gerado na dumbell do experimento anterior na parkinglot aqui descrita
Sendo assim, o test_client01 foi originado com dados levantados da parkinglot, que serão previstos pelos pesos treinados com os dados da dumbell anterior.
Na topologia considerada, ajustou-se os RTT entre os roteadores de 5ms, de forma que desse os 100ms das dumbell consideradas nos experimentos anteriores. Colocando 100ms para cada roteador ficou muito lenta a troca de pacortes e, consequentemnete, a geração dos arquivos .
Também foi retirada a calda de zeros no final do test_client01.
Teste de Aderencia: 
40, 20 longos (4GB), 10 Very Short (10KB) e 10 Short (100KB), entrando no terço final da simulação
Topologia: Parking Lot (1000MB entre os terminias e os roteadores , 1MB de bottleneck), RTT Terminal base 0,5ms; RTT servidor 10ms; RTT1=5ms; salto RTT= 5ms.
Tempo de Simulação:60min.
Este experimento visa medir a aderência do modelo gerado na dumbell do experimento anterior na parkinglot aqui descrita
Sendo assim, o test_client01 foi originado com dados levantados da parkinglot, que serão previstos pelos pesos treinados com os dados da dumbell anterior.
Na topologia considerada, ajustou-se os RTT entre os roteadores de 5ms, de forma que desse os 100ms das dumbell consideradas nos experimentos anteriores. Colocando 100ms para cada roteador ficou muito lenta a troca de pacortes e, consequentemnete, a geração dos arquivos .
Também foi retirada a calda de zeros no final do test_client01.
Teste de Aderencia: 
40, 20 longos (4GB), 10 Very Short (10KB) e 10 Short (100KB), entrando no terço final da simulação
Topologia: Parking Lot (1000MB entre os terminias e os roteadores , 1MB de bottleneck), RTT Terminal base 0,5ms; RTT servidor 10ms; RTT1=5ms; salto RTT= 5ms.
Tempo de Simulação:60min.
Este experimento visa medir a aderência do modelo gerado na dumbell do experimento anterior na parkinglot aqui descrita
Sendo assim, o test_client01 foi originado com dados levantados da parkinglot, que serão previstos pelos pesos treinados com os dados da dumbell anterior.
Na topologia considerada, ajustou-se os RTT entre os roteadores de 5ms, de forma que desse os 100ms das dumbell consideradas nos experimentos anteriores. Colocando 100ms para cada roteador ficou muito lenta a troca de pacortes e, consequentemnete, a geração dos arquivos .
Também foi retirada a calda de zeros no final do test_client01.
Teste de Aderencia: 
40, 20 longos (4GB), 10 Very Short (10KB) e 10 Short (100KB), entrando no terço final da simulação
Topologia: Parking Lot (1000MB entre os terminias e os roteadores , 1MB de bottleneck), RTT Terminal base 0,5ms; RTT servidor 10ms; RTT1=5ms; salto RTT= 5ms.
Tempo de Simulação:60min.
Este experimento visa medir a aderência do modelo gerado na dumbell do experimento anterior na parkinglot aqui descrita
Sendo assim, o test_client01 foi originado com dados levantados da parkinglot, que serão previstos pelos pesos treinados com os dados da dumbell anterior.
Na topologia considerada, ajustou-se os RTT entre os roteadores de 5ms, de forma que desse os 100ms das dumbell consideradas nos experimentos anteriores. Colocando 100ms para cada roteador ficou muito lenta a troca de pacortes e, consequentemnete, a geração dos arquivos .
Também foi retirada a calda de zeros no final do test_client01.
Teste de Aderencia: 
40, 20 longos (4GB), 10 Very Short (10KB) e 10 Short (100KB), entrando no terço final da simulação
Topologia: Parking Lot (1000MB entre os terminias e os roteadores , 1MB de bottleneck), RTT Terminal base 10ms; RTT servidor 100ms; RTT1=50ms; salto RTT= 50ms.
Tempo de Simulação:60min.
Este experimento visa medir a aderência do modelo gerado na dumbell do experimento anterior na parkinglot aqui descrita
Sendo assim, o test_client01 foi originado com dados levantados da parkinglot, que serão previstos pelos pesos treinados com os dados da dumbell anterior.
Na topologia considerada, ajustou-se os RTT entre os roteadores de 5ms, de forma que desse os 100ms das dumbell consideradas nos experimentos anteriores. Colocando 100ms para cada roteador ficou muito lenta a troca de pacortes e, consequentemnete, a geração dos arquivos .
Também foi retirada a calda de zeros no final do test_client01.
Teste de Aderencia: 
40, 20 longos (4GB), 10 Very Short (10KB) e 10 Short (100KB), entrando no terço final da simulação
Topologia: Parking Lot (1000MB entre os terminias e os roteadores , 1MB de bottleneck), RTT Terminal base 0,5ms; RTT servidor 10ms; RTT1=5ms; salto RTT= 5ms.
Tempo de Simulação:60min.
Este experimento visa medir a aderência do modelo gerado na dumbell do experimento anterior na parkinglot aqui descrita
Sendo assim, o test_client01 foi originado com dados levantados da parkinglot, que serão previstos pelos pesos treinados com os dados da dumbell anterior.
Na topologia considerada, ajustou-se os RTT entre os roteadores de 0,005ms, pois com roteadores, o processamento da fila faz com que demore mais.
Teste de Aderencia: 
testar com outros dados, mas gerados com uma topologia dumbell, igual a do treinamento.
Teste de Aderencia: 
testar com outros dados, mas gerados com uma topologia dumbell, igual a do treinamento.
