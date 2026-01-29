# Hogwarts Legacy Save Tools GUI - With Legilimens Support

&copy; Henry & Lukas 2025-2026

<https://www.nexusmods.com/hogwartslegacy/mods/2372>

I made this GUI as I plan to play Hogwarts Legacy again.

*ALWAYS BACK UP YOUR SAVE FILES!*

Keep all the files in the same folder as shown in the screenshot, and double-click HLST_GUI.exe. That's it. You don't have to type commands in CMD or PowerShell anymore.

To make Legilimens work, there should be **only Latin characters and numbers** in the full path of the folder you create. For example, **D:\HL999**.

The HLSE is 1.7.2 by default. If you prefer the old version (1.7.1), you could manually rename "hlse-1.7.1-ALPHA.html" to "hlse.html".

## THE BUTTONS

GO TO SAVED GAMES
- This will open **C:\Users\YOUR_USERNAME\AppData\Local\Hogwarts Legacy\Saved\SaveGames** in Windows File Explorer.

RENAME
- This will rename YOUR_SAVE.sav to YOUR_SAVE.orig.

DECOMPRESS
- This will launch CMD and run `hlsaves.exe -d YOUR_SAVE.orig YOUR_SAVE.decomp`.

LAUNCH THE EDITOR
- This will launch Hogwarts Legacy Save Game Editor in your default browser.
- When you finish editing in the browser, you still need to manually download the save file and rename it to YOUR_SAVE.edited.

LAUNCH LEGILIMENS
- This will ask you for YOUR_SAVE.decomp, and then launch CMD and run `Legilimens.exe YOUR_SAVE.decomp --filters ALL -o output.txt`.
- This will write the output to a file named "output.txt" in the same folder.

COMPRESS
- This will launch CMD again and run `hlsaves.exe -c YOUR_SAVE.edited YOUR_SAVE.sav`.

For more information, check out the page of *Hogwarts Legacy Save Game Editor*, *Hogwarts Legacy Save Tool*, or *Legilimens - The Hogwarts Legacy Collectible Finder*.

All dependencies are included with permission.

- [Hogwarts Legacy Save Game Editor](https://www.nexusmods.com/hogwartslegacy/mods/77),
- [Hogwarts Legacy Save Tool](https://github.com/topche-katt/hlsavetool),
- [Legilimens - The Hogwarts Legacy Collectible Finder](https://github.com/Malin001/Legilimens-Hogwarts-Legacy-cpp),
- [oo2core_9_win64.dll](https://github.com/WorkingRobot/OodleUE/blob/main/Engine/Source/Programs/Shared/EpicGames.Oodle/Sdk/2.9.10/win/redist/oo2core_9_win64.dll).

## UPDATES
 
V2.0 - 2025-12-20
- Now supports Legilimens.

V2.1 - 2026-1-3
- Bug fixes.

V2.2 - 2026-1-19
- Bug fixes and a new button.
