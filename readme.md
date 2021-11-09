# Overview
Blender is a power powerful 3D objects editor which provides a very easy to use interface for refining 3D models. It has a very comprehensive and well documented API which can be used for enhancing its features programatically. This work demonstrates how to utilize its API to find contact nodes between two irregular surfaces. This work was carried out after built in mesh assembly features of [Salome Meca][1] and [Code Aster][2] raised singularity errors. It was deduced that it is because of non coincident irregular surface nodes. This problem was resolved by generating contact groups on the irregular surfaces in Blender which was used to directed Code Aster to form contact exactly where it needs.

# Prerequisites
Basic knowledge of Blender menus and selection

# Quick Start

## Requirement
Blender's python would need pandas library which can be installed in the following way

- Open 'Python Console' which is part of 'Editor Type' menu
- Execute the following to get Blender's python path
```
>>> import sys
>>> sys.exec_prefix
'/path/to/blender/python'
```

- Next from the terminal
```
cd /path/to/blender/python/bin
./python -m ensurepip
./python -m pip install pandas
```

- Restart Blender

## Running the Script
- Import sample STL files (L5, disk)
- Select both imported objects from the 'Outliner' in the 'Editor Type' menu
- Open 'Text Editor' in the 'Editor Type' menu
- From the 'Text Editor' menu click 'Text > Create Text Block'
- Copy paste the code from 'contact.py'
- While keeping the mouse pointer inside 'Text Editor' press 'Ctrl + p'

Contact vertex groups will be generated. Vertex groups can be viewed in 'Data' type property of 'Properties' type editor in 'Editor Type' menu

# Basic Algorithm Detail
## The `samplesize` Parameter
This parameter in the only directive set by the user which the script needs to identify contact between two irregular surfaces

- It is the number of least distant nodes between the two surfaces 
- The distance of the most distant node among these nodes is the threshold 
- All nodes with distances less than threshold are qualified as contact nodes

# Next Step
- Utilize Gmsh API to mesh the objects while preserving vertex groups

# Reference 

[Blender: Using 3rd party Python modules](https://blender.stackexchange.com/a/122337)

[Euclidean distance](https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy)

[Minimum Euclidean Distance](https://stackoverflow.com/questions/1871536/minimum-euclidean-distance-between-points-in-two-different-numpy-arrays-not-wit)

[1]: https://www.code-aster.org/spip.php?article303

[2]: https://www.code-aster.org/spip.php?rubrique2