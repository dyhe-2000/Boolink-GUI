Supplementary Text: A Graphical Interface for Asynchronous Simulation of Boolean Network
1. Installing BoolSim - Software Requirements (Windows)
BoolSim requires the GNU c++ compiler (called g++) and python installed on the user’s computer. Both the tools are freely available. The following steps run through the installation of the two programs.

Firstly, check if g++ is already installed on your computer. To do this, open the command prompt (right click on the start button and click on ‘command prompt’) and type ‘g++ --version’ without the quotes and hit Enter. BoolSim requires g++ version to be 6 or higher. If g++ is not installed, it displays an error . Once g++ is installed, we come back to this step to verify that the installation is proper and complete.
To install g++ we first install MinGW. Downloading and running this program installs the necessary compilers for us in a matter of a few clicks. 
This video runs through g++ installation using MinGW ( https://youtu.be/sXW2VLrQ3Bs ). Follow the steps as shown in the video. Here are some troubleshooting tips for this step:
Here is the URL to download MinGW if you need it. https://sourceforge.net/projects/mingw/
A different way to change environment variables on your system is to open system settings (right click on the start button and click on ‘System Settings’) and type ‘environment variables’ in the search bar of the system settings window.
After g++ installation is complete, go to step 1. If successful, your computer can now compile and run c++ programs.
Next, we install python. To check if python is already installed, type ‘python --version’ and hit Enter. BoolSim requires python3; if it is not installed, it displays an error . Once python is installed, we come back to this step to verify that the installation is proper and complete.
To install python on your Windows machine, follow the steps in this video: https://youtu.be/4Rx_JRkwAjY You may stop at 4:00 in this video once python is installed. Close the installer and go to step 5. You should be able to see python’s version (3.8 or higher) when you run python --version on cmd.
Next we install a few other python packages: numpy, matplotlib, pandas, and jupyter-notebook. Run these commands in the command prompt after python is installed:
pip install numpy
pip install matplotlib
pip install pandas
pip install jupyter-notebook
After the above packages are installed, you may check their version by trying the commands given the second screenshot below.
Good to go!
![alt text](https://github.com/dyhe-2000/BoolSim-GUI/instruction pictures/readyToGo1.JPG?raw=true)
![alt text](https://github.com/dyhe-2000/BoolSim-GUI/instruction pictures/readyToGo2.JPG?raw=true)


2. Downloading and Running BoolSim
Create a new folder on your computer where you want to run BoolSim. For example, D:\BoolSim_simulation\
Visit https://github.com/dyhe-2000/BoolSim-GUI.git for downloading the package. Click on the green button named Code and then click on Download ZIP in the dropdown. See the figure.
![alt text](https://github.com/dyhe-2000/BoolSim-GUI/instruction pictures/gotoGitHubAndDownload.JPG?raw=true) 
Save the zip file in the new folder you’ve just created. If the zip file is saved to the Downloads folder by default, cut and paste the zip file into the new folder.
Then open the new folder you created in File Explorer. Right click on the zip file and extract it at the current location.
To run BoolSim, we open the command prompt at the current location. To do that, follow one of these steps:
Press Shift and right click inside the folder. In the right-click (context) menu, click on ‘Open command window here’.
Select the address bar in the File Explorer by pressing Alt+D. Once the address is selected (D:\BoolSim_simulation\ for example), type ‘cmd’ and hit Enter.
In the command prompt, type ‘python BoolSim_Windows.py’ and hit Enter. A new window should pop up.
Click on ‘Agree’ to enter the start page of BoolSim. This is the home page of BoolSim. 
![alt text](https://github.com/dyhe-2000/BoolSim-GUI/instruction pictures/boolSimHomePage.JPG?raw=true) 
To simulate a boolean network on BoolSim, you need: a file containing the names and initial states of the nodes (called node-name-file); a file containing the update equations of the nodes (called equation-file). See Section 3 for steps to create these files, or how to use the files given for some pre-defined networks.
Before proceeding, make sure you have created or located a node-name-file and an equations-file pertaining to the boolean network you wish to simulate.
To define the nodes of the network, click Network ➝ Add Node (in the menu bar). Copy-paste the contents of the node-name-file into the text box in the pop-up menu titled ‘Adding Nodes’, and click on the ‘Add’ button. You may then close the pop-up menu.
To define the boolean equations of the network, you may choose to define the equations in the word format or the index format. 
To add equations in word format, click on Connections ➝ Add Eqns in Word Form. Copy-paste the contents of the equations-file (in word form) into the text box in the pop-up menu titled ‘Adding Eqns’, and click on the ‘Add’ button. You may then close the pop-up menu.
To add equations in index format, click on Connections ➝Add Eqns in Index Form. Copy-paste the contents of the equations-file (in index form) into the text box in the pop-up menu titled ‘Adding Eqns’, and click on the ‘Add’ button. You may then close the pop-up menu.
Click on the See Graphical Network button on the homepage to visualize the network. The circles representing the nodes can be moved around by dragging for ease of visualization. Green arrows denote activation while red arrows denote inhibition. Self-regulation, which can be either positive or negative, is shown by an arrow that is entirely within the node. An arrow begins from the top of the source node to the bottom of the target node. The arrowhead of each arrow is at the target node. Click Refresh to reset to the initial view, and Back to Home to return to the homepage.
Double-clicking on any node does a search of upstream and downstream nodes of the selected node. The node itself is colored in orange, its upstream nodes are colored in magenta, and the downstream nodes in cyan. Right-clicking on or dragging any of the highlighted nodes reverts it to the default yellow.
Before simulating the network, set the number of initial conditions by clicking on the ‘Set Simulation Initializations’ option on the menu bar. You may choose one of the options in the dropdown menu by clicking on them, or click on ‘Input arbitrary initializations’ to enter a (different) number into the dialog box. Click on the ‘Add’ button of the dialog box before closing it.
Set the number of time steps by clicking on the ‘Set Simulation Time Step’ option on the menu bar. You may choose one of the options in the dropdown menu by clicking on them, or click on ‘Input arbitrary time steps’ to enter a (different) number into the dialog box. Click on the ‘Add’ button of the dialog box before closing it.
Good to go! Click on the ‘Start Simulate Process’ button on the home page to run the simulation. This could take a few minutes. The button remains inactive while the simulation is running. Monitor the progress of the simulation on the command prompt window.
To visualize the average activity of a particular node(s), click ‘Set nodes to see their graphical result’➝ ‘set node’ on the menu bar. In a separate text file (you may use ‘scratch paper.txt’ in the main folder for this), type each node that you want to visualize in a new line. For example, if you are simulating the simple network, you may type ‘IN’, ‘X’, ‘Z’ (without quotes) in separate lines in the text file. Copy-paste these lines to the text box of the pop-up menu. Click on the ‘Add’ button on the pop-up menu and close it. Click on the ‘See graphical analysis from simulation’ button on the homepage. You will now see a plot and a warning dialog box. Close the warning dialog box and hit Refresh when the plot appears. The following figure shows an example plot. Click on the ‘Back to Home’ button to get back to the home page of BoolSim.
![alt text](https://github.com/dyhe-2000/BoolSim-GUI/instruction pictures/graphPage.JPG?raw=true) 
3. Preparing the Network
BoolSim package comes with text files containing node names and the update equations for a simple network and for stomatal closure networks mediated by ABA and ABA plus CO2. You may first simulate the ‘simple network’ to make sure everything is working fine before simulating the networks for stomatal closure driven by ABA, by ABA and CO2, or a new network designed by you. To simulate any boolean network on BoolSim, you need: a file containing the names and initial states of the nodes (called node-name-file); a file containing the update equations of the nodes (called equation-file). The node-name-file and equation-file for the predefined boolean networks are located in the sub-folders as listed below:

Folder containing the simple network: sample_data_files / simple_network_data_files
Node-name-file: sample_data_files / simple_network_data_files / simple_net_node_names.txt
Equation-file: sample_data_files / simple_network_data_files / simple_net_word_eqns.txt
Folder containing the ABA network: sample_data_files / ABA_data_files
Node-name-file: Node Name and their initial state with ABA.txt
Equation-file (you may use one of the two, the word format is recommended):
File with equations written in words: Boolean Equations in words with ABA.txt
File with equations written in indices: Boolean Equations in index with ABA.txt
Folder containing the ABA-CO2 network: sample_data_files / ABA_CO2_data_files
Node-name-file: Node Name and their initial state with CO2 branch.txt
Equation-file (you may use one of the two,  the word format is recommended):
File with equations written in words: Boolean Equations in words with ABA and CO2.txt
File with equations written in indices: Boolean Equations in index with ABA and CO2.txt

To define your own network, follow the steps below. You may refer to the given data files as an example and as a template.
3.1. Creating a node-name-file
First, create a folder inside sample_data_files to store the files pertaining to your new network. For example, create a folder ‘my_bool_network’ inside sample_data_files.
Open Notepad (or your favorite text editor) and save a new file in this directory. For example, save the new file as ‘node-name-file.txt’ in the ‘my_bool_network’ folder.
In your node-name-file, type the name of each node of your network in a separate line.
If the initial state of a node is to be fixed, instead of being assigned randomly, type the initial state (0 or 1) after a space following the name.
In the visualization of the network, if you want a node to be colored in a different color (yellow is the default color), type the color at the end of the line for that node. Available colors are purple, blue, green, yellow, orange, and red. 

For example, when a node named SLAC1 needs to be colored orange and if its initial state should be 0, you should type
SLAC1 0 orange
in the line containing SLAC1.

When a node named ROS is randomly initialised but needs to be colored blue in the visualization, you should type
ROS blue
in a new line.
The contents of this file will be copied into a dialog box. Save this file before closing.
Refer to the node-name-files of the pre-defined networks for examples.
3.2. Creating an equation-file
Create a new text file in Notepad (or your favorite text editor) and save it in the same directory as you did the node-name-file. For example, save this file as ‘equation_file.txt’ in the ‘my_bool_network’ folder.
Word format is recommended for the equation-file. The instructions given here are for the word format.
Each line in the equation-file contains an update equation for a node. It is recommended to type out the equations in the same order as they appear in node-name-file, though it is not compulsory. The equations should be in the format as described below. There is also a scratch paper.txt for formatting the input to the program. Also check the existing examples. 
On the left hand side (LHS), type the name of the node being updated. The names are case-sensitive, so they should be identical to the names in the file for node names.
The right hand side (RHS) should be written in the Sum of Products (SoP) form as described in the next section ‘A primer on Boolean Logic’
Look at the existing equation-files in word format for examples.
