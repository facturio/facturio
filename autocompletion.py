"""Module d'autocomplétion."""
from Info_Facture_Devis import clients, articles
import argparse
import re

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa: E402


class ItemRow(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data))


class MainWindow(Gtk.Window):
    """La fenêtre principale contenant la barre de recherche."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.box = Gtk.Box(orientation=1, spacing=6)
        self.add(self.box)

        self.search = Gtk.SearchEntry(placeholder_text="Recherche")
        self.search.connect("search-changed", self.on_search_changed)
        self.search.connect("stop-search", self.on_stop_search)

        self.results = Gtk.ListBox()
        self.results.connect("row-activated", self.on_row_activated)

        self.resdetail = Gtk.ListBox()

        self.box.pack_start(self.search, False, True, 0)
        self.box.pack_start(self.results, False, True, 0)
        self.box.pack_start(self.resdetail, True, True, 0)

    def on_search_changed(self, entry):
        for row in self.results.get_children():
            self.results.remove(row)

        if entry.get_text() != "":
            for item in complete(clients+articles, entry.get_text()):
                self.results.add(ItemRow(item))

        self.show_all()

    def on_stop_search(self, entry):
        for row in self.results.get_children():
            self.results.remove(row)

    def on_row_activated(self, list_box, row):
        print(vars(row.data))


def complete(items, text):
    req = re.compile(".*" + re.escape(text) + ".*", re.IGNORECASE)
    res = []

    for item in items:
        if any([req.match(str(el)) for el in vars(item).values()]):
            res.append(item)

    return res


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="Autocompletion test.")
    # parser.add_argument('text', type=str, help="text to autocomplete")
    # args = parser.parse_args()

    # print(complete(clients, args.text))
    # print(complete(articles, args.text))

    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
