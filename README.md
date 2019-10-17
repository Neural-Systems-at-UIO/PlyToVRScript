# PlyToVRScript
Description of project
- What it does
This script processes a set of models, at least one, stored in the parent folder provided by the GUI user. It automates tedious and standard tasks like smoothing, decimation and transformation of the models.
- What it produces
A sub folder containing the model meshes with encoded colours, if provided, in an FBX format for portability and ease of use. 
- Intended use
Converting common scientific or medical 3D file types to a VR friendly format and at a detail level fitting the target hardware.


Required
Pythn blah blah
The structure ID must be prepended to to the structure name, if an ID exists. 
Format: <Structure ID>-<Structure name>.<file type>  ->  Example: 041-Cortex.stl
Files stored on a local drive.


Accepted filetypes
['dae', 'stl', 'obj', 'fbx']


Source folder must contain at least one folder, where each folder is processed as an isolated model.
All files with an ending in the above set [dae, stl...] will be processed as one model if present in the same model folder. The script assumes exactly one '.txt' file for colour data. See colour section for more information. All other files or folders are ignored.


How to run
Launch python script directly by opening a commandline/terminal in the root folder and running the command 'python GUI/MainGUI.py'.
OR
Click on the executable file (.bat for Windows and .sh for Linux and MAC).

Fill in all values.
Select 'View model in Blender' if you want blender to automatically open. WARNING: Will increase runtime by several hundred percent.
Click run.
Check the points in the popup.
Click yes to run, or no to abort.
Wait for the process indicator stops moving.
Use result. (e.g. open the blender file in the model folder, copy the fbx folder with the processed models)


Executable file to start the GUI (One for windows: .bat, and one for linux/mac: .sh)
How to


Common errors
No models in folder/Incorrect source folder
Missing values
Numerical values entered with non-digit symbols
Text values entered without enclosing ''
Missing [] in lists
Period instead of comma used when dividing values in lists

Blender not found
Python not found
Script is corrupt
Colours are wrong


Glossery


Colour info
1. If a txt file is not present in the model folder the script will asign random colours to the model
2. If a txt file is present the script will try to parse the file and colour the model accordingly. If there is a missing or mismatched structure in the txt file the resulting colour will be grey.
3. If multiple txt files exist, the last one will be considered the true one and attempted used as in option 2.


Expert focused guidelines
File responsibility (What python file does what)


Licenses
Blender is open
This code is open
Source files might be restricted by a licence
