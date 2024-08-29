# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 15:58:31 2024

@author: mayank
"""

# # my_package/cli.py

# import argparse
# from ramplot import TorsionAngleCalculation
# from ramplot import FunctionUserTrajectoryInputPhiPsiPlot
# def main():
#     parser = argparse.ArgumentParser(description="A CLI tool for processing data.")
#     parser.add_argument('-i', '--input', required=True, help="Input PDB Folder Path")
#     parser.add_argument('-m', '--MapType', required=True, help="Specify Map Types ")
#     parser.add_argument('-r', '--Resolutions', required=True, help="Specify Resolutions of Map Types ")
#     parser.add_argument('-p', '--PlotFileType', required=True, help="Specify Resolutions of Map TypesPlotFileType like png jpeg")
#     parser.add_argument('-o', '--Output', required=True, help="Specify Output Directory")
#     args = parser.parse_args()    
#     result = TorsionAngleCalculation(args.input,args.Output,args.MapType,args.Resolutions,args.PlotFileType)
#     print(result)
#     result =FunctionUserTrajectoryInputPhiPsiPlot(InputTPRFilePath,InputXTCFilePath,OutPutDir,InputResidues,FrameInterval,MapType,PlotResolutions,PlotFileType)
    
# if __name__ == "__main__":
#     main()
    
    
    
# my_package/cli.py

import argparse
from ramplot import TorsionAngleCalculation
from ramplot import FunctionUserTrajectoryInputPhiPsiPlot
from ramplot import FunctionUserInputPhiPsiPlot

def main():
    parser = argparse.ArgumentParser(description="Ramplot")
    
    # Common arguments
    parser.add_argument('-v', '--verbose', action='store_true', help="Increase output verbosity")
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Subcommand for function_a
    parser_pdb = subparsers.add_parser('pdb', help='Run Ramachandran Plot Using PDB Files')
    parser_pdb.add_argument('-i', '--input', required=True, help="Input PDB Folder Path")
    parser_pdb.add_argument('-m', '--MapType', required=True, help="Specify Map Types ")
    parser_pdb.add_argument('-r', '--Resolutions', default=600,  help="Specify Resolutions of Map Types ")
    parser_pdb.add_argument('-p', '--PlotFileType',default='png',  help="Specify Resolutions of Map TypesPlotFileType like png jpeg")
    parser_pdb.add_argument('-o', '--Output', required=True, help="Specify Output Directory")
    
    # Subcommand for function_b
    parser_trajectory = subparsers.add_parser('trajectory', help='Analysis of residue trajectory')
    parser_trajectory.add_argument('-t', '--InputTPR', required=True, help="Input TPR File Path")
    parser_trajectory.add_argument('-x', '--InputXTC', required=True, help="Input  XTC File  Path")
    parser_trajectory.add_argument('-m', '--MapType', required=True, help="Specify Map Types ")
    parser_trajectory.add_argument('-r', '--Resolutions', default='600',required=True, help="Specify Resolutions of Map Types ")
    parser_trajectory.add_argument('-p', '--PlotFileType', default='png',required=True, help="Specify Resolutions of Map TypesPlotFileType like png jpeg")
    parser_trajectory.add_argument('-c', '--InputResidues', required=True, help="Specify Input Residie like ChainResidueNo A101")
    parser_trajectory.add_argument('-f', '--FrameInterval',default='20', required=True, help="Specify Frame Interval")
    parser_trajectory.add_argument('-o', '--Output', required=True, help="Specify Output Directory")
    
    
    #Custom Torsion angle Plot 
    parser_Custom_Torsion_Angle = subparsers.add_parser('TorsionAngle', help='Run Ramachandran Plot Using Custom Torsion Angle CSV File')
    parser_Custom_Torsion_Angle.add_argument('-i', '--input', required=True, help="Input Custom Torsion Angle CSV File Path")
    parser_Custom_Torsion_Angle.add_argument('-m', '--MapType', required=True, help="Specify Map Types ")
    parser_Custom_Torsion_Angle.add_argument('-r', '--Resolutions', default=600, required=True, help="Specify Resolutions of Map Types ")
    parser_Custom_Torsion_Angle.add_argument('-p', '--PlotFileType',default='png', required=True, help="Specify Resolutions of Map TypesPlotFileType like png jpeg")
    parser_Custom_Torsion_Angle.add_argument('-o', '--Output', required=True, help="Specify Output Directory")
    # Parse the arguments
    args = parser.parse_args()

    # Dispatch the appropriate function based on the subcommand
    if args.command == 'pdb':
        result = TorsionAngleCalculation(args.input,args.Output,args.MapType,args.Resolutions,args.PlotFileType)
        # result = function_a(args.input, args.verbose)
    elif args.command == 'trajectory':
        result =FunctionUserTrajectoryInputPhiPsiPlot(args.InputTPR,args.InputXTC,args.Output,args.InputResidues,args.FrameInterval,args.MapType,args.Resolutions,args.PlotFileType)
    elif args.command == 'TorsionAngle':
        result =FunctionUserInputPhiPsiPlot(args.input,args.Output,args.MapType,args.Resolutions,args.PlotFileType)
    else:
        parser.print_help()
        return

    print(result)

if __name__ == "__main__":
    main()
