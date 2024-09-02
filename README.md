# SnakeEyes
SnakeEyes is a dice rolling app for playing tabletop roleplaying games, written in Python 3.12 with PyQT5.  It is capable of saving and rolling preset dice as well as any other dice, including non-standard dice, and can also be used to roll on tables and present the results.  There is also a function to generate die clocks, which are series of preset rolls representing values on a clock to track the passing of time and prompt the introduction of complications.  At the end of this readme is a short set of rules for using die clocks in gameplay.

## Installation
Because SnakeEyes is written in 64-bit Python and packaged as an executable zip, a 64-bit Python 3 installation is required to run it.  It was written and tested in Python 3.12, though it may or may not run in other versions of Python 3.

### Windows
On Windows, an appropriate Python installation is included with the release, and does not need to be installed or downloaded separately.

Simply download the .zip file of the latest Windows release from this repository, unzip it wherever you like, and double-click on the `Create Shortcut.bat` file within the app folder.  This will create a shortcut in your Start menu that allows you to run the app.

It is recommended you place the shortcut in `\AppData\Roaming\Microsoft\Windows\Start Menu\Programs` for convenience.  This will cause the shortcut to appear in the Start menu with the correct icon.  More shortcuts can always be made by double-clicking on `Create Shortcut.bat`.

### Linux
On Linux, SnakeEyes has only been built and tested for Kubuntu 24.04.  It probably runs just fine on many other distros, but you're on your own as far as resolving any problems or differences.

It is generally assumed that you already have 64-bit Python 3 installed as part of your distro.  If your distro has 3.12, you should be fine; otherwise, you may or may not need to install 3.12.

First, download the .zip file of the latest Linux release from this repository, and unzip it wherever you like (probably easiest somewhere in your Home).  To run the app, open a terminal in the app's directory and use the following command:

```
python3 SnakeEyes.pyzw
```

Alternatively, you can use the included Python interpreter (after giving `Python Interpreter - Linux/bin/python3` executable permissions, if needed):

```
"Python Interpreter - Linux/bin/python3" SnakeEyes.pyzw
```

However, for convenience, consider running `python3 CreateLinuxDesktopFile.py` or `python3 CreateLinuxDesktopFileForIncludedInterpreter.py` (also in the app's directory; they will not work properly with any other working directory).  This will generate a .desktop file, which will then be moved to `~/.local/share/applications/`.  Now SnakeEyes should show up along with your other apps in your desktop menus.

If you prefer not to use the included interpreter, consider deleting the `Python Interpreter - Linux` folder to save space.

If SnakeEyes does not run at first, you probably need to resolve some dependencies.  First, try `sudo apt install libxcb-xinerama0`.  If that doesn't resolve the issue, try installing PyQT5 with `sudo apt install python3-pyqt5`; if this does resolve the issue, you might even be able to (partially) uninstall it with `sudo apt remove python3-pyqt5` and still run SnakeEyes, as long as you don't autoremove the additional packages that were installed with it.  If installing PyQT5 through APT doesn't work, try installing it through pip; if you don't have pip already, use `sudo apt install python3-pip`, then run `pip3 install pyqt5`.  Other issues have not yet been encountered and will require you to do some research and troubleshooting to resolve on your system.

## Updates
Updating SnakeEyes is as simple as deleting all files wherever you installed it *except* the `Configs` folder, and then extracting the contents of the latest release to the installation folder.  Any shortcuts in place should resolve without issue to the updated version.  If you are using the included interpreter, you may have to give it executable permissions after updating.

The `Configs` folder should be left in place as it stores settings and contexts between uses of the app.

## Uninstallation
Uninstalling SnakeEyes itself only requires deleting the directory you extracted it to, along with any shortcuts you created.

If you need to uninstall Python 3.12 or, on Linux, PyQT5, consult their documentation.

## Die Clocks
The following rules describe a simple, abstract mechanic to loosely track time pressure and introduce complications in stressful situations, like exploring monster-infested ruins or trying to track down kidnappers before they get away with their hostage.

A die clock is first defined by a particular die, like a d6 or a d20.  The clock starts at 0, has a maximum value equal to the maximum roll possible on the die, and has a complication threshold somewhere between the two.  As the party takes actions that require appreciable time, like checking for traps, looking for clues, moving from area to area, and so on, the die clock increases, usually by 1.  The die clock usually does not increase as a result of combat encounters, unless the explicit goal of the party's foes is to slow them down or distract them from some other pressing problem.

The time it takes for the die clock to increase is purposefully nebulous to allow for flexibility, but in most situations would correspond to somewhere between five and ten minutes; after the die clock increases six times, assume an hour has passed.  The GM can also use die clocks to track the passage of longer spans of time, like hours, days, weeks, and so on.

After the clock increases, if it equals or exceeds its complication threshold, a player or the GM rolls the clock's die.  If the result equals or exceeds the current value of the clock, nothing happens.  Otherwise, the clock goes off.  If the clock is at its maximum value, it automatically goes off without a roll.

When the clock goes off, the GM presents the party with a complication of some kind, most often an encounter or something else that would logically result from the party spending time.  The GM can also use a GM intrusion to set off the clock, regardless of its source.

Once the clock has gone off, it resets to 0, and continues as before, increasing as actions are taken under some kind of time pressure or in a dangerous location, potentially going off multiple times.  This continues until the GM decides that the pressure no longer applies, either because of some kind of resolution or because the party leaves the dangerous situation.

If the GM determines that the party is in a particularly dangerous situation, drawing too much attention, or otherwise behaving recklessly, the clock might increase by higher values per action, hastening its going off.  The GM also sets the complication threshold; lower thresholds correspond to more uncertainty and more frequent complications, while higher thresholds represent more stable and predictable situations.  Consult the following table for a general idea of how clock increase values and complication thresholds interact:

|  | Low Complication Threshold | High Complication Threshold |
| :-- | :-- | :-- |
| **Low Increases** | Unpredictable, less frequent complications | Predictable, less frequent complications |
| **High Increases** | Unpredictable, more frequent complications | Predictable, more frequent complications |

The size of the die determines the granularity of the clock's values, allowing the GM more flexibility in determining how the party's actions and circumstances affect the clock.

The GM should prepare for a session using a die clock by experimenting with its die, complication threshold, and increase values to get the right feel for the situation.