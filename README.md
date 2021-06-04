# Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
  - [Windows Install Guide](#windows-install-guide)
  - [OS X Install Guide](#os-x-install-guide)
- [More Info](#more-info)
- [Contact](#contact)


# Introduction

The colors of life are imparted by diverse biological pigments, often produced by specialized pigment cells. In many organisms, pigmentation can change in response to both internal and external cues. The ability to quantify such changes represents a useful experimental tool for researchers studying pigment genetics, biochemistry, and cell biology.

This program was developed in order to quantify relative pigment levels in brown, aquatic flatworms called planarians. Images of live animals captured with a microscope and digital camera can be processed in a high-throughput manner to determine relative pigment intensity and the percentage of the visible surface area that is pigmented. While information on absolute pigment levels is not provided, this unbiased, relative quantification approach can offer insight into how pigmentation changes within a given group of animals over time, or when different groups of animals are subjected to different experimental conditions. Although the program was developed for planarians, it may also be useful for quantifying relative pigment levels in other organisms.

Image acquisition protocols are not discussed here and will vary based upon users’ available equipment and goals. The program is designed to operate with any RGB images having a background that is darker than the animal to be analyzed. Accepted file formats are .tif and .png. It is imperative that variables such as lighting, exposure time, and camera settings be constant within any given experiment. Nonlinear (i.e. gamma) image adjustments must be avoided. If linear (brightness and contrast) adjustments are necessary, they should be applied evenly across all images before processing.


# Installation

PlanaraChrome is a Python web application. The detailed instructions below explain the process for installing Python on your operating system and running the app using Terminal and any web browser as a user interface. Experienced Python users can skip directly to Step 2 for their operating system.

## Windows Install Guide
##### 1. Install python
Download and install python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/) 

For detailed information about the python installation process: [https://docs.python.org/3/using/windows.html](https://docs.python.org/3/using/windows.html)  

##### 2. Download and unzip project folder from GitHub
Click the green code button and select download ZIP: [https://github.com/matthewpittendreigh/planarachrome](https://github.com/matthewpittendreigh/planarachrome)

##### 3. Open terminal
*We will begin to configure the Planarian project and install its dependencies. To do this we will use the terminal associated with your operating system. For windows we’ll use PowerShell.*

Open the terminal. If you do not know how to do this, press the windows key to access the windows search box then type powershell. Run Windows PowerShell.

##### 4. Change working directory
*We need to tell the terminal that we would like to do operations within the downloaded project folder. To do this, will utilize the ‘cd’ or change directory command.*
*Note: The specific folder we need to change to is the root folder of the project, otherwise described as the folder directly containing the file ‘planarachrome.py’.*

Method 1 – Navigate to the project folder in Finder. Type cd in the terminal then drag and drop the project folder into the terminal window. This should paste its path. 

Method 2 – Navigate to the project folder in your file explorer. Left click the path bar at the top of the window. It should convert to a folder path. You can then copy and paste that to complete the command.

Example:
cd C:\Users\YourUserName\Desktop\planarachrome

If you have not done so, press enter to run the command.

##### 5. Create virtual environment
*A virtual environment is a container for python packages, created such that everything the project needs is contained within the project folder.*

Ensure pip (the python package index) is up to date by running the following command,
py -m pip install --upgrade pip

Then create the virtual environment,
py -m venv env

##### 6. Activate virtual environment
*Once the virtual environment is created, we need to activate it before installing any of the project requirements.*

Run command to activate,
.\env\Scripts\activate

##### 7. Install project dependencies
Run the command,
py -m pip install -r requirements.txt

*This may take a few minutes.*

##### 8. Run the project
Run the command,
py ./planarachrome.py

Python should now be hosting a local server that is running the web application. To use it, visit your local host at this link http://127.0.0.1:5000/.


For running the project after the initial installation process, repeat steps 4, 6, and 8


## OS X Install Guide
##### 1. Install python
Download and install python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/) 

For detailed information about the python installation process: [https://docs.python.org/3/using/windows.html](https://docs.python.org/3/using/windows.html)  

##### 2. Download and unzip project folder from GitHub
Click the green code button and select download ZIP: [https://github.com/matthewpittendreigh/planarachrome](https://github.com/matthewpittendreigh/planarachrome)

##### 3. Open terminal
*We will begin to configure the Planarian project and install its dependencies. To do this we will use the terminal associated with your operating system. For OS X it is simply called terminal.*

Open the Terminal. If you do not know how to do this, Command + Space will open your spotlight. Search for terminal and it should autocomplete.

##### 4. Change working directory
*We need to tell the terminal that we would like to do operations within the downloaded project folder. To do this, will utilize the ‘cd’ or change directory command.*
*Note: The specific folder we need to change to is the root folder of the project, otherwise described as the folder directly containing the file ‘planarachrome.py’.*

Method 1 – Navigate to the project folder in Finder. Type cd in the terminal then drag and drop the project folder into the terminal window. This should paste its path. 

Method 2 – Navigate to the project folder in Finder and right click the folder > Get Info. This should display the path which you can combine to create the command.

Example:
cd ~/Desktop/planarachrome
cd /Users/YourUserName/Desktop/planarachrome

If you have not done so, press enter to run the command.

##### 5. Create virtual environment
*A virtual environment is a container for python packages, created such that everything the project needs is contained within the project folder.*

Ensure pip (the python package index) is up to date by running the following command,
python3 -m pip install --user --upgrade pip

Then create the virtual environment,
python3 -m venv env

##### 6. Activate virtual environment
*Once the virtual environment is created, we need to activate it before installing any of the project requirements.*

Run command to activate,
source env/bin/activate

##### 7. Install project dependencies
Run the command,
python3 -m pip install -r requirements.txt

*This may take a few minutes.*

##### 8. Install project dependencies
Run the command,
python3 ./planarachrome.py

Python should now be hosting a local server that is running the web application. To use it, visit your local host at this link http://127.0.0.1:5000/.


For running the project after the initial installation process, repeat steps 4, 6, and 8


# More Info


# Contact


[top](#table-of-contents) 