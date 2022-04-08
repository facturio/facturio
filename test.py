#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Window(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Scrollbar")
        self.set_default_size(200, 200)
        self.connect("destroy", Gtk.main_quit)

        grid = Gtk.Grid()
        self.add(grid)

        layout = Gtk.Layout()
        layout.set_size(800, 500)
        layout.set_vexpand(True)
        layout.set_hexpand(True)

        button = Gtk.Button(label="Button 1")
        layout.put(button, 300, 400)
        button = Gtk.Button(label="Button 2")
        layout.put(button, 150, 50)
        button = Gtk.Button(label="Button 3")
        layout.put(button, 720, 470)
        grid.attach(layout, 0, 0, 1, 1)

        vadjustment = layout.get_vadjustment()
        hadjustment = layout.get_hadjustment()

        vscrollbar = Gtk.Scrollbar(orientation=Gtk.Orientation.VERTICAL,
                                   adjustment=vadjustment)
        grid.attach(vscrollbar, 1, 0, 1, 1)
        hscrollbar = Gtk.Scrollbar(orientation=Gtk.Orientation.HORIZONTAL,
                                   adjustment=hadjustment)
        grid.attach(hscrollbar, 0, 1, 1, 1)

window = Window()
window.show_all()

Gtk.main()
