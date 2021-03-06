import gtk
import urllib
import terminatorlib.plugin as plugin
import re

# Written by John Cooper http://choffee.co.uk
# Copyright 2010 John Cooper
# See copyright file that comes with this file for full licence
# Modified by cgw 2011/11/06
# AVAILABLE must contain a list of all the classes that you want exposed
# Those guys at the top are cool ... don't sue me
# Modified for Github by kmf 2017/07/16

AVAILABLE = ['GithubSearchPlugin']

_spaces = re.compile(" +")

# TODO:   move some of the constants into a config object

class GithubSearchPlugin(plugin.Plugin):
    capabilities = ['terminal_menu']

    def do_search(self, searchMenu):
        """Launch Github Issues search for string"""
        if not self.searchstring:
            return
        base_uri = "https://github.com/search?q=%s&ref=opensearch&type=Issues"
        uri = base_uri % urllib.quote(self.searchstring.encode("utf-8"))
        gtk.show_uri(None, uri, gtk.gdk.CURRENT_TIME)

    def callback(self, menuitems, menu, terminal):
        """Add our menu item to the menu"""
        self.terminal = terminal
        item = gtk.ImageMenuItem(gtk.STOCK_FIND)
        item.connect('activate', self.do_search)
        if terminal.vte.get_has_selection():
            clip = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
            self.searchstring = clip.wait_for_text().strip()
            self.searchstring = self.searchstring.replace("\n", " ")
            self.searchstring = self.searchstring.replace("\t", " ")
            self.searchstring = _spaces.sub(" ", self.searchstring)
        else:
            self.searchstring = None
        if self.searchstring:
            if len(self.searchstring) > 40:
                displaystring = self.searchstring[:37] + "..."
            else:
                displaystring = self.searchstring
            item.set_label("Search Github Issues for \"%s\"" % displaystring)
            item.set_sensitive(True)
        else:
            item.set_label("Search Github Issues")
            item.set_sensitive(False)
        # Avoid turning any underscores in selection into menu accelerators
        item.set_use_underline(False)
        menuitems.append(item)
