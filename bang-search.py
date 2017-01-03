import webbrowser
import sublime
import sublime_plugin

DUCKDUCK_BANG_URL = "https://duckduckgo.com/?q={{bang}} {{q}}"
QWANT_QWICK_URL = "https://qwant.com/?q=%26{{bang}} {{q}}"
CONFIG_FILE = "bang_search.sublime-settings"


def create_caption(bang,caption,flagFC):
    # get config file
    panel_label=""
    if flagFC:
        panel_label = bang.ljust(15, " ") +" : " + caption
    else:
        panel_label = caption
    return panel_label

# Display warning
def bang_warning(text,flagError):
    if flagError:
        sublime.status_message(text)
    else:
        sublime.message_dialog(text)


# From config file retrieve one list for caption and one list for bang
def init_lists(searchDict,flagFC):
  bangList = []
  captionList = []
  for name,content in searchDict.items():
      if(searchDict[name]['type'] == "duckduckgo"):
          content['url']=DUCKDUCK_BANG_URL.replace("{{bang}}",name)
      else:
        if(searchDict[name]['type'] == "qwant"):
          # remove the & because it's directly replaced in url %26 
          content['url']=QWANT_QWICK_URL.replace("{{bang}}",name[1:])
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
          captionList.append(create_caption(name,content['caption'],flagFC))
  # sort list the two list, based on caption list
  captionList, bangList = zip(*sorted(zip(captionList,bangList)))

  return captionList, bangList

def searchByBang(search_string, bang, searchDict,choosedBrowser):
    if isinstance(searchDict[bang]['url'],list):
        # groupsearch loop to open several tabs
        for i in searchDict[bang]['url']:
            searchUrl = i.replace("{{q}}",search_string)
            if choosedBrowser != "default":
              webbrowser.get(choosedBrowser).open_new_tab(searchUrl)
            else: 
              webbrowser.get(None).open_new_tab(searchUrl)
            
    else:
        # duckduck and custom cases
        searchUrl = searchDict[bang]['url'].replace("{{q}}",search_string)
        if choosedBrowser != "default":
          webbrowser.get(choosedBrowser).open_new_tab(searchUrl)
        else: 
          webbrowser.get(None).open_new_tab(searchUrl)

def init(self):
  self.stringToSearch = None
  self.bangToSearch = None
  self.bangList = []
  self.captionList = []
  self.flagFullCaption = sublime.load_settings(CONFIG_FILE).get("display_bang_in_panel")
  self.silentError = sublime.load_settings(CONFIG_FILE).get("silent_error")
  self.searchDict = sublime.load_settings(CONFIG_FILE).get("definitions")
  self.choosedBrowser = sublime.load_settings(CONFIG_FILE).get("browsers_list")[0]
  self.captionList, self.bangList  = init_lists(self.searchDict,self.flagFullCaption)

class BangSearchCommand(sublime_plugin.TextCommand):

    def run(self, edit,**args):
        init(self)
        querys = []
        for region in self.view.sel():
            if region.empty():
                # if we have no selection grab the current word
                word = self.view.word(region)
                if not word.empty():
                    querys.append(self.view.substr(word))
            else:
                querys.append(self.view.substr(region))

        if len(querys) != 0:
            self.stringToSearch = " ".join(querys)
            if args:
                if (args["search_method"] in self.searchDict):
                    self.bangToSearch = args["search_method"]
                    searchByBang(self.stringToSearch,self.bangToSearch, self.searchDict, self.choosedBrowser)
                else:
                    bang_warning("%s is not defined !!!" %(args["search_method"]),self.silentError)
            else:
                sublime.set_timeout(lambda:self.view.window().show_quick_panel(self.captionList, self.on_done,sublime.MONOSPACE_FONT),1)
        else:
            bang_warning(" Nothing to search !",self.silentError)

    def on_done(self, index):
        if index == -1:
            bang_warning("Search canceled",self.silentError)
        else:
            searchByBang(self.stringToSearch,self.bangList[index],self.searchDict,self.choosedBrowser)

    def on_cancel(self,arg):
        pass

    def on_change(self,arg):
        pass

class BangSearchInputCommand(sublime_plugin.TextCommand):

    def run(self,edit, **args):
        init(self)
        if args:
            if (args["search_method"] in self.searchDict):
                self.bangToSearch = args["search_method"]
                mylabel = self.searchDict[args["search_method"]]['caption'] + " : "
                self.view.window().show_input_panel(mylabel, '',self.direct_done, None, None)
            else:
                bang_warning("%s is not defined !!!" %(args["search_method"]),self.silentError)
        else:
            mylabel = "Bang search : "
            self.view.window().show_input_panel(mylabel, '',self.panel_done, None, None)

    def panel_done(self, arg):
        if arg == -1:
            bang_warning("Search canceled",self.silentError)
        else:
            self.stringToSearch = arg
            self.view.window().show_quick_panel(self.captionList,self.child_done, sublime.MONOSPACE_FONT)

    def direct_done(self, arg):
        self.stringToSearch = arg
        searchByBang(self.stringToSearch,self.bangToSearch,self.searchDict,self.choosedBrowser)

    def child_done(self,index):
        if index == -1:
            bang_warning(" Nothing to search !",self.silentError)
        else:
            searchByBang(self.stringToSearch,self.bangList[index], self.searchDict,self.choosedBrowser)

    def on_cancel(self,arg):
        pass

    def on_change(self,arg):
        pass

