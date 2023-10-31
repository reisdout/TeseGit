Epocas: 50
Units: 100
Batch Size:1
Janela Previsao: 30
Ahead Steps:5
Terminais: 20, 10 longos (4GB), 05 Very Short (10KB) e 05 Short (100KB).
Topologia: Dumbell (1000MB,1MB de bottleneck), RTT1=50ms, Salto RTT= 50ms.
Tempo de Simulação:30min.
Durante a geração de dados, observou-se que a partir de um determinado período 
o buffer do roteador estabilizava. A explicação é que o BBR ajustava os fluxos de
forma a evtar o congestionamento. O que foi feito então foi colocar os não-longos
para o terço final da simulação (t_start = 5.0+2*expSimulationTime/3+i+ (float)((rand()%10)/10))
isso foi suficiente para manter o buffer do roteador vriando até o final do experimento.
{Epoch: 0} loss: 0.061288, mean_absolute_error: 0.193178
{Epoch: 1} loss: 0.056634, mean_absolute_error: 0.184059
{Epoch: 2} loss: 0.055790, mean_absolute_error: 0.182802
{Epoch: 3} loss: 0.054420, mean_absolute_error: 0.180545
{Epoch: 4} loss: 0.053362, mean_absolute_error: 0.178579
{Epoch: 5} loss: 0.051938, mean_absolute_error: 0.175744
{Epoch: 6} loss: 0.050508, mean_absolute_error: 0.172859
{Epoch: 7} loss: 0.049305, mean_absolute_error: 0.170359
{Epoch: 8} loss: 0.048770, mean_absolute_error: 0.168766
{Epoch: 9} loss: 0.047488, mean_absolute_error: 0.166744
{Epoch: 10} loss: 0.046272, mean_absolute_error: 0.164196
{Epoch: 11} loss: 0.045361, mean_absolute_error: 0.162612
{Epoch: 12} loss: 0.044070, mean_absolute_error: 0.159392
{Epoch: 13} loss: 0.044062, mean_absolute_error: 0.159668
{Epoch: 14} loss: 0.042931, mean_absolute_error: 0.156555
{Epoch: 15} loss: 0.041720, mean_absolute_error: 0.154738
{Epoch: 16} loss: 0.040030, mean_absolute_error: 0.150474
{Epoch: 17} loss: 0.039455, mean_absolute_error: 0.149454
{Epoch: 18} loss: 0.038194, mean_absolute_error: 0.145767
{Epoch: 19} loss: 0.036824, mean_absolute_error: 0.143451
{Epoch: 20} loss: 0.035766, mean_absolute_error: 0.140051
{Epoch: 21} loss: 0.034705, mean_absolute_error: 0.138997
{Epoch: 22} loss: 0.033199, mean_absolute_error: 0.134781
{Epoch: 23} loss: 0.031953, mean_absolute_error: 0.131804
{Epoch: 24} loss: 0.030144, mean_absolute_error: 0.127229
{Epoch: 25} loss: 0.029498, mean_absolute_error: 0.125788
{Epoch: 26} loss: 0.028183, mean_absolute_error: 0.123041
{Epoch: 27} loss: 0.026050, mean_absolute_error: 0.117568
{Epoch: 28} loss: 0.025662, mean_absolute_error: 0.115999
{Epoch: 29} loss: 0.023755, mean_absolute_error: 0.112081
{Epoch: 30} loss: 0.022618, mean_absolute_error: 0.109161
{Epoch: 31} loss: 0.022220, mean_absolute_error: 0.108021
{Epoch: 32} loss: 0.019652, mean_absolute_error: 0.102496
{Epoch: 33} loss: 0.020830, mean_absolute_error: 0.103761
{Epoch: 34} loss: 0.018245, mean_absolute_error: 0.097715
{Epoch: 35} loss: 0.018186, mean_absolute_error: 0.097393
{Epoch: 36} loss: 0.017481, mean_absolute_error: 0.094474
{Epoch: 37} loss: 0.016906, mean_absolute_error: 0.093224
{Epoch: 38} loss: 0.015606, mean_absolute_error: 0.090582
{Epoch: 39} loss: 0.015292, mean_absolute_error: 0.089568
{Epoch: 40} loss: 0.014059, mean_absolute_error: 0.086044
{Epoch: 41} loss: 0.013557, mean_absolute_error: 0.084283
{Epoch: 42} loss: 0.013312, mean_absolute_error: 0.083389
{Epoch: 43} loss: 0.013193, mean_absolute_error: 0.081816
{Epoch: 44} loss: 0.012365, mean_absolute_error: 0.079576
{Epoch: 45} loss: 0.012089, mean_absolute_error: 0.078308
{Epoch: 46} loss: 0.011517, mean_absolute_error: 0.077377
{Epoch: 47} loss: 0.011093, mean_absolute_error: 0.075640
{Epoch: 48} loss: 0.010401, mean_absolute_error: 0.074174
{Epoch: 49} loss: 0.010349, mean_absolute_error: 0.073196
{Epoch: 0} loss: 0.010736, mean_absolute_error: 0.073317
{Epoch: 1} loss: 0.009593, mean_absolute_error: 0.070541
{Epoch: 2} loss: 0.010336, mean_absolute_error: 0.072346
{Epoch: 3} loss: 0.008855, mean_absolute_error: 0.067395
{Epoch: 4} loss: 0.009121, mean_absolute_error: 0.068512
{Epoch: 5} loss: 0.008875, mean_absolute_error: 0.067042
{Epoch: 6} loss: 0.008541, mean_absolute_error: 0.066254
{Epoch: 7} loss: 0.008164, mean_absolute_error: 0.064287
{Epoch: 8} loss: 0.008264, mean_absolute_error: 0.064638
{Epoch: 9} loss: 0.007762, mean_absolute_error: 0.063625
{Epoch: 10} loss: 0.008213, mean_absolute_error: 0.064038
{Epoch: 11} loss: 0.007862, mean_absolute_error: 0.062816
{Epoch: 12} loss: 0.007315, mean_absolute_error: 0.059770
{Epoch: 13} loss: 0.007135, mean_absolute_error: 0.061078
{Epoch: 14} loss: 0.006859, mean_absolute_error: 0.059434
{Epoch: 15} loss: 0.007421, mean_absolute_error: 0.060778
{Epoch: 16} loss: 0.006435, mean_absolute_error: 0.057360
{Epoch: 17} loss: 0.007179, mean_absolute_error: 0.059176
{Epoch: 18} loss: 0.006463, mean_absolute_error: 0.057438
{Epoch: 19} loss: 0.006746, mean_absolute_error: 0.058184
{Epoch: 20} loss: 0.006032, mean_absolute_error: 0.056274
{Epoch: 21} loss: 0.006312, mean_absolute_error: 0.056631
{Epoch: 22} loss: 0.006224, mean_absolute_error: 0.055466
{Epoch: 23} loss: 0.006227, mean_absolute_error: 0.055524
{Epoch: 24} loss: 0.005785, mean_absolute_error: 0.054318
{Epoch: 25} loss: 0.006188, mean_absolute_error: 0.056264
{Epoch: 26} loss: 0.005860, mean_absolute_error: 0.053874
{Epoch: 27} loss: 0.005737, mean_absolute_error: 0.053135
{Epoch: 28} loss: 0.005436, mean_absolute_error: 0.052252
{Epoch: 29} loss: 0.005734, mean_absolute_error: 0.053054
{Epoch: 30} loss: 0.005521, mean_absolute_error: 0.052415
{Epoch: 31} loss: 0.005687, mean_absolute_error: 0.052535
{Epoch: 32} loss: 0.005415, mean_absolute_error: 0.051717
{Epoch: 33} loss: 0.005853, mean_absolute_error: 0.052439
{Epoch: 34} loss: 0.005509, mean_absolute_error: 0.051773
{Epoch: 35} loss: 0.005407, mean_absolute_error: 0.050708
{Epoch: 36} loss: 0.005295, mean_absolute_error: 0.051099
{Epoch: 37} loss: 0.005277, mean_absolute_error: 0.051292
{Epoch: 38} loss: 0.005446, mean_absolute_error: 0.051239
{Epoch: 39} loss: 0.004787, mean_absolute_error: 0.048945
{Epoch: 40} loss: 0.005184, mean_absolute_error: 0.049795
{Epoch: 41} loss: 0.004961, mean_absolute_error: 0.049067
{Epoch: 42} loss: 0.004875, mean_absolute_error: 0.047847
{Epoch: 43} loss: 0.004890, mean_absolute_error: 0.048646
{Epoch: 44} loss: 0.004904, mean_absolute_error: 0.048105
{Epoch: 45} loss: 0.004821, mean_absolute_error: 0.047452
{Epoch: 46} loss: 0.004730, mean_absolute_error: 0.047814
{Epoch: 47} loss: 0.004280, mean_absolute_error: 0.045876
{Epoch: 48} loss: 0.004405, mean_absolute_error: 0.046737
{Epoch: 49} loss: 0.004569, mean_absolute_error: 0.047370
