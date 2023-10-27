#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 17:09:03 2023

@author: ns
"""

import MRSUtils as mrs

def RenameFile():
    mrs.RenameFile('../../Exp_0000057_Aderencia_10_Fluxos', parInicialCount=11)
    print ("Renomeaçao Concluida")
    
RenameFile()

