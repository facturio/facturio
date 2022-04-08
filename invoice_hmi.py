#!/usr/bin/env python3
from gi.repository import Gtk
class InvoicePage(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        self.grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 1, 1, 10, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 1, 2, 10, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 1, 3, 10, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 1, 4, 10, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 1, 5, 10, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 1, 6, 10, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 1, 7, 10, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 1, 8, 10, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 1, 9, 10, 1)
        self.add(self.grid)
