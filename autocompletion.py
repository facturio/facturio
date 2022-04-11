#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk  # noqa: E402
from Info_Facture_Devis import articles, clients


class FacturioEntryCompletion(Gtk.Entry):
    def __init__(self, func, completions):
        super().__init__()

        self.completion = Gtk.EntryCompletion()
        self.completion.set_inline_selection(True)

        self.set_completion(self.completion)

        self.completion_dict = dict((func(item), item) for item in completions)

        self.completion_list = Gtk.ListStore(str)
        [self.completion_list.append([func(item)]) for item in completions]

        self.completion.set_model(self.completion_list)
        self.completion.set_text_column(0)
        self.completion.connect('match-selected', self.on_match_selected)

    def on_match_selected(self, entry_completion, model, iter):
        print(tuple(model[entry_completion.get_text_column()]))

if __name__ == '__main__':
    win = Gtk.Window()
    box = Gtk.Box(orientation=1, spacing=6)
    box.add(FacturioEntryCompletion(lambda x: x.prenom, clients))
    box.add(FacturioEntryCompletion(lambda x: x.nom, clients))
    win.add(box)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
