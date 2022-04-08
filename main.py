#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GObject
import sys

class ButtonIcon(Gtk.ToggleButton):
    def __init__(self, label, icon_name):
        super().__init__()
        self.icon_name = icon_name
        self.label = label
        self.icon = Gio.ThemedIcon(name=self.icon_name)
        self.image = Gtk.Image.new_from_gicon(self.icon, Gtk.IconSize.BUTTON)
        self.set_image(self.image)
        self.set_label(self.label)
        self.set_always_show_image(True)

class HeaderBar(Gtk.HeaderBar):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.set_has_subtitle(False)
        self.set_show_close_button(True)
        # Creation et activation du button home
        self.home_button = ButtonIcon("", "go-home-symbolic")
        self.home_button.set_active(True)
        self.active_now = self.home_button
        self.home_button.connect('toggled', self.home_func)
        self.pack_start(self.home_button)

        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.box.get_style_context(), "linked")

        self.user_button = ButtonIcon("Utilisateur", "avatar-default-symbolic")
        self.user_button.connect('toggled', self.switch_toggle)
        self.box.pack_start(self.user_button, True, True, 10)

        self.quotation_button = ButtonIcon("Devis",
                                           "x-office-document-symbolic")
        self.quotation_button.connect('toggled', self.switch_toggle)
        self.box.pack_start(self.quotation_button, True, True, 10)

        self.invoice_button = ButtonIcon("Factures",
                                         "emblem-documents-symbolic")
        self.invoice_button.connect('toggled', self.invoice_func)
        self.box.pack_start(self.invoice_button, True, True, 10)

        self.customer_button = ButtonIcon("Clients", "system-users-symbolic")
        self.customer_button.connect('toggled', self.customer_func)
        self.box.pack_start(self.customer_button, True, True, 10)
        self.set_custom_title(self.box)
    def set_visible(self, flag: bool):
        if flag:
            self.home_button.set_visible(True)
            self.box.set_visible(True)
        else:
            self.home_button.set_visible(False)
            self.box.set_visible(False)

    def switch_toggle(self, button):
        if button != self.active_now :
            self.active_now.set_active(False)
            self.active_now = button
    def customer_func(self, button):
        self.switch_toggle(button)
        self.box.set_visible(False)
        self.home_button.set_visible(False)

    def invoice_func(self, button):
        self.switch_toggle(button)
        self.window.switch_invoice_page()

    def home_func(self, button):
        self.switch_toggle(button)
        self.set_visible(False)
        self.window.switch_home_page()

class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_hexpand(False)
        provider = Gtk.CssProvider()
        provider.load_from_path("./main.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider,
                                       Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.set_border_width(10)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.
                                       SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)

        self.display_main_page()
        self.header_bar = HeaderBar(self)
        self.set_titlebar(self.header_bar)
        self.stack.add_titled(self.grid, "home_page", "")
        self.invoice_page()
        self.stack.add_titled(self.scrll_win, "invoice_page", "")
        # Creating label .
        label = Gtk.Label()
        label.set_markup("<big>Hello World</big>")
        self.stack.add_titled(label, "label", "Label")

        self.add(self.stack)
        # self.stack.connect("notify::visible-child-name", self.vc_changed)

    def initial_show(self):
        self.show_all()
        self.header_bar.set_visible(False)

    def invoice_page(self):
        self.scrll_win= Gtk.ScrolledWindow()
        self.view_port = Gtk.Viewport()
        self.fact_grid = Gtk.Grid()

        self.view_port.add(self.fact_grid)
        self.scrll_win.add(self.view_port)

        self.fact_grid.set_column_homogeneous(True)
        self.fact_grid.set_row_homogeneous(True)
        self.fact_grid.set_row_spacing(20)
        self.fact_grid.set_column_spacing(20)

        space = Gtk.Label("")
        self.fact_grid.attach(space,1,1,10,1)
        # self.entry = Gtk.Entry()
        # self.fact_grid.attach(self.entry, 1, 1, 10, 1)
        self.entry = Gtk.Entry()
        self.fact_grid.attach(self.entry, 1, 2, 10, 1)
        self.entry = Gtk.Entry()
        self.fact_grid.attach(self.entry, 1, 3, 10, 1)
        self.entry = Gtk.Entry()
        self.fact_grid.attach(self.entry, 1, 4, 10, 1)
        self.entry = Gtk.Entry()
        self.fact_grid.attach(self.entry, 1, 5, 10, 1)
        self.entry = Gtk.Entry()
        self.fact_grid.attach(self.entry, 1, 6, 10, 1)
        self.entry = Gtk.Entry()
        self.fact_grid.attach(self.entry, 1, 7, 10, 1)
        self.entry = Gtk.Entry()
        self.fact_grid.attach(self.entry, 1, 8, 10, 1)
        self.entry = Gtk.Entry()
        self.fact_grid.attach(self.entry, 1, 9, 10, 1)
        return


    def vc_changed(self, stack, gparamstring):
        vc = stack.get_visible_child()
        if vc == self.grid:
            self.stack_switcher.hide()
        else:
            self.stack_switcher.show()
        print("visible child changed")



    def display_main_page(self):
        self.grid = Gtk.Grid()
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
        self.searchbar = Gtk.SearchEntry()
        self.grid.attach(self.searchbar, 3, 3, 6, 1)

        #icons
        self.invoice_icon= Gtk.Image.new_from_file("./icons/Plus.png")
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
        self.button.connect("clicked", self.switch_invoice_page)

        self.button2 = Gtk.Button(label="Historique")
        self.grid.attach(self.button2, 5, 5, 2, 1)

        self.button3 = Gtk.Button(label="Devis")
        self.grid.attach(self.button3, 7, 5, 2, 1)
        self.button3.connect("clicked", self.on_button_clicked)

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


    def switch_home_page(self):
        if self.stack.get_visible_child_name() != "home_page":
            self.stack.set_visible_child_name("home_page")

    def switch_invoice_page(self, button=None):
        print(self.stack.get_visible_child_name())
        if button:
            self.header_bar.invoice_button.set_active(True)
        if self.stack.get_visible_child_name() != "invoice_page":
            self.header_bar.set_visible(True)
            self.stack.set_visible_child_name("invoice_page")

    def on_button_clicked(self, widget):
        print("Hello World")
    def on_box_clicked(self, widget, x):
        print("xd")
        print("Hello World")


class App(Gtk.Application):
    def __init__(self):
        super().__init__()
        self.connect('activate', self.on_activate)
    def on_activate(self, app):
        self.window = MyWindow()
        self.window.initial_show()
        self.add_window(self.window)

# win = MyWindow()
app = App()
app.run(sys.argv)
# win.connect("destroy", Gtk.main_quit)
# win.show_all()
# Gtk.main()
