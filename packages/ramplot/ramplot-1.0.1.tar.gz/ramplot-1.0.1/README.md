# Ramplot

## Overview

`Ramplot` is a tool designed for generating and visualizing Ramachandran plots, which are essential for analyzing the phi (ϕ) and psi (ψ) torsion angles of the amino acid residues in protein structures. This tool helps in identifying allowed and disallowed regions of conformational space and is widely used in structural biology and bioinformatics.

## Features

- **Ramachandran Plots:** Generate high-quality, 3D & 2D Ramachandran plots for protein structure analysis.
- **Multiple Input Formats:** Supports various input  such as `PDB`, `Trajectory File`, and `Custom Torsion ANgle`.
- **Export Options:** Export plots in various formats like PNG, SVG, and PDF for publication or further analysis.
- **Integration with Pip/Conda:** Easy installation via pip and conda package managers.

## Installation

You can install `Ramplot` using pip or conda.

### Using pip

```bash
pip install ramplot

conda install ramplot 

Example Commands
ramplot TorsionAngle -i "CustomTorsionAngles.csv" -m MapType=['MapType2DStd','MapType2DAll','MapType3DStd','MapType3DAll'] -r 600 -p png -o Test



Ramplot README file
=====================

The Ramplot Project is  freely available Python tools for Ramachandran Plot.





The Ramplot package is open source software made available under generous
terms. 



Mayank Kumar & R.S. Rathore, RamPlot: an utility to draw 2D, 3D and assorted Ramachandran steric maps.


For the impatient
=================




Python Requirements
===================

We currently recommend using Python 3.11 from http://www.python.org

Biopython is currently supported and tested on the following Python
implementations:

- Python 3.9, 3.10, 3.11 and 3.12 -- see http://www.python.org

- PyPy3.9 v7.3.13 -- or later, see http://www.pypy.org


Dependencies
=====================

Ramplot requires 
 'numpy','pandas','biopython','matplotlib','mdanalysis','pytest-shutil' 
.

