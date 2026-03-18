# GUICLEANUP

The function is effective only on Windows platforms. It takes a dialog name as the single argument and unloads it, thereby deleting all QT widgets (controls) associated with the dialog, reducing the HANDLE (USER Objects) count of the parent process e.g. 'aview'. On Windows platforms, the maximum allowable HANDLE limit for a process is 10,000, after which, programs are known to behave erratically.

## Format
```
GUICLEANUP(object)
```

## Arguments

**Object**
: The dialog box name
