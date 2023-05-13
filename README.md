# Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
  - [Windows Install Guide](#windows-install-guide)
  - [Mac OS X Install Guide](#os-x-install-guide)
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
Download and install Python: [https://www.python.org/downloads/](https://www.python.org/downloads/) 

For detailed information about the Python installation process: [https://docs.python.org/3/using/windows.html](https://docs.python.org/3/using/windows.html)  

##### 2. Download and unzip project folder from GitHub
Click the green code button and select “Download ZIP”: [https://github.com/matthewpittendreigh/planarachrome](https://github.com/matthewpittendreigh/planarachrome)
Double click on the downloaded file to unzip it and move the unzipped folder to your desired location.

##### 3. Open terminal
*To configure the project and install its dependencies, use the terminal associated with the Windows operating system (PowerShell):*

Open the terminal. If you do not know how to do this, press the Windows key to access the Windows search box and then type “powershell”. Run Windows PowerShell.

##### 4. Change working directory
*Utilize the “cd” or change directory command in terminal to perform operations within the downloaded project folder (specifically, the root folder for the project, or the folder directly containing the file “planarachrome.py”:*

Method 1 – Navigate to the project folder in Finder. Type `cd` followed by a single space in the terminal, and then drag and drop the project folder into the terminal window. This will paste the folder’s path.

Method 2 – Navigate to the project folder in file explorer. Left click the path bar at the top of the window to obtain the folder path. Type `cd` followed by a single space in the terminal, and then copy and paste the path to complete the command.

Example:
```cd C:\Users\YourUserName\Desktop\planarachrome```

Press enter to run the command.

##### 5. Create virtual environment
*To create a virtual environment (a container for Python packages, storing everything the project needs):*

Ensure pip (the Python package index) is up to date by running the command:
```py -m pip install --upgrade pip```

Then create the virtual environment by running the command:
```py -m venv env```

##### 6. Activate virtual environment
*After creating the virtual environment, activate it before installing any of the project requirements:*

Run the command:
```.\env\Scripts\activate```

##### 7. Install project dependencies
Run the command:
```py -m pip install -r requirements.txt```

*This may take 5+ minutes.*

##### 8. Run the project
Run the command:
```py ./planarachrome.py```

Python should now be hosting a local server that is running the web application. To use it, visit your local host at the following link: http://127.0.0.1:5000/.


To run the project after the initial installation process, repeat steps 3, 4, 6, and 8


## OS X Install Guide
##### 1. Install python
Download and install Python: [https://www.python.org/downloads/](https://www.python.org/downloads/) 

For detailed information about the Python installation process: [https://docs.python.org/3/using/windows.html](https://docs.python.org/3/using/windows.html) 

##### 2. Download and unzip project folder from GitHub
Click the green code button and select “Download ZIP”: [https://github.com/matthewpittendreigh/planarachrome](https://github.com/matthewpittendreigh/planarachrome)
Double click on the downloaded file to unzip it and move the unzipped folder to your desired location.

##### 3. Open terminal
*To configure the project and install its dependencies, use the terminal associated with the OS X operating system (Terminal):*

Open the terminal. If you do not know how to do this, Command + Space will open spotlight. Search for “terminal” and double click to open.

##### 4. Change working directory
*Utilize the “cd” or change directory command in terminal to perform operations within the downloaded project folder (specifically, the root folder for the project, or the folder directly containing the file “planarachrome.py”:*

Method 1 – Navigate to the project folder in Finder. Type `cd` followed by a single space in the terminal, and then drag and drop the project folder into the terminal window. This will paste the folder’s path.

Method 2 – Navigate to the project folder in Finder and control click the folder > Get Info. This will display the folder path (see “Where” under the “General” heading). Type `cd` followed by a single space in the terminal, and then copy and paste the path to complete the command.

Example:
```
cd ~/Desktop/planarachrome
cd /Users/YourUserName/Desktop/planarachrome
```

Press enter to run the command.

##### 5. Create virtual environment
*To create a virtual environment (a container for Python packages, storing everything the project needs):*

Ensure pip (the Python package index) is up to date by running the command:
```python3 -m pip install --user --upgrade pip```

Then create the virtual environment by running the command:
```python3 -m venv env```

##### 6. Activate virtual environment
*After creating the virtual environment, activate it before installing any of the project requirements:*

Run the command:
```source env/bin/activate```

##### 7. Install project dependencies
Run the command:
```python3 -m pip install -r requirements.txt```

*This may take 5+ minutes.*

##### 8. Run the project
Run the command:
```python3 ./planarachrome.py```

Python should now be hosting a local server that is running the web application. To use it, visit your local host at the following link: http://127.0.0.1:5000/.


For running the project after the initial installation process, repeat steps 3, 4, 6, and 8


# More Info
For more information about planarian research at KSC: https://www.pellettierilab.com/


# Contact


[top](#table-of-contents) 