# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 15:34:06 2024

@author: mayank
"""

import sys
def TorsionAngleCalculation(InputPath,OutPutDir,MapType,PlotResolutions,PlotFileType):
    PlotResolutions=int(PlotResolutions)
    # PlotResolutions=600
    # PlotFileType='png'
   
    print(MapType);
    import csv
    import pkg_resources
    import Bio.PDB
    import pandas as pd
    import os
    os.environ['MPLCONFIGDIR'] = os.getcwd() + "/configs/"
    import matplotlib.pyplot as plt 
    import numpy as np
    isExist = os.path.exists(OutPutDir)
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(OutPutDir)
    isExist = os.path.exists(OutPutDir+'/Plots')
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(OutPutDir+'/Plots')
      
       # print("The new directory is created!")
    # pd.options.future.infer_string = True
    def ramachandran_type_Gly_Non_Gly(residue) :
        if residue.upper()=="GLY" :
            return "Gly"
        else:
            return "General"
    def ramachandran_type(residue, next_residue,Omega) :
        """Expects Bio.PDB residues, returns ramachandran 'type'
    
        If this is the last residue in a polypeptide, use None
        for next_residue.
    
        Return value is a string: "General", "Glycine", "Proline"
        or "Pre-Pro".
        """
        if residue.upper()=="GLY" :
            return "Gly"
        elif residue.upper()=="PRO" :
            if Omega:
                if( -20 <= Omega <= 20  ):
                    return "cisPro"
                else:
                    return'transPro'  
            else:
                return'transPro' 
        elif next_residue is not None \
        and next_residue.upper()=="PRO" :
            #exlcudes those that are Pro or Gly
            return "prePro"
        elif residue.upper()=="VAL" :
            return "Val_Ile"
        elif residue.upper()=="ILE" :
            return "Val_Ile"
    #    elif residue.resname.upper()=="THR" :
    #        return "Threonine"
        else :
            return "General" 
    
    df = pd.DataFrame(columns=['ID','PDBID','Chain','Residue','ResNum', 'PHI', 'PSI', 'Omega','tau','BFactor','chi1','chi2','chi3','chi4','chi5','Group','Isomer','Disorder','GroupGly'])
    log=open(OutPutDir+'/log.dat', 'w')
    log.write('InSIde TorsionAngleCalculation \n '+ MapType)
    with open(OutPutDir+'/PhiPsiTauCaiOmegaBFactorCalculation.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'PDBID','Chain','Residue','ResNum','PHI', 'PSI', 'Omega','tau','BFactor','chi1','chi2','chi3','chi4','chi5','Group','Isomer','Disorder','GroupGly'])
        files = os.listdir(InputPath)
        for pdb_code in files:      
            log.write(pdb_code+"\n")
            print(pdb_code)
            PDBID=pdb_code.split(".")[0]
            #PDBID='ABC'
            pdb_code_path = InputPath+'/'+pdb_code
            print("About to load Bio.PDB and the PDB file...")
            try:
                structure = Bio.PDB.PDBParser().get_structure(pdb_code_path, "%s" % pdb_code_path)        
                structure.atom_to_internal_coordinates()
                for chain in structure[0] :
                        ChainId=chain.id
                        log.write("Calculate Torsion angles for Chain ID :"+ChainId+"\n")
                        print(ChainId)
                        try:
                            Res=structure[0][ChainId].get_residues()
                            for r in Res:
                                if r:
                                    try:
                                        ric = r.internal_coord
                                        if ric:
                                            try:
                                                PHI=ric.get_angle("phi")
                                                PSI=ric.get_angle("psi")
                                                Omega=ric.get_angle("omg")
                                                BFactor=r['CA'].get_bfactor()
                                                tau=ric.get_angle("tau")
                                                chi1=ric.get_angle("chi1")
                                                chi2=ric.get_angle("chi2")
                                                chi3=ric.get_angle("chi3")
                                                chi4=ric.get_angle("chi4")
                                                chi5=ric.get_angle("chi5")
                                                residue=r.get_resname()
                                                if r.is_disordered():
                                                    Disorder='Yes'
                                                else:
                                                    Disorder='No'
                                                
                                                ResNum=r.get_id()[1]
                                                nextresidue=''
                                                try:  
                                                        nextresidue=structure[0][ChainId][ResNum+1].get_resname()
                                                except:
                                                        pass
                                                # print(nextresidue)
                                                GroupGlyType=ramachandran_type_Gly_Non_Gly(residue)
                                                Group = ramachandran_type(residue, nextresidue,Omega)
                                                # print(Group)
                                                Isomer=''
                                                if Omega:
                                                    if(-20<= Omega <= 20):
                                                        Isomer='Cis'
                                                        # print(Isomer)
                                                    else:
                                                        Isomer='Trans'
                                                ID=str(r.full_id[0])+" Chain: "+str(r.full_id[2])+" ResNum:"+str(r.get_id()[1])+" ResName:"+r.get_resname()
                                                # print(ID)
                                                if ID and PHI and PSI and Omega: #,Isomer
                                                    rows = [ID, PDBID , r.full_id[2],residue,r.get_id()[1],PHI, PSI, Omega,tau,BFactor,chi1,chi2,chi3,chi4,chi5,Group,Isomer,Disorder,GroupGlyType]
                                                    df.loc[len(df)] = rows
                                                    writer.writerow(rows)
                                                else:
                                                    log.write('Error : Unable to calculate  torsion angles '+pdb_code+' Chain'+ChainId+ ' Residue ' + str(r.get_id()[1])+' '+r.get_resname()+' PHI:'+str(PHI)+' PSI:'+str(PSI)+' Omega:'+str(Omega)+"\n")
                                                    #print('Error : Unable to calculate  torsion angles '+pdb_code+' Chain'+ChainId+ ' Residue ' + str(r.get_id()[1])+' '+r.get_resname()+' PHI:'+str(PHI)+' PSI:'+str(PSI)+' Omega:'+str(Omega))
                                            except:
                                                log.write('Error : Unable to calculate  torsion angles '+pdb_code+' Chain'+ChainId+ ' Residue ' + str(r.get_id()[1])+' '+r.get_resname()+"\n")
                                                #print('Error : Unable to calculate  torsion angles '+pdb_code+' Chain'+ChainId+ ' Residue ' + str(r.get_id()[1])+' '+r.get_resname())
                                                continue 
                                    except:
                                        log.write('Error :Unable to get internal cord '+pdb_code+' Chain'+ChainId)
                                        #print('Error :Unable to get internal cord '+pdb_code+' Chain'+ChainId)
                                        continue                        
                        except:
                            log.write('Error :Unable to Calculate Torsion Angle '+pdb_code+' Chain'+ChainId+"\n")
                            #print('Error :Unable to Calculate Torsion Angle '+pdb_code+' Chain'+ChainId)
                            continue
            except:
                log.write('Error :Unable to load PDB Files'+pdb_code+"\n")
                #print('Error :Unable to load PDB Files'+pdb_code)
                continue
        
            log.write('Torsion Angles calculation complited for '+pdb_code+"\n")
    # print(df)
    gd = df.groupby('Group')
    # extract keys from groups
    keys = gd.groups.keys()
    file=open(OutPutDir+'/MolProbityPhiPsiTauCaiOmegaBFactorAll.csv', 'w', newline='')
    writer = csv.writer(file)
    # writer.writerow(['AID','PHI', 'PSI','Group','Disorder','BFactor','PotentialEnergy','Region'])
    writer.writerow(['ID', 'PDBID' ,'Chain', 'Residue','ResNum','PHI', 'PSI', 'Omega','tau','BFactor','chi1','chi2','chi3','chi4','chi5','Group','Isomer','Disorder','MolprovityRegion','GroupGly'])
    MolProbitydf = pd.DataFrame(columns=['ID','PDBID' ,'Chain','Residue','ResNum', 'PHI', 'PSI', 'Omega','tau','BFactor','chi1','chi2','chi3','chi4','chi5','Group','Isomer','Disorder','MolprovityRegion','GroupGly'])
    for Groups in keys:
        dataframe=gd.get_group(Groups).reset_index()
        AID=dataframe["ID"]
        PDBIDs=dataframe["PDBID"]
        Chain=dataframe["Chain"]
        ResNum=dataframe["ResNum"]
        A1PHI=dataframe["PHI"]
        A1PSI=dataframe["PSI"]
        Group=dataframe["Group"]
        Disorder=dataframe["Disorder"]
        BFactor=dataframe["BFactor"]
        Omega=dataframe['Omega']
        tau=dataframe['tau']
        chi1=dataframe['chi1']
        chi2=dataframe['chi2']
        chi3=dataframe['chi3']
        chi4=dataframe['chi4']
        chi5=dataframe['chi5']
        Residue=dataframe['Residue'] 
        Isomer=dataframe['Isomer']
        GroupGly=dataframe['GroupGly']
        ln=len(A1PHI)
        MolprovityDataPath=pkg_resources.resource_filename('ramplot', "RamBoundry/MolprovityAllRegion"+Groups+".csv")
        MolprovityData = pd.read_csv(MolprovityDataPath)
        MolprovityPHI=MolprovityData['MolprovityPHI']
        MolprovityPSI=MolprovityData['MolprovityPSI'] 
        # MolprovityPHIGeneral=MolprovityDataGeneral['MolprovityPHI']
        # MolprovityPSIGeneral=MolprovityDataGeneral['MolprovityPSI']
        for x in range(ln):
                InputPHI=int(A1PHI[x])
                InputPSI=int(A1PSI[x])
                InputID=AID[x]
                IndexListofPHI = MolprovityData.index[MolprovityData['MolprovityPHI'] == InputPHI].tolist()
                for i in IndexListofPHI:
                    if MolprovityData['MolprovityPSI'][i]==InputPSI:
                        # print(MolprovityData['MolprovityPSI'][i])
                        MolprovityRegion=MolprovityData['MolprovityRegion'][i]
                        # PotentialEnergy=MolprovityData['PotentialEnergy'][i]
                        # PotentialEnergy=''
                        rows=[InputID,PDBIDs[x],Chain[x],Residue[x],ResNum[x],A1PHI[x], A1PSI[x],Omega[x],tau[x],BFactor[x],chi1[x],chi2[x],chi3[x],chi4[x],chi5[x],Group[x],Isomer[x],Disorder[x],MolprovityRegion,GroupGly[x]]
                        writer.writerow(rows)
                        MolProbitydf.loc[len(MolProbitydf)] = rows
                        break
                
                    
    file.close()
    file=open(OutPutDir+'/MolProbityPhiPsiTauCaiOmegaBFactorGeneralGly.csv', 'w', newline='')
    writer = csv.writer(file)
    # writer.writerow(['AID','PHI', 'PSI','Group','Disorder','BFactor','PotentialEnergy','Region'])
    writer.writerow(['AID','PDBID', 'Chain','Residue','ResNum','PHI', 'PSI', 'Omega','tau','BFactor','chi1','chi2','chi3','chi4','chi5','Group','Isomer','Disorder','MolprovityRegion','GroupGly','MolprovityRegionG'])
    MolProbitydfGeneralGly = pd.DataFrame(columns=['AID','PDBID','Chain','Residue','ResNum', 'PHI', 'PSI', 'Omega','tau','BFactor','chi1','chi2','chi3','chi4','chi5','Disorder','Group','Isomer','MolprovityRegion','GroupGly','MolprovityRegionG'])
    AID=MolProbitydf["ID"]
    PDBIDs=MolProbitydf["PDBID"]
    Chain=MolProbitydf["Chain"]
    ResNum=MolProbitydf["ResNum"]
    A1PHI=MolProbitydf["PHI"]
    A1PSI=MolProbitydf["PSI"]
    Group=MolProbitydf["Group"]
    Disorder=MolProbitydf["Disorder"]
    BFactor=MolProbitydf["BFactor"]
    Omega=MolProbitydf['Omega']
    tau=MolProbitydf['tau']
    chi1=MolProbitydf['chi1']
    chi2=MolProbitydf['chi2']
    chi3=MolProbitydf['chi3']
    chi4=MolProbitydf['chi4']
    chi5=MolProbitydf['chi5']
    Residue=MolProbitydf['Residue'] 
    Isomer=MolProbitydf['Isomer']
    GroupGly=MolProbitydf['GroupGly']
    MolprovityRegion=MolProbitydf['MolprovityRegion']
    ln=len(A1PHI)
    MolprovityDataPath=pkg_resources.resource_filename('ramplot', "RamBoundry/MolprovityAllRegionGeneral.csv")
    MolprovityData = pd.read_csv(MolprovityDataPath)
    MolprovityPHI=MolprovityData['MolprovityPHI']
    MolprovityPSI=MolprovityData['MolprovityPSI']
    for x in range(ln):
            InputPHI=int(A1PHI[x])
            InputPSI=int(A1PSI[x])
            InputID=AID[x]
            IndexListofPHI = MolprovityData.index[MolprovityData['MolprovityPHI'] == InputPHI].tolist()
            for i in IndexListofPHI:
                if MolprovityData['MolprovityPSI'][i]==InputPSI:
                    # print(MolprovityData['MolprovityPSI'][i])
                    MolprovityRegionG=MolprovityData['MolprovityRegion'][i]
                    # PotentialEnergy=MolprovityData['PotentialEnergy'][i]
                    # PotentialEnergy=''
                    rows=[InputID,PDBIDs[x],Chain[x],Residue[x],ResNum[x],A1PHI[x], A1PSI[x],Omega[x],tau[x],BFactor[x],chi1[x],chi2[x],chi3[x],chi4[x],chi5[x],Disorder[x],Group[x],Isomer[x],MolprovityRegion[x],GroupGly[x],MolprovityRegionG]
                    writer.writerow(rows)
                    MolProbitydfGeneralGly.loc[len(MolProbitydfGeneralGly)] = rows
                    break
    
    file.close()
    # Analysis
    TotalResidueCount=len(MolProbitydfGeneralGly.index)
    if TotalResidueCount >0:
        fileAnalysis=open(OutPutDir+'/Analysis.csv', 'w', newline='')
        Analysiswriter = csv.writer(fileAnalysis)
        # importing datetime module for now()
        import datetime
        # using now() to get current time
        current_time = datetime.datetime.now()
        Analysiswriter.writerow(['Ram Plot Analysis'])
        Analysiswriter.writerow(['JobID',OutPutDir,current_time])
        MolprovityRegionAll=MolProbitydfGeneralGly['MolprovityRegion']
        #MolprovityRegionStd=MolProbitydfGeneralGly['MolprovityRegionG']
        
        TotalResidue=len(MolprovityRegionAll)
        Analysiswriter.writerow(['Total Residue',TotalResidue])
        
        RegionwiseAll=MolProbitydfGeneralGly.groupby('MolprovityRegion')
        RegionwiseStd=MolProbitydfGeneralGly.groupby('MolprovityRegionG')
        RegionwiseAllkeys = RegionwiseAll.groups.keys()
        print(RegionwiseAllkeys)
        try:
            ResidueFavouredRegionStd=RegionwiseStd.get_group(0.0).reset_index()
            CountResidueFavouredRegionStd=len(ResidueFavouredRegionStd.index)
            PerResidueFavouredRegionStd=round(CountResidueFavouredRegionStd*100/TotalResidue,3)
        except:
            CountResidueFavouredRegionStd=0
            PerResidueFavouredRegionStd=0
        try:
            ResidueAllowedRegionStd=RegionwiseStd.get_group(0.02).reset_index()
            CountResidueAllowedRegionStd=len(ResidueAllowedRegionStd.index)
            PerResidueAllowedRegionStd=round(CountResidueAllowedRegionStd*100/TotalResidue,3)
        except:
            CountResidueAllowedRegionStd=0
            PerResidueAllowedRegionStd=0
        DisallowedResidueInfoStd=''
        try:   
            ResidueDisallowedRegionStd=RegionwiseStd.get_group(0.03).reset_index() 
            CountResidueDisallowedRegionStd=len(ResidueDisallowedRegionStd.index)
            PerResidueDisallowedRegionStd=round(CountResidueDisallowedRegionStd*100/TotalResidue,3)

            
        except:
            ResidueDisallowedRegionStd=0
            PerResidueDisallowedRegionStd=0
        Analysiswriter.writerow(['Ramachandran plot (Standard) statistics'])    
        Analysiswriter.writerow(['Favoured: ',CountResidueFavouredRegionStd,'('+str(PerResidueFavouredRegionStd)+'%)'])
        Analysiswriter.writerow(['Allowed: ',CountResidueAllowedRegionStd,'('+str(PerResidueAllowedRegionStd)+'%)'])
        Analysiswriter.writerow(['Disallowed: ',CountResidueDisallowedRegionStd,'('+str(PerResidueDisallowedRegionStd)+'%)'])
        if CountResidueDisallowedRegionStd >=0:
            Analysiswriter.writerow(['Disallowed Residues'])
            Analysiswriter.writerow(['SN.','PDB ID','Chain','Residue','Residue No','PHI','PSI'])
            for i in range(CountResidueDisallowedRegionStd):
                Analysiswriter.writerow([str(i+1)+'. ',ResidueDisallowedRegionStd['PDBID'][i], ResidueDisallowedRegionStd['Chain'][i],ResidueDisallowedRegionStd['Residue'][i],ResidueDisallowedRegionStd['ResNum'][i],round(ResidueDisallowedRegionStd['PHI'][i],2),round(ResidueDisallowedRegionStd['PSI'][i],2)])
                DisallowedResiduesStd=str(i+1)+'. '+ResidueDisallowedRegionStd['PDBID'][i]+' Chain: '+ ResidueDisallowedRegionStd['Chain'][i]+' '+ ResidueDisallowedRegionStd['Residue'][i]+ str(ResidueDisallowedRegionStd['ResNum'][i])+'PHI: '+ str(round(ResidueDisallowedRegionStd['PHI'][i],2))+' PSI: '+ str(round(ResidueDisallowedRegionStd['PSI'][i],2))
                DisallowedResidueInfoStd=DisallowedResidueInfoStd+DisallowedResiduesStd+','
                print(DisallowedResiduesStd)   
                
        try:
            ResidueFavouredRegionAll=RegionwiseAll.get_group(0.0).reset_index()
            CountResidueFavouredRegionAll=len(ResidueFavouredRegionAll.index)
            PerResidueFavouredRegionAll=round(CountResidueFavouredRegionAll*100/TotalResidue,3)
        except:
            CountResidueFavouredRegionAll=0
            PerResidueFavouredRegionAll=0
        try:
            ResidueAllowedRegionAll=RegionwiseAll.get_group(0.02).reset_index()
            CountResidueAllowedRegionAll=len(ResidueAllowedRegionAll.index)
            PerResidueAllowedRegionAll=round(CountResidueAllowedRegionAll*100/TotalResidue,3)
        except:
            CountResidueAllowedRegionAll=0
            PerResidueAllowedRegionAll=0
        DisallowedResidueInfoAll=''    
        try:
            ResidueDisallowedRegionAll=RegionwiseAll.get_group(0.03).reset_index()
            CountResidueDisallowedRegionAll=len(ResidueDisallowedRegionAll.index)
            PerResidueDisallowedRegionAll=round(CountResidueDisallowedRegionAll*100/TotalResidue,3)
            

        except:
            CountResidueDisallowedRegionAll=0
            PerResidueDisallowedRegionAll=0
        Analysiswriter.writerow(['Ramachandran plot (six categories) statistics'])
        Analysiswriter.writerow(['Favoured: ',CountResidueFavouredRegionAll,'('+str(PerResidueFavouredRegionAll)+'%)'])
        Analysiswriter.writerow(['Allowed: ',CountResidueAllowedRegionAll,'('+str(PerResidueAllowedRegionAll)+'%)'])
        Analysiswriter.writerow(['Disallowed: ',CountResidueDisallowedRegionAll,'('+str(PerResidueDisallowedRegionAll)+'%)'])
        if CountResidueDisallowedRegionAll >=0:
            Analysiswriter.writerow(['Disallowed Residues'])
            Analysiswriter.writerow(['SN.','PDB ID','Chain','Residue','Residue No','PHI','PSI'])
            for i in range(CountResidueDisallowedRegionAll):
                Analysiswriter.writerow([str(i+1)+'. ',ResidueDisallowedRegionAll['PDBID'][i], ResidueDisallowedRegionAll['Chain'][i],ResidueDisallowedRegionAll['Residue'][i],ResidueDisallowedRegionAll['ResNum'][i],round(ResidueDisallowedRegionAll['PHI'][i],2),round(ResidueDisallowedRegionAll['PSI'][i],2)])
                DisallowedResiduesAll=str(i+1)+'. '+ResidueDisallowedRegionAll['PDBID'][i]+' Chain: '+ ResidueDisallowedRegionAll['Chain'][i]+' '+ ResidueDisallowedRegionAll['Residue'][i]+ str(ResidueDisallowedRegionAll['ResNum'][i])+' PHI: '+ str(round(ResidueDisallowedRegionAll['PHI'][i],2))+' PSI: '+ str(round(ResidueDisallowedRegionAll['PSI'][i],2))
                DisallowedResidueInfoAll=DisallowedResidueInfoAll+DisallowedResiduesAll+','
                print(DisallowedResiduesAll)
  
        
        fileAnalysis.close()
        print(ResidueDisallowedRegionStd)
    else:
        log.write('Total Residue Count='+str(TotalResidueCount))
        print('No Valid Residues Found')
    
    # Implementation of matplotlib function
    if 'MapType2DAll' in MapType and TotalResidueCount >0 :

        # JobID='Ram6561f98446989'
    
        fig, ax = plt.subplots(nrows=2, ncols=3)
        
        # data1 = pd.read_csv(OutPutDir+'/MolProbityPhiPsiTauCaiOmegaBFactorAll.csv')
        # MolProbitydf = pd.DataFrame(data1)
        gdCountour = MolProbitydf.groupby('Group')
        i=0
        j=0
        GroupList=['General','Gly','Val_Ile','prePro','transPro','cisPro']
        for GroupsCountour in GroupList:
            MolprovityDataPath=pkg_resources.resource_filename('ramplot',"RamBoundry/MolprovityAllRegion"+GroupsCountour+".csv")
            CountourDataMol = pd.read_csv(MolprovityDataPath)
            CountourDfMol = pd.DataFrame(CountourDataMol)
            x_list=np.unique(CountourDfMol['MolprovityPHI'].to_numpy())
            y_list=np.unique(CountourDfMol['MolprovityPSI'].to_numpy())
            X, Y = np.meshgrid(x_list, y_list)
            Z=CountourDataMol.pivot(index='MolprovityPSI',columns='MolprovityPHI',values='MolprovityRegion')
            ax[i,j].set_aspect(1)
            ax[i,j].contour(X, Y, Z,linewidths=0.2)
            try:
                GroupsCountourDataframe=gdCountour.get_group(GroupsCountour).reset_index()
                gdCountourRegion = GroupsCountourDataframe.groupby('MolprovityRegion')
                # extract keys from groups
                keysCountourRegion = gdCountourRegion.groups.keys()
                for keyCountourRegion in keysCountourRegion:
                    RegionDf=gdCountourRegion.get_group(keyCountourRegion).reset_index()
                    x1=RegionDf['PHI']
                    y1=RegionDf['PSI']
                    if keyCountourRegion==0:
                        ax[i,j].scatter(x1, y1, c='springgreen',s=0.40)
                    if keyCountourRegion==0.02:
                        ax[i,j].scatter(x1, y1, c='blue',s=0.40)
                    if keyCountourRegion==0.03:
                        ax[i,j].scatter(x1, y1, c='red',s=0.40)
            except:
                pass
            ax[i,j].set_xlabel("φ(Degree)",fontsize=5)
            ax[i,j].set_ylabel("ψ(Degree)",fontsize=5)
            
            ax[i,j].set_xlim(-180, 180)
            ax[i,j].set_ylim(-180, 180)
            if GroupsCountour=='Val_Ile':
                GroupsCountour='Val/Ile'
            ax[i,j].set_xticks(np.arange(-180, 181, step=60))  # Set x-axis ticks
            ax[i,j].set_yticks(np.arange(-180, 181, step=60))   # Set y-axis ticks

            ax[i,j].set_title(GroupsCountour,fontdict ={'size':6})
            ax[i,j].tick_params(direction='out', length=2,  colors='r',
               grid_color='r', grid_alpha=0.5,labelsize=5)
            if j < 2:
                j=j+1
            else:
                j=0
                i=i+1
        # plt.xlabel("PHI",fontsize=5)
        # plt.ylabel("PSI",fontsize=5)
        # plt.xticks(np.arange(-180, 180, step=60),fontsize=5)
        # plt.yticks(np.arange(-180, 180, step=60),fontsize=5)
        #plt.yticks(fontsize=5)
        # Custom legend entries
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='springgreen', markersize=2,label='Favored'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='blue',  markersize=2,label='Allowed'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=2,label='Disallowed')
        ]
        
        plt.tight_layout()
        plt.savefig(OutPutDir+'/Plots/MapType2DAll.'+PlotFileType,dpi=PlotResolutions)
        # plt.show()
    if 'MapType3DAll' in MapType and TotalResidueCount >0:
        gdCountour2 = MolProbitydf.groupby('Group')
        fig = plt.figure()
        i=1
        GroupList=['General','Gly','Val_Ile','prePro','transPro','cisPro']
        for GroupsCountour in GroupList:
            ax1 = fig.add_subplot(2,3,i, projection='3d')
            MolprovityDataPath=pkg_resources.resource_filename('ramplot',"RamBoundry/MolprovityAllRegion"+GroupsCountour+".csv")
            CountourDataMol = pd.read_csv(MolprovityDataPath)
            CountourDfMol = pd.DataFrame(CountourDataMol)
            x_list=np.unique(CountourDfMol['MolprovityPHI'].to_numpy())
            y_list=np.unique(CountourDfMol['MolprovityPSI'].to_numpy())
            X, Y = np.meshgrid(x_list, y_list)
            Z=CountourDataMol.pivot(index='MolprovityPSI',columns='MolprovityPHI',values='MolprovityRegion')
            ax1.contour(X, Y, Z,linewidths=0.2)
            try:
                GroupsCountourDataframe2=gdCountour2.get_group(GroupsCountour).reset_index()
                ax1.view_init(elev=45)
                GroupsCountourDataframe2['PHI'] = GroupsCountourDataframe2['PHI'].astype(int)
                GroupsCountourDataframe2['PSI'] = GroupsCountourDataframe2['PSI'].astype(int)
                ac=GroupsCountourDataframe2.groupby(["PHI", "PSI"]).size().reset_index(name='Count')

                #ac.to_csv('Test3d.csv')
                phi=ac['PHI'].tolist()
                psi=ac['PSI'].tolist()
                count=ac['Count'].tolist()
                
                xpi=len(phi)
                x3 = phi
                y3 = psi
                z3 = np.zeros(xpi)
                dx = np.ones(xpi)
                dy = np.ones(xpi)
                dz = count
                cmap = plt.get_cmap('gist_earth') # Get desired colormap - you can change this!
                max_height = np.max(dz)   # get range of colorbars so we can normalize
                min_height = np.min(dz)
                # scale each z to [0,1], and get their rgb values
                rgba = [cmap((k-min_height)/max_height) for k in dz]
                ax1.bar3d(x3, y3, z3, dx, dy, dz, color=rgba, zsort='average')
                colourMap = plt.cm.ScalarMappable(cmap=plt.cm.gist_earth)
                colourMap.set_array(dz)
                
            except:
                ax1.set_zlim(0, 1)
                ax1.view_init(elev=45)
                pass
            ax1.grid(False)
           
            
            ax1.set_xlabel("φ(Degree)",fontsize=5)
            ax1.set_ylabel("ψ(Degree)",fontsize=5)
            ax1.set_zlabel('Frequency',fontsize=5)
            ax1.set_xlim(-180, 180)
            ax1.set_ylim(-180, 180)
            if GroupsCountour=='Val_Ile':
                GroupsCountour='Val/Ile'
            ax1.set_xticks(np.arange(-180, 181, step=60))  # Set x-axis ticks
            ax1.set_yticks(np.arange(-180, 181, step=60))   # Set y-axis ticks

            ax1.set_title(GroupsCountour,fontdict ={'size':6})
            ax1.tick_params(direction='out', length=2,  colors='r',
               grid_color='r', grid_alpha=0.5,labelsize=5)
            font={'size':5}
            ax1.tick_params('z', labelsize=font['size'])
            fig.align_xlabels()
            i=i+1

        plt.savefig(OutPutDir+'/Plots/MapType3DAll.'+PlotFileType,dpi=PlotResolutions)
    if 'MapType2DStd' in MapType and TotalResidueCount >0:
            fig, ax = plt.subplots(figsize=(6,6))
            MolprovityDataPath=pkg_resources.resource_filename('ramplot',"RamBoundry/MolprovityAllRegionGeneral.csv")
            CountourDataMol = pd.read_csv(MolprovityDataPath)
            CountourDfMol = pd.DataFrame(CountourDataMol)
            x_list=np.unique(CountourDfMol['MolprovityPHI'].to_numpy())
            y_list=np.unique(CountourDfMol['MolprovityPSI'].to_numpy())
            X, Y = np.meshgrid(x_list, y_list)
            Z=CountourDataMol.pivot(index='MolprovityPSI',columns='MolprovityPHI',values='MolprovityRegion')
            ax.contour(X, Y, Z,linewidths=0.2)
            #colors=['deepskyblue','aqua','red'],
            ax.set_aspect(1)
            gdCountourGroup = MolProbitydfGeneralGly.groupby('GroupGly')
            keysCountourGroup = gdCountourGroup.groups.keys()
            for keyCountourGroup in keysCountourGroup:    
                GroupRegionDf=gdCountourGroup.get_group(keyCountourGroup).reset_index()
                gdCountourRegion = GroupRegionDf.groupby('MolprovityRegionG')
                    # extract keys from groups ,
                if keyCountourGroup=='General':
                    keysCountourRegion = gdCountourRegion.groups.keys()
                    # print(keysCountourRegion)
                    for keyCountourRegion in keysCountourRegion:
                        RegionDf=gdCountourRegion.get_group(keyCountourRegion).reset_index()
                        x1=RegionDf['PHI']
                        y1=RegionDf['PSI']
                        if keyCountourRegion==0:
                            ax.scatter(x1, y1, c='springgreen',s=5)
                        if keyCountourRegion==0.02:
                            ax.scatter(x1, y1, c='blue',s=5)
                        if keyCountourRegion==0.03:
                            ax.scatter(x1, y1, c='red',s=5)
                if keyCountourGroup=='Gly':
                    keysCountourRegion = gdCountourRegion.groups.keys()
                    # print(keysCountourRegion)
                    for keyCountourRegion in keysCountourRegion:
                        RegionDf=gdCountourRegion.get_group(keyCountourRegion).reset_index()
                        x1=RegionDf['PHI']
                        y1=RegionDf['PSI']
                        if keyCountourRegion==0:
                            ax.scatter(x1, y1,marker='^',c='springgreen',s=5)
                        if keyCountourRegion==0.02:
                            ax.scatter(x1, y1,marker='^',c='blue',s=5)
                        if keyCountourRegion==0.03:
                            ax.scatter(x1, y1, marker='^',c='red',s=5)
    
            ax.set_xlim(-180, 180)
            ax.set_ylim(-180, 180)
            #ax.set_title('Ramachandran Plot',fontdict ={'weight':'bold'})
            ax.set_xlabel("φ(Degree)",fontsize=5)
            ax.set_ylabel("ψ (Degree)",fontsize=5)
            ax.set_xticks(np.arange(-180, 181, step=60))  # Set x-axis ticks
            ax.set_yticks(np.arange(-180, 181, step=60))   # Set y-axis ticks

            #ax.set_title(GroupsCountour,fontdict ={'size':10})
            ax.tick_params(direction='out', length=2,  colors='r',
               grid_color='r', grid_alpha=0.5,labelsize=5)
            #plt.tight_layout()
            #fig.text(0.5, 0.04, 'Total Residues - '+str(TotalResidue)+' Favoured- '+str(CountResidueFavouredRegionStd)+'('+str(PerResidueDisallowedRegionStd)+'%)  Allowed '+str(CountResidueAllowedRegionStd)+'('+str(PerResidueAllowedRegionStd)+'%) Disallowed - '+str(CountResidueDisallowedRegionStd)+'('+str(PerResidueDisallowedRegionStd)+'%)',  ha='center',fontsize=4)
            #fig.text(0.5, 0.03,DisallowedResidueInfoStd, ha='center',fontsize=3,wrap=True)
            #fig.text(0.5, 0.02,'2D Ramachandran plot  Here, green, blue  and red dots represent torsion angles of favoured , allowed and disallowed regions residues other than glycine.Glycine Reside Represent in green,  blue and red  triangles', ha='center',fontsize=5,wrap=True)
           
            plt.savefig(OutPutDir+'/Plots/StdMapType2DGeneralGly.'+PlotFileType,dpi=PlotResolutions)
        
    if 'MapType3DStd' in MapType and TotalResidueCount >0:
          fig = plt.figure(figsize=(6,6))
          #fig.tight_layout()
          
          ax3 = fig.add_subplot(1,1,1, projection='3d')
          #ax1.plot_surface(X, Y, Z, lw=0.1, cmap='coolwarm', edgecolor='k')
          GroupsCountourDataframe2=df
          GroupsCountourDataframe2['PHI'] = GroupsCountourDataframe2['PHI'].astype(int)
          GroupsCountourDataframe2['PSI'] = GroupsCountourDataframe2['PSI'].astype(int)
          ac=GroupsCountourDataframe2.groupby(["PHI", "PSI"]).size().reset_index(name='Count')

          #ac.to_csv('Test3d.csv')
          phi=ac['PHI'].tolist()
          psi=ac['PSI'].tolist()
          count=ac['Count'].tolist()

          xpi=len(phi)
          x3 = phi
          y3 = psi
          z3 = np.zeros(xpi)
          dx = np.ones(xpi)
          dy = np.ones(xpi)
          dz = count
          cmap = plt.get_cmap('viridis') # Get desired colormap - you can change this!
          max_height = np.max(dz)   # get range of colorbars so we can normalize
          min_height = np.min(dz)
          rgba = [cmap((k-min_height)/max_height) for k in dz]

          colourMap = plt.cm.ScalarMappable(cmap=plt.cm.gist_earth)
          colourMap.set_array(dz)
          MolprovityDataPath=pkg_resources.resource_filename('ramplot',"RamBoundry/MolprovityAllRegionGeneral.csv")
          CountourDataMol = pd.read_csv(MolprovityDataPath)
          CountourDfMol = pd.DataFrame(CountourDataMol)
          x_list=np.unique(CountourDfMol['MolprovityPHI'].to_numpy())
          y_list=np.unique(CountourDfMol['MolprovityPSI'].to_numpy())
          X, Y = np.meshgrid(x_list, y_list)
          Z=CountourDataMol.pivot(index='MolprovityPSI',columns='MolprovityPHI',values='MolprovityRegion')
          ax3.contour(X, Y, Z,linewidths=0.2)
          #colors=['deepskyblue','aqua','red'],
          ax3.bar3d(x3, y3, z3, dx, dy, dz, color=rgba, zsort='average')
          ax3.grid(False)
          ax3.set_xlim(-180, 180)
          ax3.set_ylim(-180, 180)
          ax3.set_zlabel('Frequency',fontsize=5)
          #ax3.tick_params('z', labelsize=font['size'])
          ax3.view_init(elev=45)
          #plt.title(GroupsCountour,fontdict ={'family':'DejaVu Sans','size':10,'weight':'bold'})
          plt.xlabel("φ(Degree)",fontsize=5)
          plt.ylabel("ψ(Degree)",fontsize=5)

          plt.xticks(np.arange(-180, 180, step=60),fontsize=5)
          plt.yticks(np.arange(-180, 180, step=60),fontsize=5)
          font={'size':5}
          
          i=i+1
          plt.savefig(OutPutDir+'/Plots/StdMapType3DGeneral.'+PlotFileType,dpi=PlotResolutions)  
    arr = df.to_numpy()
    try:
        ResultTorsionAngles = MolProbitydfGeneralGly
        ResultTorsionAngles['MolprovityRegion'] = ResultTorsionAngles['MolprovityRegion'].replace({0.0: 'Favoured', 0.02: 'Allowed', 0.03: 'Disallowed'})
        ResultTorsionAngles['MolprovityRegionG'] = ResultTorsionAngles['MolprovityRegionG'].replace({0.0: 'Favoured', 0.02: 'Allowed', 0.03: 'Disallowed'})
        ResultTorsionAngles.rename(columns = {'MolprovityRegion':'RamaChandran Plot Region(Six Category)'}, inplace = True) 
        ResultTorsionAngles.rename(columns = {'MolprovityRegionG':'RamaChandran Plot Region(Std)'}, inplace = True) 
        #.replace(0.00, 'Favoured',inplace=True)
        ResultTorsionAngles2=ResultTorsionAngles.drop(['AID', 'Isomer'], axis=1)
        ResultTorsionAngles2.to_csv(OutPutDir+'/ResultTorsionAngles.csv')
        os.remove(OutPutDir+'/PhiPsiTauCaiOmegaBFactorCalculation.csv')
        os.remove(OutPutDir+'/MolProbityPhiPsiTauCaiOmegaBFactorGeneralGly.csv')
        os.remove(OutPutDir+'/MolProbityPhiPsiTauCaiOmegaBFactorAll.csv')
    except:
        log.write('Error: Unable to write ResultTorsionAngles.csv')
    log.close()
    return arr
#End 
#JobID='Ram660a8b8362ce7'
#abc=TorsionAngleCalculation(JobID,['MapType2DStd','MapType2DAll','MapType3DStd','MapType3DAll'])
# if __name__ == '__main__':
#     globals()[sys.argv[1]](sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
import sys
import Bio.PDB
import csv
import os
import MDAnalysis as mda
from MDAnalysis.coordinates import PDB
from concurrent.futures import ThreadPoolExecutor
import shutil
import pkg_resources 
# def ExtractPDBFromTrajectory(tprfile,xtcfile,JobID):
#     # Load the topology and trajectory files
#     u = mda.Universe(tprfile, xtcfile)
    
#     # Select non-water atoms
    
#     protein = u.select_atoms('not resname SOL and not resname HOH')
    
#     # Loop over each frame in the trajectory
#     for ts in u.trajectory:
#         # Create a file name for the current frame
#         frame_filename = OutPutDir+'/PDB/frame_'+str(ts.frame)+'.pdb'
        
#         # Write the current frame to a PDB file without water molecules
#         with mda.Writer(frame_filename, protein.n_atoms) as W:
#             W.write(protein)
    
#     print("All frames have been extracted without water molecules.")
def write_frame(protein, frame_filename):
    with mda.Writer(frame_filename, protein.n_atoms) as W:
        W.write(protein)

def ExtractPDBFromTrajectory(tprfile, xtcfile, OutPutDir,log,interval):
    # Load the topology and trajectory files
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="MDAnalysis.coordinates.PDB")
    log.write('InSIde FunctionUserTrajectoryInputPhiPsiPlot \n')
    u = mda.Universe(tprfile, xtcfile)
    
    # Select non-water atoms
    protein = u.select_atoms('not resname SOL and not resname HOH')
    
    # Create the output directory if it does not exist
    output_dir = os.path.join(OutPutDir+'/PDB/')
    os.makedirs(output_dir, exist_ok=True)
    
    # Use ThreadPoolExecutor to write frames in parallel
    with ThreadPoolExecutor() as executor:
        futures = []
        for ts in u.trajectory[::interval]:
            # Create a file name for the current frame
            frame_filename = os.path.join(output_dir, f'frame_{ts.frame}.pdb')
            
            # Submit a task to write the current frame
            futures.append(executor.submit(write_frame, protein, frame_filename))
        
        # Ensure all tasks are completed
        for future in futures:
            future.result()
    # try:
    #     shutil.rmtree(xtcfile)
    #     shutil.rmtree(tprfile)
    # except: 
    #     log.write(' shutil unable to remove trajectory files \n')
            
    # u.close()
    # print("All frames have been extracted without water molecules.")
# JobID='RamPlot66a4e246328b9'

def PHIPSICalculateParticularResidue(OutPutDir,InputResidues,TorsionAngles,log):
    os.makedirs(OutPutDir+'/Result',exist_ok = True)
    # f=open(OutPutDir+'/Result/TorsionANglesAllResidoe.csv', 'a', newline='')
    # writer = csv.writer(f)
    # writer.writerow(['PDBID','Chain','Residue','ResidueNo','PHI', 'PSI'])
        # pdb_code = "5AVL_Clean/5AVL_1.pdb"
    log.write('InSIde PHIPSICalculateParticularResidue \n')
    files=os.listdir(OutPutDir+'/PDB/')
    for file in files: 
        inputpath=OutPutDir+'/PDB/'+file
        # print("About to load Bio.PDB and the PDB file...")
        structure = Bio.PDB.PDBParser().get_structure(inputpath, "%s" % inputpath)
        
        structure.atom_to_internal_coordinates()
        # Res=structure[0]['A'].get_residues()
        
        NoInputResidues=len(InputResidues)
        if NoInputResidues >= 1:
            for i in range(NoInputResidues):
                try:
                    # print(InputResidues[i])
                    chain=InputResidues[i][0] 
                    residue=int(InputResidues[i][1:])
                    ric= structure[0][chain][residue].internal_coord
                    if ric:
                        PHI=ric.get_angle("phi")
                        PSI=ric.get_angle("psi")
                        ResidueName=structure[0][chain][residue].get_resname()
                        # print(PHI)
                        # print(PSI)
                        if PHI and PSI:
                            # writer.writerow([inputpath, chain,ResidueName,residue,PHI, PSI])
                            TorsionAngles.loc[len(TorsionAngles)] = [inputpath, chain,ResidueName,residue,PHI, PSI]
                    else:
                        print('Error')
    # f.close()
                except:
                    
                    log.write('Invalid Input:'+InputResidues[i]+' \n')
                    continue

    
def FunctionUserTrajectoryInputPhiPsiPlot(InputTPRFilePath,InputXTCFilePath,OutPutDir,InputResidues,FrameInterval,MapType,PlotResolutions,PlotFileType):

    import pandas as pd
    import csv
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    def ramachandran_type_Gly_Non_Gly(residue) :
        if residue.upper()=="GLY" :
            return "Gly"
        else:
            return "General"
    isExist = os.path.exists(OutPutDir)
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(OutPutDir)
    isExist = os.path.exists(OutPutDir+'/Plots')
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(OutPutDir+'/Plots')
    #JobID='RamPlot661abdf5bf6bc' 
    # MapType=['MapType2DStd','MapType2DAll','MapType3DStd','MapType3DAll']
    # PlotResolutions=600
    # PlotFileType='png'
    log=open(OutPutDir+'/log.dat', 'a')
    # + MapType+' \n'
    log.write('InSIde FunctionUserTrajectoryInputPhiPsiPlot \n')
    PlotResolutions=int(PlotResolutions)
    interval=int(FrameInterval)
    # try:
    result_df = pd.DataFrame()
    # TrajectoryInputFiles=os.listdir(OutPutDir+'/Trajectory/')
    # for TrajectoryInputFile in TrajectoryInputFiles:
    #     if(TrajectoryInputFile.split('.')[-1]=='tpr'):
    InputTPRFiles=InputTPRFilePath
        # if(TrajectoryInputFile.split('.')[-1]=='xtc'):
    InputXTCFiles=InputXTCFilePath

    if InputTPRFiles and InputXTCFiles:
        try:
            ExtractPDBFromTrajectory(InputTPRFiles,InputXTCFiles,OutPutDir,log,interval)
            # os.rmdir(OutPutDir+'/Trajectory/')

            # InputResidues=['A101','A104']
            # print(InputResidues)
            InputResidues = InputResidues.split(',')
            # print(InputResidues)
            NoInputResidues=len(InputResidues)
            if NoInputResidues >= 1:
                    TorsionAngles = pd.DataFrame(columns=['PDBID','Chain','Residue','ResidueNo','PHI', 'PSI'])
                    try:
                        PHIPSICalculateParticularResidue(OutPutDir,InputResidues,TorsionAngles,log)                    
                        TorsionAnglesgrouped = TorsionAngles.groupby(['Chain', 'ResidueNo'])
                        NoInputResidues=len(InputResidues)
                        if NoInputResidues >= 1:
                            for i in range(NoInputResidues):
                                try:
                                    # print(InputResidues[i])
                                    chain=InputResidues[i][0] 
                                    residue=int(InputResidues[i][1:])
                                    TorsionAnglesgroup=TorsionAnglesgrouped.get_group((chain,residue))
                                    TorsionAnglesgroup.to_csv(OutPutDir+'/Result/'+InputResidues[i]+'.csv')
                                except:
                                    continue
                        InputFiles=os.listdir(OutPutDir+'/Result/')
                        for InputFile in InputFiles:
                            PlotName=InputFile.split('.')[0]
                            InputPath=OutPutDir+'/Result/'+InputFile
                            # print(InputPath)
                            CustomData = pd.read_csv(InputPath)
                            InputColName=list(CustomData.columns)
                            MolProbitydfStandard = pd.DataFrame(columns=['PDBID','Chain','Residue','ResidueNo', 'PHI', 'PSI','Region','Group'])
                            # try:
                            PDBID=CustomData['PDBID']
                            Chain=CustomData['Chain']
                            Residue=CustomData['Residue']
                            ResidueNo=CustomData['ResidueNo']
                            PHI=CustomData['PHI']
                            PSI=CustomData['PSI']
                            ln=len(PHI)
                            MolprovityDataPath=pkg_resources.resource_filename('ramplot',"RamBoundry/MolprovityAllRegionGeneral.csv")
                            MolprovityData = pd.read_csv(MolprovityDataPath)
                            MolprovityPHI=MolprovityData['MolprovityPHI']
                            MolprovityPSI=MolprovityData['MolprovityPSI']
                            for x in range(ln):
                                    InputPHI=int(PHI[x])
                                    InputPSI=int(PSI[x])
                                    IndexListofPHI = MolprovityData.index[MolprovityData['MolprovityPHI'] == InputPHI].tolist()
                                    for i in IndexListofPHI:
                                        if MolprovityData['MolprovityPSI'][i]==InputPSI:
                                            # print(MolprovityData['MolprovityPSI'][i])
                                            MolprovityRegionG=MolprovityData['MolprovityRegion'][i]
                                            Group=ramachandran_type_Gly_Non_Gly(Residue[x])
                                            rows=[PDBID[x],Chain[x],Residue[x],ResidueNo[x],PHI[x],PSI[x],MolprovityRegionG,Group]
                                            MolProbitydfStandard.loc[len(MolProbitydfStandard)] = rows
                            # print(MolProbitydfStandard)
                        
                            # print(MolProbitydfStandard)
                            CountTotalResidue=len(MolProbitydfStandard.index)
                            if  CountTotalResidue > 0:
                                fileAnalysis=open(OutPutDir+'/Analysis.csv', 'a', newline='')
                                Analysiswriter = csv.writer(fileAnalysis)
                                # importing datetime module for now()
                                import datetime
                                # using now() to get current time
                                current_time = datetime.datetime.now()
                                Analysiswriter.writerow(['Ram Plot Analysis'])
                                Analysiswriter.writerow(['JobID',current_time])
                                Analysiswriter.writerow(['Analysis of ',PlotName])
                                MolprovityRegionStd=MolProbitydfStandard['Region']
                                RegionwiseStd=MolProbitydfStandard.groupby('Region')
                                TotalResidue=len(MolprovityRegionStd)
                                Analysiswriter.writerow(['Total Residue',TotalResidue])
                                
                                try:
                                    ResidueFavouredRegionStd=RegionwiseStd.get_group(0.0).reset_index()
                                    CountResidueFavouredRegionStd=len(ResidueFavouredRegionStd.index)
                                    PerResidueFavouredRegionStd=round(CountResidueFavouredRegionStd*100/TotalResidue,3)
                                except:
                                    CountResidueFavouredRegionStd=0
                                    PerResidueFavouredRegionStd=0
                                try:
                                    ResidueAllowedRegionStd=RegionwiseStd.get_group(0.02).reset_index()
                                    CountResidueAllowedRegionStd=len(ResidueAllowedRegionStd.index)
                                    PerResidueAllowedRegionStd=round(CountResidueAllowedRegionStd*100/TotalResidue,3)
                                except:
                                    CountResidueAllowedRegionStd=0
                                    PerResidueAllowedRegionStd=0
                                DisallowedResidueInfoStd=''
                                try:   
                                    ResidueDisallowedRegionStd=RegionwiseStd.get_group(0.03).reset_index() 
                                    CountResidueDisallowedRegionStd=len(ResidueDisallowedRegionStd.index)
                                    PerResidueDisallowedRegionStd=round(CountResidueDisallowedRegionStd*100/TotalResidue,3)
                            
                                    
                                except:
                                    CountResidueDisallowedRegionStd=0
                                    ResidueDisallowedRegionStd=0
                                    PerResidueDisallowedRegionStd=0
                                Analysiswriter.writerow(['Ramachandran plot (Standard) statistics'])    
                                Analysiswriter.writerow(['Favoured: ',CountResidueFavouredRegionStd,'('+str(PerResidueFavouredRegionStd)+'%)'])
                                Analysiswriter.writerow(['Allowed: ',CountResidueAllowedRegionStd,'('+str(PerResidueAllowedRegionStd)+'%)'])
                                Analysiswriter.writerow(['Disallowed: ',CountResidueDisallowedRegionStd,'('+str(PerResidueDisallowedRegionStd)+'%)'])
                                if CountResidueDisallowedRegionStd >=0:
                                    Analysiswriter.writerow(['Disallowed Residues'])
                                    Analysiswriter.writerow(['SN.','PDB ID','Chain','Residue','Residue No','PHI','PSI'])
                                    for i in range(CountResidueDisallowedRegionStd):
                                        Analysiswriter.writerow([str(i+1)+'. ',ResidueDisallowedRegionStd['PDBID'][i], ResidueDisallowedRegionStd['Chain'][i],ResidueDisallowedRegionStd['Residue'][i],ResidueDisallowedRegionStd['ResidueNo'][i],round(ResidueDisallowedRegionStd['PHI'][i],2),round(ResidueDisallowedRegionStd['PSI'][i],2)])
                                        DisallowedResiduesStd=str(i+1)+'. '+ResidueDisallowedRegionStd['PDBID'][i]+' Chain: '+ ResidueDisallowedRegionStd['Chain'][i]+' '+ str(ResidueDisallowedRegionStd['Residue'][i])+ str(ResidueDisallowedRegionStd['ResidueNo'][i])+'PHI: '+ str(round(ResidueDisallowedRegionStd['PHI'][i],2))+' PSI: '+ str(round(ResidueDisallowedRegionStd['PSI'][i],2))
                                        DisallowedResidueInfoStd=DisallowedResidueInfoStd+DisallowedResiduesStd+','
                                        # print(DisallowedResiduesStd)     
                                
                                fileAnalysis.close()
                                # print(ResidueDisallowedRegionStd)
                            else:
                                # print('No Valid Residues Found')
                                log.write('No Valid Residues Found')               
                            if 'MapType2DStd' in MapType and CountTotalResidue > 0:
                                    fig, ax = plt.subplots(figsize=(6,6))
                                    MolprovityDataPath=pkg_resources.resource_filename('ramplot',"RamBoundry/MolprovityAllRegionGeneral.csv")
                                    CountourDataMol = pd.read_csv(MolprovityDataPath)
                                    CountourDfMol = pd.DataFrame(CountourDataMol)
                                    x_list=np.unique(CountourDfMol['MolprovityPHI'].to_numpy())
                                    y_list=np.unique(CountourDfMol['MolprovityPSI'].to_numpy())
                                    X, Y = np.meshgrid(x_list, y_list)
                                    Z=CountourDataMol.pivot(index='MolprovityPSI',columns='MolprovityPHI',values='MolprovityRegion')
                                    ax.contour(X, Y, Z,linewidths=0.2)
                                    #colors=['deepskyblue','aqua','red'],
                                    ax.set_aspect(1)
                                    gdCountourGroup = MolProbitydfStandard.groupby('Group')
                                    keysCountourGroup = gdCountourGroup.groups.keys()
                                    for keyCountourGroup in keysCountourGroup:    
                                        GroupRegionDf=gdCountourGroup.get_group(keyCountourGroup).reset_index()
                                        gdCountourRegion = GroupRegionDf.groupby('Region')
                                            # extract keys from groups ,
                                        if keyCountourGroup=='General':
                                            keysCountourRegion = gdCountourRegion.groups.keys()
                                            #print(keysCountourRegion)
                                            for keyCountourRegion in keysCountourRegion:
                                                RegionDf=gdCountourRegion.get_group(keyCountourRegion).reset_index()
                                                x1=RegionDf['PHI']
                                                y1=RegionDf['PSI']
                                                if keyCountourRegion==0:
                                                    ax.scatter(x1, y1, c='springgreen',s=5)
                                                if keyCountourRegion==0.02:
                                                    ax.scatter(x1, y1, c='blue',s=5)
                                                if keyCountourRegion==0.03:
                                                    ax.scatter(x1, y1, c='red',s=5)
                                        if keyCountourGroup=='Gly':
                                            keysCountourRegion = gdCountourRegion.groups.keys()
                                            #print(keysCountourRegion)
                                            for keyCountourRegion in keysCountourRegion:
                                                RegionDf=gdCountourRegion.get_group(keyCountourRegion).reset_index()
                                                x1=RegionDf['PHI']
                                                y1=RegionDf['PSI']
                                                if keyCountourRegion==0:
                                                    ax.scatter(x1, y1,marker='^',c='springgreen',s=5)
                                                if keyCountourRegion==0.02:
                                                    ax.scatter(x1, y1,marker='^',c='blue',s=5)
                                                if keyCountourRegion==0.03:
                                                    ax.scatter(x1, y1, marker='^',c='red',s=5)
                            
                                    ax.set_xlim(-180, 180)
                                    ax.set_ylim(-180, 180)
                                    #ax.set_title('Ramachandran Plot',fontdict ={'weight':'bold'})
                                    ax.set_xlabel("φ((Degree)",fontsize=5)
                                    ax.set_ylabel("ψ(Degree)",fontsize=5)
                                    ax.set_xticks(np.arange(-180, 181, step=60))  # Set x-axis ticks
                                    ax.set_yticks(np.arange(-180, 181, step=60))   # Set y-axis ticks
                            
                                    #ax.set_title(GroupsCountour,fontdict ={'size':10})
                                    ax.tick_params(direction='out', length=2,  colors='r',
                                       grid_color='r', grid_alpha=0.5,labelsize=5)
                                    #plt.tight_layout()
                                    #fig.text(0.5, 0.04, 'Total Residues - '+str(TotalResidue)+' Favoured- '+str(CountResidueFavouredRegionStd)+'('+str(PerResidueDisallowedRegionStd)+'%)  Allowed '+str(CountResidueAllowedRegionStd)+'('+str(PerResidueAllowedRegionStd)+'%) Disallowed - '+str(CountResidueDisallowedRegionStd)+'('+str(PerResidueDisallowedRegionStd)+'%)',  ha='center',fontsize=4)
                                    #fig.text(0.5, 0.03,DisallowedResidueInfoStd, ha='center',fontsize=3,wrap=True)
                                    #fig.text(0.5, 0.02,'2D Ramachandran plot  Here, green, blue  and red dots represent torsion angles of favoured , allowed and disallowed regions residues other than glycine.Glycine Reside Represent in green,  blue and red  triangles', ha='center',fontsize=5,wrap=True)
                                   
                                    plt.savefig(OutPutDir+'/Plots/StdMapType2DGeneralGly_'+PlotName+'.'+PlotFileType,dpi=PlotResolutions)
                            if 'MapType3DStd' in MapType and CountTotalResidue > 0:
                                  fig = plt.figure(figsize=(6,6))
                                  #fig.tight_layout()
                                  
                                  ax3 = fig.add_subplot(1,1,1, projection='3d')
                                  #ax1.plot_surface(X, Y, Z, lw=0.1, cmap='coolwarm', edgecolor='k')
                                  GroupsCountourDataframe2=MolProbitydfStandard
                                  GroupsCountourDataframe2['PHI'] = GroupsCountourDataframe2['PHI'].astype(int)
                                  GroupsCountourDataframe2['PSI'] = GroupsCountourDataframe2['PSI'].astype(int)
                                  ac=GroupsCountourDataframe2.groupby(["PHI", "PSI"]).size().reset_index(name='Count')
                            
                                  #ac.to_csv('Test3d.csv')
                                  phi=ac['PHI'].tolist()
                                  psi=ac['PSI'].tolist()
                                  count=ac['Count'].tolist()
                            
                                  xpi=len(phi)
                                  x3 = phi
                                  y3 = psi
                                  z3 = np.zeros(xpi)
                                  dx = np.ones(xpi)
                                  dy = np.ones(xpi)
                                  dz = count
                                  cmap = plt.get_cmap('viridis') # Get desired colormap - you can change this!
                                  max_height = np.max(dz)   # get range of colorbars so we can normalize
                                  min_height = np.min(dz)
                                  rgba = [cmap((k-min_height)/max_height) for k in dz]
                            
                                  colourMap = plt.cm.ScalarMappable(cmap=plt.cm.gist_earth)
                                  colourMap.set_array(dz)
                                  MolprovityDataPath=pkg_resources.resource_filename('ramplot',"RamBoundry/MolprovityAllRegionGeneral.csv")
                                  CountourDataMol = pd.read_csv(MolprovityDataPath)
                                  CountourDfMol = pd.DataFrame(CountourDataMol)
                                  x_list=np.unique(CountourDfMol['MolprovityPHI'].to_numpy())
                                  y_list=np.unique(CountourDfMol['MolprovityPSI'].to_numpy())
                                  X, Y = np.meshgrid(x_list, y_list)
                                  Z=CountourDataMol.pivot(index='MolprovityPSI',columns='MolprovityPHI',values='MolprovityRegion')
                                  ax3.contour(X, Y, Z,linewidths=0.2)
                                  #colors=['deepskyblue','aqua','red'],
                                  ax3.bar3d(x3, y3, z3, dx, dy, dz, color=rgba, zsort='average')
                                  ax3.grid(False)
                                  ax3.set_xlim(-180, 180)
                                  ax3.set_ylim(-180, 180)
                                  ax3.set_zlabel('Frequency',fontsize=5)
                                  #ax3.tick_params('z', labelsize=font['size'])
                                  ax3.view_init(elev=45)
                                  #plt.title(GroupsCountour,fontdict ={'family':'DejaVu Sans','size':10,'weight':'bold'})
                                  plt.xlabel("φ((Degree)",fontsize=5)
                                  plt.ylabel("ψ(Degree)",fontsize=5)
                                  plt.xticks(np.arange(-180, 180, step=60),fontsize=5)
                                  plt.yticks(np.arange(-180, 180, step=60),fontsize=5)
                                  #plt.subplots_adjust(top = 0.99, bottom=0.01, hspace=1.5, wspace=0.4)
                                  #fig.tight_layout(h_pad=5, w_pad=5).
                                  #fig.text(0.5, 0.04, 'Total Residues - '+str(TotalResidue)+' Favoured- '+str(CountResidueFavouredRegionStd)+'('+str(PerResidueDisallowedRegionStd)+'%)  Allowed '+str(CountResidueAllowedRegionStd)+'('+str(PerResidueAllowedRegionStd)+'%) Disallowed - '+str(CountResidueDisallowedRegionStd)+'('+str(PerResidueDisallowedRegionStd)+'%)',  ha='center',fontsize=4)
                                  #fig.text(0.5, 0.03,DisallowedResidueInfoStd, ha='center',fontsize=3,wrap=True)
                                  #fig.text(0.5, 0.02,'3D Ramachandran plot  Here, bar represent frequency of torsion angles.' , ha='center',fontsize=5,wrap=True)
                                  plt.savefig(OutPutDir+'/Plots/StdMapType3DGeneral_'+PlotName+'.'+PlotFileType,dpi=PlotResolutions)
                        
                        # except:
                        #     log.write('File not avilable \n');
                                  if CountTotalResidue > 0:
                                    # try:
                                        
                                        ResultTorsionAngles=MolProbitydfStandard
                                        ResultTorsionAngles['Region'] = ResultTorsionAngles['Region'].replace({0.0: 'Favoured', 0.02: 'Allowed', 0.03: 'Disallowed'})
                                        # ResultTorsionAngles['MolprovityRegionG'] = ResultTorsionAngles['MolprovityRegionG'].replace({0.0: 'Favoured', 0.02: 'Allowed', 0.03: 'Disallowed'})
                                        ResultTorsionAngles.rename(columns = {'Region':'RamaChandran Plot Region(Std)'}, inplace = True) 
                                        # ResultTorsionAngles.rename(columns = {'MolprovityRegionG':'RamaChandran Plot Region(Std)'}, inplace = True) 
                                        #.replace(0.00, 'Favoured',inplace=True)
                                        # ResultTorsionAngles.drop(['AID', 'Isomer'], axis=1)
                                        
                                        result_df = pd.concat([result_df,ResultTorsionAngles], ignore_index=True)
                                        result_df.to_csv(OutPutDir+'/ResultTorsionAngles.csv')
                                    # MolProbitydfStandard.to_csv(OutPutDir+'/Result.csv')
                    except:
                        log.write('Unable to Calculate Torsion Angles \n')
        except:
              log.write('Unable to Extract PDB File from Trajectory \n');
    log.close()
    
def FunctionUserInputPhiPsiPlot(InputPath,OutPutDir,MapType,PlotResolutions,PlotFileType):
    
    import pandas as pd
    import csv
    import matplotlib.pyplot as plt
    import numpy as np
    
    def ramachandran_type_Gly_Non_Gly(residue) :
        if residue.upper()=="GLY" :
            return "Gly"
        else:
            return "General"
    
    isExist = os.path.exists(OutPutDir)
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(OutPutDir)
    isExist = os.path.exists(OutPutDir+'/Plots')
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(OutPutDir+'/Plots')
    log=open(OutPutDir+'/log.dat', 'a')
    log.write('InSIde TorsionAngleCalculation  '+ MapType+' \n')
    PlotResolutions=int(PlotResolutions)
    try:
        CustomData = pd.read_csv(InputPath)
        InputColName=list(CustomData.columns)
        MolProbitydfStandard = pd.DataFrame(columns=['PDBID','Chain','Residue','ResidueNo', 'PHI', 'PSI','Region','Group'])
        try:
            PDBID=CustomData[CustomData.columns[0]]
            Chain=CustomData[CustomData.columns[1]]
            Residue=CustomData[CustomData.columns[2]]
            ResidueNo=CustomData[CustomData.columns[3]]
            PHI=CustomData[CustomData.columns[4]]
            PSI=CustomData[CustomData.columns[5]]
            ln=len(PHI)
            MolprovityDataPath=pkg_resources.resource_filename('ramplot',"RamBoundry/MolprovityAllRegionGeneral.csv")
            MolprovityData = pd.read_csv(MolprovityDataPath)
            MolprovityPHI=MolprovityData['MolprovityPHI']
            MolprovityPSI=MolprovityData['MolprovityPSI']
            for x in range(ln):
                    InputPHI=int(PHI[x])
                    InputPSI=int(PSI[x])
                    IndexListofPHI = MolprovityData.index[MolprovityData['MolprovityPHI'] == InputPHI].tolist()
                    for i in IndexListofPHI:
                        if MolprovityData['MolprovityPSI'][i]==InputPSI:
                            # print(MolprovityData['MolprovityPSI'][i])
                            MolprovityRegionG=MolprovityData['MolprovityRegion'][i]
                            Group=ramachandran_type_Gly_Non_Gly(Residue[x])
                            rows=[PDBID[x],Chain[x],Residue[x],ResidueNo[x],PHI[x],PSI[x],MolprovityRegionG,Group]
                            MolProbitydfStandard.loc[len(MolProbitydfStandard)] = rows
            # print(MolProbitydfStandard)

            print(MolProbitydfStandard)
            CountTotalResidue=len(MolProbitydfStandard.index)
            if  CountTotalResidue > 0:
                fileAnalysis=open(OutPutDir+'/Analysis.csv', 'a', newline='')
                Analysiswriter = csv.writer(fileAnalysis)
                # importing datetime module for now()
                import datetime
                # using now() to get current time
                current_time = datetime.datetime.now()
                Analysiswriter.writerow(['Ram Plot Analysis'])
                Analysiswriter.writerow([current_time])
            
                MolprovityRegionStd=MolProbitydfStandard['Region']
                RegionwiseStd=MolProbitydfStandard.groupby('Region')
                TotalResidue=len(MolprovityRegionStd)
                Analysiswriter.writerow(['Total Residue',TotalResidue])
                
                try:
                    ResidueFavouredRegionStd=RegionwiseStd.get_group(0.0).reset_index()
                    CountResidueFavouredRegionStd=len(ResidueFavouredRegionStd.index)
                    PerResidueFavouredRegionStd=round(CountResidueFavouredRegionStd*100/TotalResidue,3)
                except:
                    CountResidueFavouredRegionStd=0
                    PerResidueFavouredRegionStd=0
                try:
                    ResidueAllowedRegionStd=RegionwiseStd.get_group(0.02).reset_index()
                    CountResidueAllowedRegionStd=len(ResidueAllowedRegionStd.index)
                    PerResidueAllowedRegionStd=round(CountResidueAllowedRegionStd*100/TotalResidue,3)
                except:
                    CountResidueAllowedRegionStd=0
                    PerResidueAllowedRegionStd=0
                DisallowedResidueInfoStd=''
                try:   
                    ResidueDisallowedRegionStd=RegionwiseStd.get_group(0.03).reset_index() 
                    CountResidueDisallowedRegionStd=len(ResidueDisallowedRegionStd.index)
                    PerResidueDisallowedRegionStd=round(CountResidueDisallowedRegionStd*100/TotalResidue,3)
            
                    
                except:
                    CountResidueDisallowedRegionStd=0
                    ResidueDisallowedRegionStd=0
                    PerResidueDisallowedRegionStd=0
                Analysiswriter.writerow(['Ramachandran plot (Standard) statistics'])    
                Analysiswriter.writerow(['Favoured: ',CountResidueFavouredRegionStd,'('+str(PerResidueFavouredRegionStd)+'%)'])
                Analysiswriter.writerow(['Allowed: ',CountResidueAllowedRegionStd,'('+str(PerResidueAllowedRegionStd)+'%)'])
                Analysiswriter.writerow(['Disallowed: ',CountResidueDisallowedRegionStd,'('+str(PerResidueDisallowedRegionStd)+'%)'])
                if CountResidueDisallowedRegionStd >=0:
                    Analysiswriter.writerow(['Disallowed Residues'])
                    Analysiswriter.writerow(['SN.','PDB ID','Chain','Residue','Residue No','PHI','PSI'])
                    for i in range(CountResidueDisallowedRegionStd):
                        Analysiswriter.writerow([str(i+1)+'. ',ResidueDisallowedRegionStd['PDBID'][i], ResidueDisallowedRegionStd['Chain'][i],ResidueDisallowedRegionStd['Residue'][i],ResidueDisallowedRegionStd['ResidueNo'][i],round(ResidueDisallowedRegionStd['PHI'][i],2),round(ResidueDisallowedRegionStd['PSI'][i],2)])
                        DisallowedResiduesStd=str(i+1)+'. '+ResidueDisallowedRegionStd['PDBID'][i]+' Chain: '+ ResidueDisallowedRegionStd['Chain'][i]+' '+ ResidueDisallowedRegionStd['Residue'][i]+ str(ResidueDisallowedRegionStd['ResidueNo'][i])+'PHI: '+ str(round(ResidueDisallowedRegionStd['PHI'][i],2))+' PSI: '+ str(round(ResidueDisallowedRegionStd['PSI'][i],2))
                        DisallowedResidueInfoStd=DisallowedResidueInfoStd+DisallowedResiduesStd+','
                        print(DisallowedResiduesStd)     
                
                fileAnalysis.close()
                print(ResidueDisallowedRegionStd)
            else:
                print('No Valid Residues Found')
                log.write('No Valid Residues Found')               
            if 'MapType2DStd' in MapType and CountTotalResidue > 0:
                    fig, ax = plt.subplots(figsize=(6,6))
                    MolprovityDataPath=pkg_resources.resource_filename('ramplot',"RamBoundry/MolprovityAllRegionGeneral.csv")
                    CountourDataMol = pd.read_csv(MolprovityDataPath)
                    CountourDfMol = pd.DataFrame(CountourDataMol)
                    x_list=np.unique(CountourDfMol['MolprovityPHI'].to_numpy())
                    y_list=np.unique(CountourDfMol['MolprovityPSI'].to_numpy())
                    X, Y = np.meshgrid(x_list, y_list)
                    Z=CountourDataMol.pivot(index='MolprovityPSI',columns='MolprovityPHI',values='MolprovityRegion')
                    ax.contour(X, Y, Z,linewidths=0.2)
                    #colors=['deepskyblue','aqua','red'],
                    ax.set_aspect(1)
                    gdCountourGroup = MolProbitydfStandard.groupby('Group')
                    keysCountourGroup = gdCountourGroup.groups.keys()
                    for keyCountourGroup in keysCountourGroup:    
                        GroupRegionDf=gdCountourGroup.get_group(keyCountourGroup).reset_index()
                        gdCountourRegion = GroupRegionDf.groupby('Region')
                            # extract keys from groups ,
                        if keyCountourGroup=='General':
                            keysCountourRegion = gdCountourRegion.groups.keys()
                            #print(keysCountourRegion)
                            for keyCountourRegion in keysCountourRegion:
                                RegionDf=gdCountourRegion.get_group(keyCountourRegion).reset_index()
                                x1=RegionDf['PHI']
                                y1=RegionDf['PSI']
                                if keyCountourRegion==0:
                                    ax.scatter(x1, y1, c='springgreen',s=5)
                                if keyCountourRegion==0.02:
                                    ax.scatter(x1, y1, c='blue',s=5)
                                if keyCountourRegion==0.03:
                                    ax.scatter(x1, y1, c='red',s=5)
                        if keyCountourGroup=='Gly':
                            keysCountourRegion = gdCountourRegion.groups.keys()
                            #print(keysCountourRegion)
                            for keyCountourRegion in keysCountourRegion:
                                RegionDf=gdCountourRegion.get_group(keyCountourRegion).reset_index()
                                x1=RegionDf['PHI']
                                y1=RegionDf['PSI']
                                if keyCountourRegion==0:
                                    ax.scatter(x1, y1,marker='^',c='springgreen',s=5)
                                if keyCountourRegion==0.02:
                                    ax.scatter(x1, y1,marker='^',c='blue',s=5)
                                if keyCountourRegion==0.03:
                                    ax.scatter(x1, y1, marker='^',c='red',s=5)
            
                    ax.set_xlim(-180, 180)
                    ax.set_ylim(-180, 180)
                    #ax.set_title('Ramachandran Plot',fontdict ={'weight':'bold'})
                    ax.set_xlabel("φ((Degree)",fontsize=5)
                    ax.set_ylabel("ψ(Degree)",fontsize=5)
                    ax.set_xticks(np.arange(-180, 181, step=60))  # Set x-axis ticks
                    ax.set_yticks(np.arange(-180, 181, step=60))   # Set y-axis ticks
            
                    #ax.set_title(GroupsCountour,fontdict ={'size':10})
                    ax.tick_params(direction='out', length=2,  colors='r',
                       grid_color='r', grid_alpha=0.5,labelsize=5)
                    #plt.tight_layout()
                    #fig.text(0.5, 0.04, 'Total Residues - '+str(TotalResidue)+' Favoured- '+str(CountResidueFavouredRegionStd)+'('+str(PerResidueDisallowedRegionStd)+'%)  Allowed '+str(CountResidueAllowedRegionStd)+'('+str(PerResidueAllowedRegionStd)+'%) Disallowed - '+str(CountResidueDisallowedRegionStd)+'('+str(PerResidueDisallowedRegionStd)+'%)',  ha='center',fontsize=4)
                    #fig.text(0.5, 0.03,DisallowedResidueInfoStd, ha='center',fontsize=3,wrap=True)
                    #fig.text(0.5, 0.02,'2D Ramachandran plot  Here, green, blue  and red dots represent torsion angles of favoured , allowed and disallowed regions residues other than glycine.Glycine Reside Represent in green,  blue and red  triangles', ha='center',fontsize=5,wrap=True)
                   
                    plt.savefig(OutPutDir+'/Plots/StdMapType2DGeneralGly.'+PlotFileType,dpi=PlotResolutions)
            if 'MapType3DStd' in MapType and CountTotalResidue > 0:
                  fig = plt.figure(figsize=(6,6))
                  #fig.tight_layout()
                  
                  ax3 = fig.add_subplot(1,1,1, projection='3d')
                  #ax1.plot_surface(X, Y, Z, lw=0.1, cmap='coolwarm', edgecolor='k')
                  GroupsCountourDataframe2=MolProbitydfStandard
                  GroupsCountourDataframe2['PHI'] = GroupsCountourDataframe2['PHI'].astype(int)
                  GroupsCountourDataframe2['PSI'] = GroupsCountourDataframe2['PSI'].astype(int)
                  ac=GroupsCountourDataframe2.groupby(["PHI", "PSI"]).size().reset_index(name='Count')
                  phi=ac['PHI'].tolist()
                  psi=ac['PSI'].tolist()
                  count=ac['Count'].tolist()
            
                  xpi=len(phi)
                  x3 = phi
                  y3 = psi
                  z3 = np.zeros(xpi)
                  dx = np.ones(xpi)
                  dy = np.ones(xpi)
                  dz = count
                  cmap = plt.get_cmap('viridis') # Get desired colormap - you can change this!
                  max_height = np.max(dz)   # get range of colorbars so we can normalize
                  min_height = np.min(dz)
                  rgba = [cmap((k-min_height)/max_height) for k in dz]
            
                  colourMap = plt.cm.ScalarMappable(cmap=plt.cm.gist_earth)
                  colourMap.set_array(dz)
                  MolprovityDataPath=pkg_resources.resource_filename('ramplot',"RamBoundry/MolprovityAllRegionGeneral.csv")
                  CountourDataMol = pd.read_csv(MolprovityDataPath)
                  CountourDfMol = pd.DataFrame(CountourDataMol)
                  x_list=np.unique(CountourDfMol['MolprovityPHI'].to_numpy())
                  y_list=np.unique(CountourDfMol['MolprovityPSI'].to_numpy())
                  X, Y = np.meshgrid(x_list, y_list)
                  Z=CountourDataMol.pivot(index='MolprovityPSI',columns='MolprovityPHI',values='MolprovityRegion')
                  ax3.contour(X, Y, Z,linewidths=0.2)
                  #colors=['deepskyblue','aqua','red'],
                  ax3.bar3d(x3, y3, z3, dx, dy, dz, color=rgba, zsort='average')
                  ax3.grid(False)
                  ax3.set_xlim(-180, 180)
                  ax3.set_ylim(-180, 180)
                  ax3.set_zlabel('Frequency',fontsize=5)
                  #ax3.tick_params('z', labelsize=font['size'])
                  ax3.view_init(elev=45)
                  #plt.title(GroupsCountour,fontdict ={'family':'DejaVu Sans','size':10,'weight':'bold'})
                  plt.xlabel("φ((Degree)",fontsize=5)
                  plt.ylabel("ψ(Degree)",fontsize=5)
                  plt.xticks(np.arange(-180, 180, step=60),fontsize=5)
                  plt.yticks(np.arange(-180, 180, step=60),fontsize=5)
                  #plt.subplots_adjust(top = 0.99, bottom=0.01, hspace=1.5, wspace=0.4)
                  #fig.tight_layout(h_pad=5, w_pad=5).
                  #fig.text(0.5, 0.04, 'Total Residues - '+str(TotalResidue)+' Favoured- '+str(CountResidueFavouredRegionStd)+'('+str(PerResidueDisallowedRegionStd)+'%)  Allowed '+str(CountResidueAllowedRegionStd)+'('+str(PerResidueAllowedRegionStd)+'%) Disallowed - '+str(CountResidueDisallowedRegionStd)+'('+str(PerResidueDisallowedRegionStd)+'%)',  ha='center',fontsize=4)
                  #fig.text(0.5, 0.03,DisallowedResidueInfoStd, ha='center',fontsize=3,wrap=True)
                  #fig.text(0.5, 0.02,'3D Ramachandran plot  Here, bar represent frequency of torsion angles.' , ha='center',fontsize=5,wrap=True)
                  plt.savefig(OutPutDir+'/Plots/StdMapType3DGeneral.'+PlotFileType,dpi=PlotResolutions)
        except:
             log.write('Custom file structure not same as sample file \n');
    except:
        log.write('File not avilable \n');
    if CountTotalResidue > 0:
        try:
            ResultTorsionAngles=MolProbitydfStandard
            ResultTorsionAngles['Region'] = ResultTorsionAngles['Region'].replace({0.0: 'Favoured', 0.02: 'Allowed', 0.03: 'Disallowed'})
            # ResultTorsionAngles['MolprovityRegionG'] = ResultTorsionAngles['MolprovityRegionG'].replace({0.0: 'Favoured', 0.02: 'Allowed', 0.03: 'Disallowed'})
            ResultTorsionAngles.rename(columns = {'Region':'RamaChandran Plot Region(Std)'}, inplace = True) 
            # ResultTorsionAngles.rename(columns = {'MolprovityRegionG':'RamaChandran Plot Region(Std)'}, inplace = True) 
            #.replace(0.00, 'Favoured',inplace=True)
            # ResultTorsionAngles.drop(['AID', 'Isomer'], axis=1)
            ResultTorsionAngles.to_csv(OutPutDir+'/ResultTorsionAngles.csv')
            # MolProbitydfStandard.to_csv(OutPutDir+'/Result.csv')
        except:
            log.write('Error unable to genrate ResultTorsionAngles.csv')

    log.close()
# JobID='RamPlot66a4e246328b9' 
# MapType=['MapType2DStd','MapType2DAll','MapType3DStd','MapType3DAll']
# InputResidues=['A101','A104']
# PlotResolutions=600
# PlotFileType='png'
# FunctionUserTrajectoryInputPhiPsiPlot(JobID,MapType,InputResidues,PlotResolutions,PlotFileType)

