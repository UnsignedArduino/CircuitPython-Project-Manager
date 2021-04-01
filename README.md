# CircuitPython-Project-Manager
A Python program that will copy files to a CircuitPython device, basically eliminating the risk of losing code from 
the CircuitPython drive being corrupted and allows for version-control systems!

> Problems? Please 
[file an issue](https://github.com/UnsignedArduino/CircuitPython-Project-Manager/issues/new) or even better, a pull 
request if you can fix it!

> Need help/don't understand something? Join the [Adafruit Discord server](http://adafru.it/discord) and ping @Ckyiu 
> on there!

> Note: If you are viewing this file offline, the HTML generated from this markdown isn't perfect. It is highly 
recommended that you view this file on 
[GitHub](https://github.com/UnsignedArduino/CircuitPython-Project-Manager/blob/main/README.md), as it has been tuned for 
GitHub-style markdown.

> Check out my other projects related to CircuitPython: (Oh look **shameless self-promotion** again)
> - [CircuitPython-Bundle-Manager](https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager): A Python program 
    that makes it easy to manage modules on a CircuitPython device!

> Note: As you can tell, the documentation is _definitely_ not finished. While I'm writing this documentation, you 
> can either wait for me to finish (not recommended) or ping me on Discord on the Discord server linked above. 
> (recommended)

## Table of Contents
1. [Installing](#installing)
   1. [Installing from source](#installing-from-source)

## Installing

Due to how new this project is, there are no binaries currently.  

### Installing from source

1. [Download](https://git-scm.com/downloads) and install Git. It does not matter what editor you use for Git's default.
    1. Or...download this repo via the `Download ZIP` option under the green `Code` button, shown in Figure 1.1:
    
    ![A picture on the Download Zip button on the GitHub page](assets/1/1.png)
    
2. [Download](https://www.python.org/downloads/) and install Python **3.9**. (Because I use type definitions, but 3.8 
   seems to work too)
    1. Make sure to check `Add Python 3.x to PATH`, as shown in Figure 1.2:
       
       ![A picture of the Python 3.9 installer with the Add Python 3.9 to PATH checkbox checked](assets/1/2.png)
       
    2. Make sure to also install Tk/Tcl support! If you can access the IDLE, then Tk/Tcl is installed, as shown in 
       Figure 1.3: (Only applies if you are using the `Customize installation` option in the installer)
       
       ![A picture of the Python 3.9 installer with the tcl/tk and IDLE checkbox checked](assets/1/3.png)
   
       If you are building Python,
       [here is a guide on building Python on Debian I found helpful](https://linuxize.com/post/how-to-install-python-3-8-on-debian-10/).
       Before building, you may need to install a bunch of packages using `apt`: 
       `sudo apt install libbz2-dev libgdbm-dev libgdbm-compat-dev liblzma-dev libsqlite3-dev libssl-dev uuid-dev libreadline-dev zlib1g-dev tk-dev libffi-dev`.
       
3. If you are on Windows, I would also install the 
   [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701) while you are at it.

4. If you installed Git, `cd` into a convenient directory (like the home directory or the desktop) and run:
    ```commandline
    git clone https://github.com/UnsignedArduino/CircuitPython-Project-Manager
    cd CircuitPython-Project-Manager
    ```
    1. If you downloaded the ZIP, move the downloaded ZIP to somewhere convenient (ex. home directory or desktop), 
       extract it, open a terminal and `cd` into the extracted directory.

5. If you run `dir` (or `ls -a` on Mac and Linux) you should get something like this:

    1. `dir` (Windows):
    
    ```commandline
    03/31/2021  04:49 PM    <DIR>          .
    03/31/2021  04:49 PM    <DIR>          ..
    03/31/2021  04:49 PM                33 .gitignore
    03/31/2021  04:49 PM    <DIR>          assets
    03/31/2021  04:49 PM    <DIR>          default_circuitpython_hierarchy
    03/31/2021  04:49 PM            59,538 gui.py
    03/31/2021  04:49 PM    <DIR>          gui_tools
    03/31/2021  04:49 PM               934 main.py
    03/31/2021  04:49 PM    <DIR>          project_tools
    03/31/2021  04:49 PM             3,674 README.md
    03/31/2021  04:49 PM                38 requirements.txt
    5 File(s)         64,217 bytes
    6 Dir(s)  39,622,823,936 bytes free
    ```

   2. `ls -a` (macOS and Linux):
    
    ```commandline
    .  ..  assets  default_circuitpython_hierarchy  .git  .gitignore  gui.py  gui_tools  main.py  project_tools  README.md  requirements.txt
    ```

6. If you are going to use a [virtual environment](https://docs.python.org/3/library/venv.html), run the following 
   commands:
    1. Windows:
    ```commandline
    python -m venv .venv
    ".venv/Scripts/activate.bat"
    ```
    2. macOS and Linux:
    ```commandline
    python3 -m venv .venv
    source .venv/bin/activate
    ```

7. Install the packages:
    1. Windows:
    ```commandline
    pip install -r requirements.txt
    ```
    2. macOS and Linux:
    ```commandline
    pip3 install -r requirements.txt
    ```
