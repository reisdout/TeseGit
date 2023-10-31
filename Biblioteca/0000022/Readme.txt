Para entender a necessidade das redes recorrentes, imagine o problema de se estimar
a veloicidade de um carro por meio de várias fotos desse carro ao longo de uma avinida.
As redes neurais clássicas conseguem localizar o carro em cada um dos frames, mas não
podem estabelecer uma relação entre as diversas posições do carro em cada frame.
Para fazer isso, faz-se necessário retroalimentar a rede e assim estabelecer-se uma relação
entre posições, possibilitando, assim, estimar a velocidade.
Em outras palavras, tudo que depende de uma sequencia ou dimensão temporal, 
como procesamento de texto, sinais médicos, áudios, vídeo 


I. Introdução
	.DDoS X DoS
	.Importância da detecção na defesa
	.Dificuldade na detecção, por serem similares a legítimos
	.Machine learning melhor do que estatística
	.Dificuldades no emprego de Machine Learning
		.Seleção das features
		.especialização para casos específicos
		.Necessidade de atualizção do modelo.
	.Vantagem das redes profundas sobre as rasas

II. RELATED WORK

	.Contra ataques
		.Estatístico
		.Machine Learning
	.Esquema geral de um Aprendizado Supervisionada para detectar DDoS

III. DEEP LEARNING BASED APPROACH
	.Dificuldade de se detectar ataques de baixa taxa
	.Importância do histórico do tráfego==>Recurrent Neural Network (RNN) (LSTM, GRU)
	.O desempenho é meolho quanto maior é o histórico
	.Extração das Features
	.Transformação - A impressão é que o y deveria ficare no plano (xy) e não no zy....

	
IV. EXPERIMENTS

	.Utilização de LSTM, com janela =100.
	.LSTM mais apropriada para dados históricos