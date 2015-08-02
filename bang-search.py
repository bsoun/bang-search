import webbrowser
import sublime
import sublime_plugin
 
DUCKDUCK_BANG_URL = "https://duckduckgo.com/?q={{bang}} {{q}}"

searchDict = sublime.load_settings("bang_search.sublime-settings")\
            .get("definitions")
flagFullCaption = sublime.load_settings("bang_search.sublime-settings")\
            .get("display_bang_in_panel")
silentError = sublime.load_settings("bang_search.sublime-settings")\
            .get("silent_error")            

stringToSearch = None
bangToSearch = None # define for direct input search with args
bangList = []
captionList = []

 
# Create the caption in the quick panel with or without the bang
def create_caption(bang,caption):
    panel_label=""
    if flagFullCaption:
        panel_label = bang.ljust(15, " ") +" : " + caption
    else:
        panel_label = caption
    return panel_label

# Display warning
def bang_warning(text):
    print(silentError)
    if silentError:
        sublime.status_message(text)
    else:
        sublime.message_dialog(text)

# Add url to duckduck type

for name,content in searchDict.items():
    if(searchDict[name]['type'] == "duckduckgo"):
        content['url']=DUCKDUCK_BANG_URL.replace("{{bang}}",name)
# Add list(url) to group type
for name,content in searchDict.items():
    if(searchDict[name]['type'] == "group"):
        url=[]
        for i in content['banglist']:
            if (i in searchDict):
                url.append(searchDict[i].get('url'))
        content['url']=url
    # Create bangList and captionList for quickPannel
for name,content in searchDict.items():
    if(searchDict[name]['type'] != "hidden"):
        bangList.append(name)
        captionList.append(create_caption(name,content['caption']))
# sort list the two list, based on caption list
captionList, bangList = zip(*sorted(zip(captionList,bangList)))

def searchByBang(search_string, bang):
    if isinstance(searchDict[bang]['url'],list):
        # groupsearch loop to open several tabs
        for i in searchDict[bang]['url']:
            searchUrl = i.replace("{{q}}",search_string)
            webbrowser.open_new_tab(searchUrl)
    else:
        # duckduck and custom cases
        searchUrl = searchDict[bang]['url'].replace("{{q}}",search_string)
        webbrowser.open_new_tab(searchUrl)
 
 
  
 
class BangSearchCommand(sublime_plugin.TextCommand):
 
    def run(self, edit,**args):
        querys = []
        for region in self.view.sel():
            if region.empty():
                # if we have no selection grab the current word
                word = self.view.word(region)
                if not word.empty():
                    querys.append(self.view.substr(word))
                else:
                # append the selection
                    if not region.empty():
                        querys.append(self.view.substr(region))
        if len(querys) != 0:
            self.stringToSearch = " ".join(querys)
            if args:
                if (args["search_method"] in searchDict):
                    self.bangToSearch = args["search_method"]
                    searchByBang(self.stringToSearch,self.bangToSearch)
                else:
                    bang_warning("%s is not defined !!!" %(args["search_method"]))                    
            else:
                sublime.set_timeout(lambda:self.view.window().show_quick_panel(captionList, self.on_done,sublime.MONOSPACE_FONT),1)
        else:
            bang_warning(" Nothing to search !")
 
    def on_done(self, index):
        if index == -1:
            bang_warning("Search canceled")
        else:
            searchByBang(self.stringToSearch,bangList[index])
 
    def on_cancel(self,arg):
        pass

    def on_change(self,arg):
        pass
 
class BangSearchInputCommand(sublime_plugin.TextCommand):
    def run(self,edit, **args):
        if args:
            if (args["search_method"] in searchDict):
                self.bangToSearch = args["search_method"]
                mylabel = searchDict[args["search_method"]]['caption'] + " : "
                self.view.window().show_input_panel(mylabel, '',self.direct_done, None, None)
            else:
                bang_warning("%s is not defined !!!" %(args["search_method"]))
        else:
            mylabel = "Bang search : "
            self.view.window().show_input_panel(mylabel, '',self.panel_done, None, None)
 
    def panel_done(self, arg):
        if arg == -1:
            bang_warning("Search canceled")
        else:
            self.stringToSearch = arg
            self.view.window().show_quick_panel(captionList,self.child_done, sublime.MONOSPACE_FONT)
 
    def direct_done(self, arg):
        self.stringToSearch = arg
        searchByBang(self.stringToSearch,self.bangToSearch)
 
    def child_done(self,index):
        if index == -1:
            bang_warning(" Nothing to search !")
        else:
            searchByBang(self.stringToSearch,bangList[index])
 
    def on_cancel(self,arg):
        pass
 
    def on_change(self,arg):
        pass
 
 
# webbrowser.get('/usr/bin/google-chrome %s').open_new_tab(searchUrl)
# webbrowser.get('firefox %s').open_new_tab(searchUrl)
