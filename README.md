Bang Search 
=============

**Version : 1.1.2**
Correction of bug.

**Version : 1.1.1**

This plugin for Sublime Text 3 allow to perform a web search from the currently selected text/word or from an input panel from **your predifined requests** in **one or several browser tabs**.


Various custom or predefined search engine are declared in the `bang-search.sublime-settings`.
You can add yours quite easily in this file , you can prefix your bang by whatever you want except for duckduckgo, this one must be valid : !...


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

The two first parameters control the display options :
- Display the bang before the caption of your predefine search engine in the quick panel
- The second one :   
	* If true, display alert message in the bottom status panel
	* If false, a dialog box show you the warning message
- The third parameter contain the list of browser (see below)
```json
[
{
    "display_bang_in_panel": true,
    "silent_error": true,
    "browsers_list": ["default","firefox","google-chrome"],
}
]
```
The *definitions* contain your search requests :
```json
[
{
     "!gt": {
        "type": "duckduckgo",
        "caption": "Google Translate"
      },
      "!python27": {
        "type": "duckduckgo",
        "caption": "Python 2.7"
      },
      "&gh": {
        "type": "qwant",
        "caption": "Github"
      },
      "@ipynbViewer": {      
      "type": "custom",
      "caption": "iPyNotebookViewer",
      "url": "https://google.com/#q={{q}} site:nbviewer.ipython.org/github/"
      },   
      "@speakerdeck": {
        "type": "hidden",
        "caption"  : "speakerdeck",
        "url"      : "https://speakerdeck.com/search?utf8=✓&q= {{q}}"
          },      
      "#PY2": {
        "type": "group",
        "caption": "python2 general search",
        "banglist": [
          "!python27",
          "@ipynbViewer"]}
}
]
```

There are 4 types of request :  
* **duckduckgo** : a bang style [duckduckgo][5] search request, you have to give a valid !bang
* **qwant** : a qwick style [qwant][6] search request, you have to give a valid &qwick
* **custom** : any kind of site or search engine, google [i.e.][4], {{q}} will be replace by your search 
* **hidden** : a custom request which doesn't appear in the quick panel (can be use in command arg, or group call)
* **group** : a list of bang [duckduckgo|custom|hidden] defined in your bang-search.sublime-settings



You can edit the settings by going to Preferences -> Package Settings -> Bang Search -> Settings - User

##Browser configuration

The lib used to open a new tab is webbrowser.py. Only the first element of browsers_list will be used, the others are here to allow quick change in your configuration file. The "default" value refer to the None settings in webbrowser.py corresponding to the default browser.

**THE FOLLOWING CONFIGURATION IS AT YOUR OWN RISK, let "default" if you have any doubt.**

###Identify already defined browsers by webbrowser.py

Open a console : View > Show console

And enter the following code to identify which browser you can use :
```
import webbrowser; print(webbrowser._browsers)
```

###Register a browser in webbrowser.py

Open a console : View > Show console

And enter the following code to [register](https://docs.python.org/3/library/webbrowser.html#webbrowser.register) a browser. Here is a sample for windows, you have to define an alias and the correct path to the choosed browser.
```
import webbrowser; webbrowser.register('google-chrome', None, webbrowser.BackgroundBrowser("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"))
```

###Choose the browser for Bang-Search

In the bang_search.sublime-settings, place your _default_ browser in first place in the list.
```
"browsers_list": ["firefox","default","google-chrome"],
```

##Usage

Get the quick panel to choose your search query :
- Place the cursor inside a word or select some text and press `Alt+Super+B`
![quick_panel][quick_panel]

- Press `Ctrl+Super+B` to get the input panel
![input_panel][input_panel]



Use a personal key binding with args search-method:

- Launch directly the @def query from your selected text.
```
{
  "keys": ["shift+alt+super+b","shift+alt+super+d"], 
  "command": "bang_search",
  "args": {"search_method": "@def"}
},
```
- Launch directly the @def query after opening the input text.
```
{
  "keys": ["ctrl+shift+super+b", "ctrl+shift+super+d"], 
  "command": "bang_search_input",
  "args": {"search_method": "@def"}
}
```
![input_definition][input_definition]


  [1]: http://www.sublimetext.com
  [2]: https://sublime.wbond.net/
  [3]: https://github.com/bsoun/bang-search/archive/master.zip
  [4]: http://www.googleguide.com/advanced_operators_reference.html
  [5]: https://duckduckgo.com/bang
  [6]: https://www.qwant.com/qwick


[quick_panel]: https://raw.githubusercontent.com/bsoun/bang-search/master/doc/quick_panel.gif
[input_panel]: https://raw.githubusercontent.com/bsoun/bang-search/master/doc/input_panel.gif
[input_definition]:https://raw.githubusercontent.com/bsoun/bang-search/master/doc/input_definition.gif
