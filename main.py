#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
from omnisearch import FacturioOmnisearch


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Facturio")

        self.resize(1920, 1080)
        self.set_hexpand(False)
        provider = Gtk.CssProvider()
        provider.load_from_path("./main.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        #grid
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(20)

        # spaces
        self.space = Gtk.Label(label="")
        self.grid.attach(self.space,1,1,10,1)

        # logo
        self.facturio_label = Gtk.Label(label="Facturio")
        self.grid.attach(self.facturio_label, 3, 2, 6, 1 )

        self.space = Gtk.Label(label="")
        self.grid.attach(self.space,1,4,10,1)

        #search bar
        self.searchbar = FacturioOmnisearch()
        self.grid.attach(self.searchbar.box, 3, 3, 6, 2)

        #icons
        self.invoice_icon = Gtk.Image.new_from_file("./icons/Plus.png")
        # self.evbox= Gtk.EventBox()
        # self.evbox.add(self.invoice_icon)
        # self.evbox.connect("button-press-event", self.on_box_clicked)
        W_Weight, W_Height=self.get_size()
        print(type(W_Height))
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename='./icons/Plus.png', width=240000/W_Weight, height=240000/W_Height, preserve_aspect_ratio=True)
        img = Gtk.Image.new_from_pixbuf(pixbuf)
        self.button = Gtk.Button()
        self.button.add(img)
        self.grid.attach(self.button, 3, 5, 2, 1)

        self.button2 = Gtk.Button(label="Historique")
        self.grid.attach(self.button2, 5, 5, 2, 1)

        self.button3 = Gtk.Button(label="Devis")
        self.grid.attach(self.button3, 7, 5, 2, 1)

        self.button4 = Gtk.Button(label="Carte")
        self.grid.attach(self.button4, 3, 6, 2, 1)

        self.button5 = Gtk.Button(label="Client")
        self.grid.attach(self.button5, 5, 6, 2, 1)

        self.button6 = Gtk.Button(label="Moi")
        self.grid.attach(self.button6, 7, 6, 2, 1)

        # spaces
        self.space = Gtk.Label(label="")
        self.grid.attach(self.space,1,7,10,1)
        self.space = Gtk.Label(label="")
        self.grid.attach(self.space,1,8,10,1)

        # self.button4 = Gtk.Button(label="Facture")
        # self.grid.attach(self.button, 3, 4, 2, 1)

        # self.button5 = Gtk.Button(label="Facture")
        # self.grid.attach(self.button, 3, 4, 2, 1)

        # self.button6 = Gtk.Button(label="Facture")
        # self.grid.attach(self.button, 3, 4, 2, 1)
        # self.evbox.set_above_child(self.box)
        # self.box= Gtk.Box(spacing=6)
        # self.box1= Gtk.Box()
        # self.evbox.set_visible_window(True)
        # self.add(self.box)
        # self.button = Gtk.Button(label="Click Here")
        # self.button2 = Gtk.Button()
        # self.button2.set_always_show_image(True)
        # self.box.pack_start(self.button2, False, False, 0)
        # self.button.connect("clicked", self.on_button_clicked)
        # self.box.pack_start(self.button, False, False, 0)
        # self.box.pack_start(self.box1, False, False, 0)
        # self.box.pack_start(self.evbox, False, False, 0)

    def on_button_clicked(self, widget):
        print("Hello World")
    def on_box_clicked(self, widget, x):
        print("xd")
        print("Hello World")

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
