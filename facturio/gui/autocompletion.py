#!/usr/bin/env python3
"""Module de création de champs d'autocomplétion."""

import facturio.examples as examples
import gi
import re
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk  # noqa: E402


class FacturioEntryCompletion(Gtk.Entry):
    """Classe qui crée un nouveau champ de complétion."""
    def __init__(self, func, *args, **kwargs):
        """Paramètres: Fonction qui transforme un objet en chaîne, et liste d'objets."""
        super().__init__(*args, **kwargs)

        self.func = func
        self.to_update = []

        self.completion = Gtk.EntryCompletion()

        self.completion.set_inline_selection(True)
        self.completion.set_inline_completion(False)

        self.set_completion(self.completion)
        self.completion.set_text_column(0)
        self.completion.connect('match-selected', self.on_match_selected)

    def fill_entry(self, completions):

        self.completion_list = Gtk.ListStore(str)
        [self.completion_list.append([self.func(item)]) for item in completions]

        self.cdict = dict(((self.func(item), item) for item in completions))

        self.completion.set_model(self.completion_list)

    def on_match_selected(self, completion, model, iter):
        txt = completion.props.model.get_value(iter, 0)
        for comp in self.to_update:
            comp.props.text = comp.func(self.cdict[txt])

if __name__ == '__main__':
    win = Gtk.Window()
    box = Gtk.Box(orientation=1, spacing=6)

    comps = [
        FacturioEntryCompletion(lambda x: x.first_name),
        FacturioEntryCompletion(lambda x: x.last_name),
        FacturioEntryCompletion(lambda x: x.email),
        FacturioEntryCompletion(lambda x: x.address),
        FacturioEntryCompletion(lambda x: x.phone_number)
    ]

    for i in comps:
        i.fill_entry(examples.clients)
        i.to_update = comps
        box.add(i)

    win.add(box)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
