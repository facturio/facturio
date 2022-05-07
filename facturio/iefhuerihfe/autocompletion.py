#!/usr/bin/env python3
"""Module de création de champs d'autocomplétion."""

import facturio.examples as examples
import gi
import re
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk  # noqa: E402


class FacturioEntryCompletion(Gtk.Entry):
    """Classe qui crée un nouveau champ de complétion."""
    def __init__(self, func, completions):
        """Paramètres: Fonction qui transforme un objet en chaîne, et liste d'objets."""
        super().__init__()

        self.func = func
        self.to_update = []

        self.completion = Gtk.EntryCompletion()

        self.completion.set_inline_selection(True)
        self.completion.set_inline_completion(True)

        self.set_completion(self.completion)

        self.completion_list = Gtk.ListStore(str)
        [self.completion_list.append([func(item)]) for item in completions]

        self.completion.set_model(self.completion_list)
        self.completion.set_text_column(0)
        self.completion.connect('match-selected', self.on_match_selected)

    def on_match_selected(self, completion, model, iter):
        txt = completion.props.model.get_value(iter, 0)
        for comp in self.to_update:
            comp.props.text = txt

if __name__ == '__main__':
    win = Gtk.Window()
    box = Gtk.Box(orientation=1, spacing=6)

    fn = FacturioEntryCompletion(lambda x: x.first_name, examples.clients)
    ln = FacturioEntryCompletion(lambda x: x.last_name, examples.clients)
    ml = FacturioEntryCompletion(lambda x: x.email, examples.clients)
    adr = FacturioEntryCompletion(lambda x: x.adress, examples.clients)
    tel = FacturioEntryCompletion(lambda x: x.phone_number, examples.clients)

    fn.to_update = [ln, ml, adr, tel]
    ln.to_update = [fn, ml, adr, tel]
    ml.to_update = [fn, ln, adr, tel]
    adr.to_update = [fn, ln, ml, tel]
    tel.to_update = [fn, ln, ml, adr]

    box.add(fn)
    box.add(ln)
    box.add(ml)
    box.add(adr)
    box.add(tel)

    win.add(box)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
