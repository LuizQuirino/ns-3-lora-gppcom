from collections import defaultdict
import os
import math
import random
import re
import subprocess
import sys
import argparse
from glob import glob
import numpy as np
import matplotlib.pylab as plt
from itertools import cycle
# To install YAML: sudo apt-get install python3-yaml
import yaml

class Simulation:
    def __init__(self, configurations_file):
        self.email_to = 'martinsdecastro23@gmail.com'            
        with open(configurations_file, 'r') as f:
            self.doc = yaml.load(f, Loader=yaml.loader.BaseLoader)
        self.campaign_name = os.path.splitext(configurations_file)[0]
        
        # Read commom parameters
        self.campaign = self.doc['scenario']['campaign']
        self.simLocation = str(doc['scenario']['simLocation'])
        self.simulationTime = self.doc['scenario']['simulationTime']
        self.nDevices = self.doc['scenario']['nDevices'][0]
        self.radius = self.doc['scenario']['radius'][0]
        self.appPeriodSeconds = self.doc['scenario']['appPeriodSeconds']
        self.bPrint = (self.doc['scenario']['bPrint'])
        self.fixedSeed = (self.doc['scenario']['fixedSeed'])
        self.algoritmo = self.doc['scenario']['Algoritmo']
        self.ns3_path = str(self.doc['scenario']['ns3_path'])
        self.ns3_path = os.getcwd() + '/' + self.ns3_path
        self.ns3_script = str(self.doc['scenario']['ns3_script'])
        self.nJobs = int(self.doc['scenario']['jobs'])
        self.filename = str(self.doc['scenario']['filename'])
       
    def runCampaign(self,curCampaign):
        # Configure simulation file in accordance with campaign parameter
        sh_name = self.campaign_name + '_' + self.simLocation + '_' + curCampaign
        print(curCampaign+" campaign written in file: " 'run_%s.sh' % sh_name)
        with open('run_all_%s.sh' % sh_name, 'w') as f:                    
            if self.simLocation == 'cluster':
              print('To be implemented')
            else:
              f.write('#!/bin/bash\n')
              f.write("cd '"+self.ns3_path+"'"+"\n")
              outputDir = self.ns3_path+'/results_'+self.simLocation + '_' + curCampaign
              #f.write('rm -rf '+outputDir+' 2>/dev/null\n')
              f.write('mkdir -p '+outputDir+'\n')
            for iJob in range(0, self.nJobs):
                jobRunSeed = random.randint(1, 23*10**14)
                for iAlg in self.algoritmo:                           
                    for varParam in self.doc['scenario'][curCampaign]:
                      if str(curCampaign) == 'radius':
                          command = (
                          'NS_GLOBAL_VALUE="RngRun='+str(jobRunSeed)+ '" ' +
                          "./waf --run '"+self.ns3_script+
                          " --radius="+varParam+
                          " --nDevices="+self.nDevices+
                          " --simulationTime="+self.simulationTime+
                          " --appPeriodSeconds="+self.appPeriodSeconds+
                          " --print="+self.bPrint+
                          " --fixedSeed="+str(self.fixedSeed)+
                          " --algoritmo="+iAlg+
                          " --filename="+ self.filename +
                          " --outputDir='"+outputDir+"'"
                          "'"
                          )
                      elif str(curCampaign) == 'nDevices':
                          command = (
                          'NS_GLOBAL_VALUE="RngRun='+str(jobRunSeed)+ '" ' +
                          "./waf --run '"+self.ns3_script+ 
                          " --radius="+self.radius+
                          " --nDevices="+varParam+
                          " --simulationTime="+self.simulationTime+
                          " --appPeriodSeconds="+self.appPeriodSeconds+
                          " --print="+self.bPrint+
                          " --fixedSeed="+str(self.fixedSeed)+
                          " --algoritmo="+iAlg+
                          " --filename="+ self.filename +
                          " --outputDir='"+outputDir+"'"
                          "'"
                          )
                      f.write(command+' & wait\n')
                      
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, help='Configuration File')
args = parser.parse_args()

configurations_file = args.file; 
with open(configurations_file, 'r') as f:
    doc = yaml.load(f, Loader=yaml.loader.BaseLoader)
    campaign_name = os.path.splitext(configurations_file)[0]

print('Simulação escolhida: ')
campaign = doc['scenario']['campaign']
print(campaign)
                 
simu = Simulation(configurations_file)

for simC in campaign:
    if str(simC) == 'nDevices' or str(simC) == 'radius':
        simu.runCampaign(simC);
    else:
        print('Invalid simulation campaign: verify the campaign parameter!')