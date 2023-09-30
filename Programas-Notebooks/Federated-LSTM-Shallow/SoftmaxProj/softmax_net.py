
from GeneralAckSoftmax_Client import Client  
from FromRouterSoftmax_Client import ClientBufferArrival





       
    



def TreinarModelo(parExpDirPath, parBasePath):
    
    client01 = Client(0,parExpDirPath,parBasePath)    


    
    client01.RefreshModel(True)
    client01.GetMapedMatrix()
    

   


    #previsores_treinamento = pd.read_csv('./SQ-false-positive-filering-ML/input/x_train.csv')
    #classe_treinamento = pd.read_csv('./SQ-false-positive-filering-ML/input/y_train.csv')

    client01.SaveModel()

    '''
    classificador_json = classificador.to_json()
    with open(parExpDirPath+"/model.json",'w') as json_file:
        json_file.write(classificador_json)
    classificador.save_weights(parExpDirPath+"/model_weights.h5")
    from keras2cpp import export_model
    export_model(classificador, parExpDirPath+"/example.model")
    '''

#TreinarModelo('./Exp_0000034','./Exp_0000034/1Mono-4NewReno-noventacincocentesimos-seisdecimos-40-70-3h30min.csv')

#TreinarModelo('./Exp_0000037','./Exp_0000037/05fl-10h-95_60-compatibilizado.csv')




def TreinarModeloBufferArrival(parExpDirPath, parBasePath,parBaseArrival):
    
    client01 = ClientBufferArrival(0,parExpDirPath,parBasePath,parBaseArrival)    
    client01.RefreshModel(True)
    client01.GetMapedMatrix()
    

   


    #previsores_treinamento = pd.read_csv('./SQ-false-positive-filering-ML/input/x_train.csv')
    #classe_treinamento = pd.read_csv('./SQ-false-positive-filering-ML/input/y_train.csv')

    client01.SaveModel()

    '''
    classificador_json = classificador.to_json()
    with open(parExpDirPath+"/model.json",'w') as json_file:
        json_file.write(classificador_json)
    classificador.save_weights(parExpDirPath+"/model_weights.h5")
    from keras2cpp import export_model
    export_model(classificador, parExpDirPath+"/example.model")
    
    '''

def EvalueteModelLevarage(parExpDirPath,
                          parBasePath):
    
    client01 = Client(0,parExpDirPath,parBasePath)
    client01.AderenciaOutrosFluxos()


#TreinarModelo('./Exp_0000034','./Exp_0000034/1Mono-4NewReno-noventacincocentesimos-seisdecimos-40-70-3h30min.csv')

#TreinarModelo('./Exp_0000037','./Exp_0000037/05fl-10h-95_60-compatibilizado.csv')

TreinarModeloBufferArrival('../Exp_0000038','../Exp_0000038/terminal00.csv', '../Exp_0000038/router00.csv')



