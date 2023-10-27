#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 17:09:03 2023

@author: ns
"""

import MRSUtils as mrs

def RenameFile():
    mrs.RenameFile('../../Exp_0000060_Aderencia_40_Fluxos', parInicialCount=41)
    
    print ("Renomeaçao Concluida")
    
RenameFile()

