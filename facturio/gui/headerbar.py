import i18n
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


class ButtonIcon(Gtk.RadioButton):
    """
    Spécialise la classe Gtk.RadioButton en ajoutant un icon et un label
    """
    def __init__(self, label, icon_name):
        super().__init__()
        self.icon_name = icon_name
        self.label = label
        self.icon = Gio.ThemedIcon(name=self.icon_name)
        self.image = Gtk.Image.new_from_gicon(self.icon, Gtk.IconSize.BUTTON)
        self.set_image(self.image)
        self.set_label(self.label)
        self.set_always_show_image(True)
        self.set_mode(False)

class HeaderBarSwitcher(Gtk.HeaderBar):
    """
    Spécialise la classe Gtk.HeaderBar en ajoutant un stack qui nous
    permet de changer de page comme StackSwitcher avec un meilleur
    style
    """
    __instance = None

    def get_instance():
        """Renvoie le singleton."""
        if HeaderBarSwitcher.__instance is None:
            HeaderBarSwitcher.__instance = HeaderBarSwitcher()
        return HeaderBarSwitcher.__instance

    def __init__(self):
        super().__init__()
        self.stack = None
        self.set_has_subtitle(False)
        self.set_show_close_button(True)
        # button invisible pour les pages qui n'apparaisent pas sur
        # l'header bar
        self.invisible_btn = Gtk.RadioButton()

        # dict avec l'ensemble des buttons qui propose le changement de page
        self.button_dict = {}

        # Création et affichage du button home
        btn = ButtonIcon("", "go-home-symbolic")
        self.button_dict["home_page"] = btn
        btn.connect("clicked", self.switch_page, "home_page")
        btn.join_group(self.invisible_btn)
        self.pack_start(btn)

        # box contenant tout les buttons du centre
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        # Gtk.StyleContext.add_class(self.box.get_style_context(), "linked")
        # création des buttons et ajout dans self.box
        self.__init_buttons()
        self.set_custom_title(self.box)


    def set_stack(self, stack: Gtk.Stack):
        self.stack = stack

    def get_stack(self):
        return self.stack


    def __init_buttons(self):
        """
        Création des buttons du milieu et ajout dans self.box
        """
        page_names = ("invoice_page", "estimate_page", "customer_page")
        labels = (i18n.t('home.invoice'), i18n.t('home.estimate'), i18n.t('home.client'))
        icons = ("emblem-documents-symbolic", "x-office-document-symbolic",
                 "system-users-symbolic")
        for name, label, icon in zip(page_names, labels, icons):
            self.button_dict[name] = ButtonIcon(label, icon)
            self.button_dict[name].connect("clicked", self.switch_page, name)
            self.button_dict[name].join_group(self.invisible_btn)
            self.box.pack_start(self.button_dict[name], True, True, 10)


    def set_visible(self, flag: bool):
        """
        Change la visibilité selon la flag des tous le buttons
        dans la header bar
        """
        if flag:
            self.button_dict["home_page"].set_visible(True)
            self.box.set_visible(True)
        else:
            self.button_dict["home_page"].set_visible(False)
            self.box.set_visible(False)

    def switch_page(self, btn: Gtk.Button = None, page: str = None):
        """
        Change de page.

        Si la page est home on cache la header bar
        """
        if page is None:
            raise ValueError
        if self.stack:
            self.stack.set_visible_child_name(page)


            # if self.stack.get_visible_child_name() != page:
            #     if page == "home_page":
            #         self.set_visible(False)
            #     else:
            #         self.set_visible(True)
            #     self.stack.set_visible_child_name(page)


    def active_button(self, btn: Gtk.Button = None, page: str = None):
        "active le button en déclanchant une signal si besoin"
        if page in self.button_dict:
            self.button_dict[page].set_active(True)
        else:
            self.invisible_btn.set_active(True)
            self.switch_page(btn, page)
