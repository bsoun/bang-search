Bang Search **BETA VERSION**
=============

This plugin for Sublime Text 3 allow to perform a web search from the currently selected text/word
or from an input panel.
Various custom or predefined search engine are declared in the bang_search.sublime-settings.

There are several ways to perform your search :
* on a selected text/word :
	- show a quick panel to select your search request
	- directly launch a predefined search request	
* from an input panel
	- show a quick panel to select your search request
	- directly launch a predefined search request	

This package adds: 

* A `Bang Search` command to the context menu for the selected
* A `Bang Input Search` command to the context menu for the selected
* A `Bang Search` to the command pannel
* A `Bang Input Search`to the context panel

## Install

If your using the [Sublime Package Manger][2] hold down Ctrl+Shift+P and type
`Package Control: Install Package`. Then search for `bang-search` and hit return.

If your not using the package manager then go to your Sublime packages directory(Sublime Text/Packages) Then run this command `git clone https://github.com/bsoun/bang-search.git`.

Or you can download the package as a zip file [https://github.com/bsoun/bang-search/archive/master.zip][3] then copy it into your Sublime packages directory.


## SETTINGS
The two first parameters control the estethic
```json
{
	// Display the bang before the caption of your predefine search engine
    "display_bang_in_panel": true,
    // If true, display alert message in the bottom status panel
    // If false, a dialog box show you the warning message
    "silent_error": true,
}
```
The *definition* contain your search request
```json
{
** TO COMPLETE **
}
```
There are 3 types of request :
- duckduckgo : a bang style [duckduckgo][5] search request
- custom : any kind of site or search engine, google [i.e.][4]
- hidden : a custom request which doesn't appear in the quick panel (use in command arg, or group call)
- group : a list of bang [duckduckgo|custom|hidden] defined in your bang-search.sublime-settings


You can edit the settings by going to Preferences -> Package Settings -> Bang Search -> Settings - User

##Usage

Place the cursor inside a word or select some text and press `Ctrl+Super+B` or `Alt+Super+B`.

Context Menu
![context menu][4]

Command Pallette

![pallete][5]

![pallete][6]

  [1]: http://www.sublimetext.com
  [2]: https://sublime.wbond.net/
  [3]: https://github.com/bsoun/bang-search/archive/master.zip
  [4]: http://www.googleguide.com/advanced_operators_reference.html
  [5]: https://duckduckgo.com/bang
