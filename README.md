# PlyToVRScript
Description of project
- What it does
This script processes a set of models, at least one, stored in the parent folder provided by the GUI user. It automates tedious and standard tasks like smoothing, decimation and transformation of the models.
- What it produces
A sub folder containing the model meshes with encoded colours, if provided, in an FBX format for portability and ease of use. 
- Intended use
Converting common scientific or medical 3D file types to a VR friendly format and at a detail level fitting the target hardware.


##Required
- Python 3.7
- Blender 2.8x
- The structure ID must be prepended to to the structure name, if an ID exists. 
    - Format: <Structure ID>-<Structure name>.<file type>  ->  Example: 041-Cortex.stl
- Files stored in the correct format: `[dae, stl, obj, fbx]`
- Source folder must contain at least one folder, where each folder is processed as an isolated model.
All files with an ending in the above set [dae, stl...] will be processed as one model if present in the same model folder.
The script assumes exactly one '.txt' file for colour data. See the [colour section](#colour-info) for more information. 
All other files or folders are ignored.


##How to run
There are two methods of launching the project:
1. Launch python script directly by opening a commandline/terminal in the root folder and running the command `python GUI/MainGUI.py`.
2. Click on the executable file (.bat for Windows and .sh for Linux and MAC).

##Using the GUI
1. Fill in all values that you want.
2. Select 'View model in Blender' if you want blender to automatically open. WARNING: Will increase runtime by several hundred percent.
3. Click run.
4. Check the points in the popup.
5. Click yes to run, or no to abort.
6. Wait for the process indicator stops moving.
7. Use result. (e.g. open the blender file in the model folder, copy the fbx folder with the processed models)


##Common errors
- No models in folder/Incorrect source folder
    - Make sure that the folder containing the source files has is correct and contains one subfolder for each model to process.
- Missing values
    - Make sure that the settings are correct and especially that 'Target Size' and 'File type to import' has the correct numbers and file types. 
- Numerical values entered with non-digit symbols
    - The allowed symbols are within the set `[0-9,]`
- Period instead of comma used when dividing values in lists
    - Period (.) is used for decimal numbers (e.g. 4.6), while comma (,) is used for separating values (e.g. 1, 2, 3).
- Colours are wrong
    - Refer to the below paragraph about [colour info](#colour-info)
- Blender not found
    - Install blender
- Python not found
    - Install Python 3.7
- Script is corrupt
    - Download the script anew from the repository



##Glossery


##Colour info
1. If a txt file is not present in the model folder the script will assign random colours to the model
2. If a txt file is present the script will try to parse the file and colour the model accordingly. If there is a missing or mismatched structure in the txt file the resulting colour will be grey.
3. If multiple txt files exist, the last one will be considered the true one and attempted used as in option 2.


##Expert focused guidelines
File responsibility (What python file does what)


##Licenses
- Blender is open source
- This code is open source
- Source files might be restricted by a licence
