#!/usr/bin/env python3
"""Module de création de champs d'autocomplétion."""

import facturio.examples as examples
import gi
import re
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk  # noqa: E402


class FacturioOmnisearch(Gtk.SearchEntry):
    """Classe qui crée un nouveau champ de complétion."""
    def __init__(self, list, *args, **kwargs):
        """Paramètres: Fonction qui transforme un objet en chaîne, et liste d'objets."""
        super().__init__(*args, **kwargs)

        self.completion = Gtk.EntryCompletion()
        self.set_completion(self.completion)
        self.num=None

        self.complist = Gtk.ListStore(str)
        [self.complist.append([str(i)]) for i in list]

        self.completion.set_model(self.complist)
        self.completion.set_match_func(facturio_match_func)

        self.go_to=False
        self.completion.set_inline_selection(True)
        self.completion.set_inline_completion(False)
        self.completion.set_text_column(0)


def facturio_match_func(completion, key, iter, *user_data):
    k = re.compile('.*' + re.escape(key) + '.*')
    return re.match(k, completion.props.model.get_value(iter, 0))

if __name__ == '__main__':
    win = Gtk.Window()

    box = Gtk.Box(orientation=1, spacing=6)
    fn = FacturioOmnisearch(examples.clients)
    box.add(fn)

    win.add(box)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
