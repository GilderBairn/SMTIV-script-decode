
# README (SUPER IMPORTANT)
## How do I use this dang thing? What IS it?

These files contain the English localized text script for the 3DS game Shin Megami Tensei IV, translated from its native .mbm format to a human-readable .txt. This is our first draft of the extraction, and improvements may be made in the future. Included as well is the .mbm -> .txt program itself! This will presumably only fully work with SMTIV's .mbm files, but feel free to throw other stuff at the wall and see what sticks.

This is kind of a handmade online library for the game. Each .txt has a corresponding .mbm in the actual ROM. Of course, this doesn't contain any actual game files, just the translations where the .mbms would be. You can dig through it right here, or download files to view in the text editor of your choice. It's just text, so even if you download everything, it'll be pretty small. If you're still pretty lost, just click the green code button above and click "Download ZIP" for everything.

If you have a (LEGAL!!) extracted ROM of your own to look through, you can compare the .mbm files to the .txt ones here for context purposes. The file structure should be the exact same, and all names are unchanged as well for ease of access. If that's too much searching for your tastes (understandable), a full compiled .txt of ALL text is also here to ctrl + F your way around. Fair warning, it's really big.

There's likely an error or two around, as not all variables are totally understood, and some potentially-inaccurate placeholder text has been inserted to keep the translator program running. These will be something like a number (i.e. 71), or simple names for understood variables (things like demon name and race). These variables are likely pulled from the many MANY tables found in the game. As we haven't cracked those yet, we have placeholders instead to keep it all readable. Though, if any intrepid investigators would like to suggest what a chosen placeholder might actually represent, please feel free.

Another note: Not all the text found is used in-game, this is standard fare for most video games in general. For more info on what is used vs. unused, check [this article](https://tcrf.net/Shin_Megami_Tensei_IV) on SMTIV by the fine folks at The Cutting Room Floor. Some unused text remains in Japanese, as well. On top of that, some files will be entirely blank. This was likely a product of the devs, or more removed content, it doesn't necessarily mean anything's actually missing.

There are lots of game files that are NOT .mbm, meaning some folders in this upload will be outright empty (as they didn't contain anything to translate). We might remove these on our next pass for ease of searching, but for now they're still in. If anything else seems up that we might've missed, please feel free to submit a bug report.

Now, the apple has been set before all of you. Eat well! :)

## Recommended Folders
You'll find the juiciest stuff in the following folders (in order of appearance):
- /addon
	- All written DLC content is here, essentially.
- /battle
	- /DevilMsg
		- These are from when your demons speak to you after battle.
	- /event
		- All folders are different events in specific battles. Some unused.
	- /talk
		- This is all Talk system stuff. Lots of gems in here, both hilarious and sad.
- /event
	- Pretty self explanatory. All events are in their own folder here. Again, some are unused.
- /item
	- Just one .txt containing all (?) item descriptions. Sadly, their corresponding items are variables confined to an untranslated table, so it's just the descriptions.
- /map
	- All folders with a letter followed by a number contain map-related events.
- /mikado
	- Similar to above. Not much, but some stuff there.
- /npc_room
	- Chats with NPCs are here.
- /quest_center
	- /center
		- Bulletin-board related text.
	- /common
	- /npc
		- Talks with NPCs at quest centers (i.e. K's and THA).
- /shop
	- Basic shopkeeper text.
- /status
	- Descriptions for demons. Similar to the /item and /skill folders, these descriptions are currently unlabeled, though you can probably easily deduce who each one refers to.
- /unite
	- Cathedral of Shadows! A chat with Mido as well. Nifty.

## What's NOT in these files:
- Graphics (i.e. backgrounds, sprites, 3D models)
- Audio (i.e. voice clips, music)
- Cutscenes, or the captions in them, though I think they're all available on YouTube anyway.
- The original Japanese text. As interesting as it would probably be, neither me or my partner know a lick of Japanese. Unsure if the program we made would work with the Japanese copy anyway, but if anyone wants to give it a go, feel free.
- An analysis of the text. I'll leave this to more articulate folks for now. It's just the text left as it is, with the placeholders only there to keep the decoding program functional.
- The tables variables are pulled from. We don't know how to get those open or readable quite yet.
- Anything from IV: Apocalypse. Might be our next foray, but right now it's just IV.
- The game itself.. sorry.

## Final Thoughts and Usage Stuff

Due to Nintendo's.. er.. poor handling of the 3DS in recent years and ATLUS kind of just leaving this game to flounder on a discontinued console, I hope having this script uploaded can be a piece of preservation for a really good game (or just a fun canon resource for obsessive superfans like myself). 

Obviously neither me or my partner wrote this game, so it'd be silly to be like "you can't use this resource for x thing". All writing creds go to ATLUS, we just made it accessible. The decoding program itself (that we DID write) is open source and you can basically do whatever you want with it.

If you read all this, thanks! I hope you find some interesting stuff about this extremely underrated game, and have an awesome day.

## Running the python script

The included python script can be run from the command line to decode MSG2 format (.mbm) files like the ones found in SMTIV, and possibly other ATLUS games. The script itself will produce .txt file counterparts containing a summary the contents of the encoded .mbm either alongside the original files, in a single combined text document, or both depending on the user's specification. 

### Requirements
- Python version 3.9 or higher installed

### Usage

From your any terminal/command prompt run a command with the following structure

```
$ Python mbm.py <path to an .mbm file or a folder containing them> [any number of options (optional, separated by spaces)]
```

Note that you may provide a path to a single file (must end in .mbm!) or a directory/folder to search through for .mbm files.

### Options

- -r - if a directory/folder is specified in the input, the script will recursively convert .mbm files in all sub-folders of the provided folder
- -a - script will create a combined "all-in-one" file containing all the contents of the .mbm files encountered while searchign a folder
- -A - script will ONLY create a combined "all-in-one" file, and will not create .txt files alongside any .mbm files found in a folder
- -v - verbose mode; the script will provide more detailed logs of what it encounters. when providing a single .mbm file as input, the verbose mode will provide even more detailed debug information