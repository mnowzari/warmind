"# warmind" 

Warmind is a simple command-line stat puller for Destiny 2. It uses the Destiny 2/Bungie Platform API.

This is a work in progress. 

To run the program, simply call the following from your command line:
	> python destiny2_warmind.py

List of commands:

basic_info: Prints basic information regarding the provided account

char_sheet: Displays the character sheet for all characters on your account. Includes basic stats as well as list of the current loadout.

stats_pve: Historical stats for all PvE activities

stats_pvp: Historical stats for all PvP activities

stats_raid: Historical stats for all Raid activities

stats_strike: Historical stats for all Strike activities

stats_story: Historical stats for all Story activities

!help: Brings up this help menu

!new_guard: Enter a new Guardian (WIP)

!dump: Downloads raw data in the form of JSON files from Bungie servers to your computer. Useful if you're a developer and know what to do with JSON. 

!q: Quit program