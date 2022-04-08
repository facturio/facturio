import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GObject
import sys
from invoice_hmi import InvoicePage
from home_hmi import MainPage, HeaderBar
from customer_hmi import Customer

class Window(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_hexpand(True)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_vexpand(True)
        self.resize(960, 540)
        provider = Gtk.CssProvider()
        provider.load_from_path("./main.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider,
                                       Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.set_border_width(10)

        self.header_bar = HeaderBar(self)
        self.set_titlebar(self.header_bar)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.
                                       SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)

        self.main_page = MainPage(self)
        self.stack.add_named(self.main_page, "home_page")
        self.invoice_page = InvoicePage()
        self.stack.add_named(self.invoice_page, "invoice_page")
        self.customer_page = Customer()
        self.stack.add_named(self.customer_page, "customer_page")

        self.add(self.stack)

    def initial_show(self):
        self.show_all()
        self.stack.set_visible_child_name("home_page")
        self.header_bar.set_visible(False)


    def switch_page(self, btn=None, page=None):
        if self.stack.get_visible_child_name() != page:
            self.stack.set_visible_child_name(page)
        self.header_bar.switch_toggle(button=None, page=page)


class App(Gtk.Application):
    def __init__(self):
        super().__init__()
        self.connect('activate', self.on_activate)
    def on_activate(self, app):
        self.window = Window()
        self.window.initial_show()
        self.add_window(self.window)


def main():
    app = App()
    app.run(sys.argv)
if __name__ == "__main__":
    main()
