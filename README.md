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

> Note: **This project is still in beta!!!**

## Table of Contents
1. [Installing](#installing)
   1. [Installing from source](#installing-from-source)
2. [Running](#running)
3. [How to use](#how-to-use)
   1. [First run](#first-run)
   2. [Making a new project](#making-a-project)
   3. [Managing projects](#managing-projects)
   4. [Managing dependencies](#managing-dependencies)
   5. [The menu-bar in depth](#the-menu-bar-in-depth)
4. [Options](#options)

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

8. You should now be able to run it!
    1. Windows:
    ```commandline
    python main.py
    ```
    2. macOS and Linux:
    ```commandline
    python3 main.py
    ```

[Back to table of contents](#table-of-contents)

## Running
~~If you installed from a binary, then just run the `CircuitPython Project Manager.exe` (`CircuitPython Project Manager` 
macOS and Linux) file. You may want to create a shortcut/symlink to it on the desktop or create a menu entry. If you 
would like to submit an icon, you can open an issue for it with the icon.~~ No binaries just yet! 

If you install from source and you are not using a virtual environment, then you can just create a `.bat` file containing 
`python \path\to\the\main.py` (`python3`, forward slashes, and use `.sh` for the extension on macOS and Linux) on the 
desktop for convenience. Otherwise, you will need to re-activate the virtual environment everytime you want to run it. 
I highly recommend using these shell scripts:

1. Windows:

```batch
:: Replace this with the path to the directory of the CircuitPython Project Manager, should have main.py in it
cd path\to\the\CircuitPython-Project-Manager
:: You can use python.exe or pythonw.exe - the w one will just supress output of the program
".venv\Scripts\pythonw.exe" main.py
```

2. macOS and Linux:

```shell
# Replace with the path to the CircuitPython Project Manager
cd path/to/the/CircuitPython-Project-Manager
.venv/bin/python3 main.py
```
Don't forget to give the `.sh` file execute permission! (`chmod +x shell_file.sh`)

[Back to table of contents](#table-of-contents)

## How to use

### First run
On run, you should get something like this:

> If the GUI looks different from these images, it's because I don't want to update all these images. I will only 
> update the relevant images.

Figure 2.1: Start up on Windows.

![A picture of the CircuitPython Project Manager on Windows](assets/2/1.png)

Figure 2.2: Start up on Debian. (To be honest, Tk doesn't look that _great_ on Linux...)

![A picture of the CircuitPython Project Manager on Debian](assets/2/2.png)

> Note: From now on, I will be exclusively showing pictures of the CircuitPython Project Manager on Windows unless there 
> are Linux-specific instructions. The interface is _exactly_ the same.

First, let's make a project...

[Back to table of contents](#table-of-contents)

### Making a project

First, lets go to the file menu and click `New...`. As the accelerators say (yea that's the technical term - it's 
supposed to "accelerate" the usage of the program) you can also press <kbd>Ctrl</kbd> + <kbd>N</kbd>. 
(<kbd>Cmd</kbd> - <kbd>N</kbd> for macOS)

Figure 2.3: The file menu with `New...` command highlighted. 

![A picture of the CircuitPython Project Manager's File menu open with the New.. command highlighted](assets/2/3.png)

A new dialog should pop up on your screen - you won't miss it as it's bigger than the main window!

Figure 2.4: The New project dialog.

![A picture of the CircuitPython Project Manager's New Project dialog open](assets/2/4.png)

Click the `Browse...` button to select a directory to place the project in. Or you can also type/copy and paste in the 
location of the project.

Then you may want to change the title of the project to something other than "Untitled."

If you plan on using Git as a VCS, there is a checkbutton on whether you want to auto-generate a `.gitignore`. Really
it might be better to make it mandatory because you should always use a VCS for your code. If you never heard of a VCS 
or Git, then just uncheck this option. 

If you want, type in a description for this project. It's not mandatory at all but it's nice to put TODOs in there or 
whatever. 

If it satisfies the requirements than you can press the `Make new project` button. Otherwise the status message will 
tell you why you can't make a new project with the current settings. 

Once you make a new project, it will open automatically in the main window. On to the next section!

[Back to table of contents](#table-of-contents)

### Managing projects

After opening a project (or creating it) you will be presented with a fairly large window as my applications go at the 
time of this writing with tons of buttons which is always fun.

Figure 2.5: A standard project after creation.

![A picture of the CircuitPython Project Manager with a freshly-created project opened](assets/2/5.png)

Let's outline them in colorful boxes, and I'll tell you what each one does!

Figure 2.6: A standard project after creation but with colorful boxes around all the UI elements.

![A picture of the CircuitPython Project Manager with a freshly-created project opened with the main UI elements boxed in colorful rectangles](assets/2/6.png)

1. In purple, this is where you can modify the project title.
2. In dark-blue, this is where you can modify the project description.
3. In blue, this is a list of the files and **whole** directories that will be synced.
4. In green, this is how you can include and exclude files and directories you want to sync.
5. In yellow, this is where you can save and discard all your changes after changing some stuff around. Pressing the 
   `Sync` button will also sync the listed files and directories to the drive listed as the target.
6. In orange, this is the location of the drive. You may recognize this from my previous project the 
   [CircuitPython Bundle Manager](https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager) (Oh no more shameless
   self promotion) and yes I totally did not copy and paste the code from it. I would never do such a thing. It's the 
   same interface too because ~~I'm all about consistency.~~ But if you don't know, it's a combo box which will list 
   all the connected CircuitPython devices, unless the `Show all drives` checkbutton is, checked. And the refresh button
   will refresh the list of connected drives. 
7. In red, this is the menu bar. We will go more in depth and description and explain all the magic that happens in 
   [The menu-bar in depth](#the-menu-bar-in-depth) section coming up.

If you want to add a file to be synced, say if you were making a lightsaber with sound effects, you may want to sync an 
`.mp3` file with lightsaber noises. To do that, just copy the `.mp3` file into the project directory. (Which you can 
open by clicking on the `Edit` menu casacade and pressing `Open .cpypmconfig file location` because by default, the 
`.cpypmconfig` file defaults to being in the root of your project, unless you moved it. Why would you move it???) Next 
press the `Add file` button and a file selector pops up. Select the `.mp3` file and if all goes to plan, it should 
appear in your list of files and directories to sync!

If you want to add a whole directory to be synced, like if you were making a slide show, then copy the directory full 
of pictures into the project and press `Add directory` and select that directory to sync. If all goes well, it should 
appear in the list of files and directories to sync!

Now if you want to sync your stuff, you must first select a CircuitPython drive. Click on the drop-down icon and select 
a drive. If you can't find it, than you may benefit from selecting `Show all drives?` and checking again. If that still 
doesn't work (file an issue?) then you can enter the path of the device manually too. 

If you are on Linux, depending on where your distribution mounts drives, you may not find any unless you edit the 
application's configuration file. To do so, press on the `Help` casacade and select the `Open configuration` command. 
This will open the configuration file in the default `.json` application. 

Figure 2.7: My configuration file before editing.

![A picture of the configuration file opened in Mousepad on the Raspberry Pi OS (hey it was the only Linux distro I have available right now)](assets/2/7.png)

Now if your distro mounts drives in say, `/media/pi`, then edit the `unix_drive_mount_point` attribute and save.

Figure 2.8: My configuration file after editing.

![A picture of the configuration file after being edited](assets/2/8.png)

Now after editing you may be wondering _why isn't it working??? It won't let me press the button!!! Your software is 
broken and I'm never gonna use it ever again!!!_ You'll need to press the `Save` button and if all things go right, 
everything should go grey for a second and back to normal. You should be able to sync! 

To sync, press the `Sync` button. (wow I would have never thought that) A teensy tiny dialog will pop up saying 
"Syncing..." and once the sync is done it will disappear. That's it! You can also press <kbd>Ctrl</kbd> + <kbd>R</kbd> 
(<kbd>Cmd</kbd> + <kbd>R</kbd> for the folks in macOS land) to sync too or use the sync command in the `Sync` casacade. 

Next we'll ~~do some shameless self promotion~~ and figure out how to manage dependencies.

[Back to table of contents](#table-of-contents)

### Managing dependencies

**This chapter is basically self promotion for my other project the 
[CircuitPython Bundle Manager](https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager).**

Using the CircuitPython Bundle Manager we can manage our dependencies for our project! You can find installation 
instructions [here](https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager#installing). 

In the edit menu, we can copy the root of the project via the `Copy project root file location` and paste that into the 
drive portion of the CircuitPython Bundle Manager, like in figure 2.9.

Figure 2.9: Using the CircuitPython Bundle Manager to install dependencies for us. 

![A picture of the **CircuitPython Bundle Manager** hovering over the `neopixel.mpy` file with the project root location in the drive area](assets/2/9.png)

[Back to table of contents](#table-of-contents)

### The menu-bar in depth

There are lots of commands in the menu-bar. Figure 2.10 shows all of them.

Figure 2.10: All commands in the menu-bar at the time of this writing when a project is opened. 

![Pictures of the CircuitPython Project Manager's various menu items while a project is opened](assets/2/10.png)

- `File`
    - `New...`: Opens a dialog to create a new project. Will only be enabled if no project is opened. The keyboard 
    shortcut is <kbd>Ctrl</kbd> + <kbd>N</kbd>. (<kbd>Cmd</kbd> + <kbd>N</kbd> for macOS users)
    - `Open...`: Opens a file selector prompting you to select a `.cpypmconfig` file. Will only be enabled if no 
    project is opened. The keyboard shortcut is <kbd>Ctrl</kbd> + <kbd>O</kbd>. (<kbd>Cmd</kbd> + <kbd>O</kbd> for 
    macOS users)
    - `Open recent`: Is a sub-menu listing the last 10 `.cpypmconfig` files you've opened. Will only be enabled if no 
    project is opened.
        - `Clear recent projects`: Will clear all the recent projects.
    - `Close project`: Will close the current project. Will only be enabled if a project is opened. The keyboard 
    shortcut is <kbd>Ctrl</kbd> + <kbd>Q</kbd>. (<kbd>Cmd</kbd> + <kbd>Q</kbd> for macOS users)
- `Edit`: All these items will only be enabled if a project is opened.
    - `Open .cpypmconfig`: Opens the `.cpypmconfig` file in the default `.cpypmconfig` application.
    - `Open .cpypmconfig file location`: Opens the `.cpypmconfig` file location in the default file browser.
    - `Open project root file location`: Opens the project root file location in the default file browser.
    - `Copy project root file location`: Copies the project root file location to the clipboard.
    - `Save changes`: Saves the changes you made in the GUI. The keyboard shortcut is <kbd>Ctrl</kbd> + <kbd>S</kbd>. 
    (<kbd>Cmd</kbd> + <kbd>S</kbd> for macOS users)
    - `Discard changes`: Discards the changes you made in the GUI. The keyboard shortcut is 
    <kbd>Ctrl</kbd> + <kbd>D</kbd>. (<kbd>Cmd</kbd> + <kbd>D</kbd> for macOS users)
- `Sync`: All these items will only be enabled if a project is opened.
    - `Sync files`: Syncs the files. The keyboard shortcut is <kbd>Ctrl</kbd> + <kbd>R</kbd>. (For "run") 
      (<kbd>Cmd</kbd> + <kbd>R</kbd> for macOS users)
- `Help`
    - `Open configuration`: Opens the configuration file in the default `.json` application.
    - `Open logs`: Opens the logs in the default `.log` application.
    - `Open README.md`: Opens the README.md file. The keyboard shortcut is <kbd>F1</kbd>
    - `Convert Markdown to HTML`: A checkbutton on whether to convert the markdown to HTML before opening it for you. 
    If it is checked, the README will be opened in the default `.html` application, otherwise it will open in the 
    default `.md` application.
    - `Open project on GitHub`: Opens the project on GitHub in the default browser.
    - `Open issue on GitHub`: Opens the new issue panel on GitHub in the default browser. 

[Back to table of contents](#table-of-contents)

## Options

You can find these options in `config.json`, which is in the same directory as 
[`main.py`](https://github.com/UnsignedArduino/CircuitPython-Project-Manager/blob/main/main.py), and should be 
auto-generated upon first run. In case it does not happen, (file a issue?) this is the default JSON file:
```json
{
    "last_dir_opened": "E:\\Test",
    "opened_recent": [
        "E:\\Test\\Untitled\\.cpypmconfig"
    ],
    "show_traceback_in_error_messages": false,
    "unix_drive_mount_point": "/media"
}
```
- `last_dir_opened` should be a string of a path that points to the last directory that you opened, so the next time 
  you open a file/directory, you will start there! It will be set once you open a directory/file, and **will not appear 
  immediately.** 
- `opened_recent` should be a list of strings which are the paths of projects you last opened. It will be set once you 
  open/create a new project, and **will not appear immediately.** 
- `show_traceback_in_error_messages` should be a boolean. (Either `true` or `false`) This will control whether stack 
  traces will appear in error messages.
- `unix_drive_mount_point` should be a string of a path that points to the place where your distro automatically mounts 
  drives. Only applies to Unix-based systems.

[Back to table of contents](#table-of-contents)