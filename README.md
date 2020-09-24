# Maya python tools
Python tools for Maya.

## loadSubstanceMaps.py
Browse for a folder containing Substance Painter texture maps and import as an aiStandardSurface.

## lockit.py and unlockit.py
Simple scripts for the shelf to lock and unlock the translation, rotation and scale of selected objects.
Motivation: useful for reference objects

## manualBackup.py
Simple script to save a backup copy of current file elsewhere while remaining on the current file. Similar to QuickSave in ZBrush, with the difference being the user must name the new file. Equivalent to save as followed by re-opening the original file.

Motivation: Incremental save creates too many files with trivial changes, and it's difficult to find the file you want when rolling back, but backups are still needed for good versions to rollback to if something goes wrong. This is a reliable, simple manual backup for peace of mind before attempting something tricky.

Limitations: This only saves the current Maya .mb file. Anything else contained in other files would not be saved.

![Back up demo](demos/backup_maya_shelf_tool.gif)

## License
[MIT](https://opensource.org/licenses/MIT)
