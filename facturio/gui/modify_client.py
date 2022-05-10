#!/usr/bin/env python3
import sqlite3
import gi
from facturio.gui import displayclient
from facturio.gui.page_gui import PageGui
from facturio.classes.client import Client
from facturio.gui.home import HeaderBarSwitcher
from facturio.db.clientdao import ClientDAO
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf


class ModifyClient(PageGui):
    """
    Classe IHM de le fenetre de la modification
    de l'utilisateur
    +--------+
    | --     |
    | --  -- |
    +--------+
    TODO set text
    """
    __instance = None

    @staticmethod
    def get_instance():
        """Renvoie le singleton."""
        if ModifyClient.__instance is None:
            ModifyClient.__instance = ModifyClient()
        return ModifyClient.__instance

    def __init__(self):
        self.dao=ClientDAO.get_instance()
        super().__init__()
        self.header_bar = HeaderBarSwitcher.get_instance()
        self.cent = Gtk.Grid(column_homogeneous=False,
                                  row_homogeneous=False, column_spacing=20,
                                  row_spacing=20)
        self.num_client =0
        if self.num_client != 0:
            self.attr_usr = self.__get_client()
        else:
            self.attr_usr=[""]
        self.client_entries={}
        self.client_label={}
        self.__init_grid()
        self.title__("Modifier Client")
        self.__space_info()
        self.utilisateur()
        self.__swicth_client()

    def __get_client(self):
        """
        Recupere de la bd les info utilisateur
        et les retourne sous forme de liste
        """
        if self.num_client == 0:
            return None
        client = self.dao.get_with_id(self.num_client)
        print("obj=",client)
        return client

    def __init_grid(self):
        """
        Propriete de la Grid Gtk
        voir doc
        """
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.set_column_homogeneous(False)
        self.grid.set_row_homogeneous(False)
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(20)
        return self


    def title__(self, ttl):
        bttl= Gtk.Box()
        self.tl = Gtk.Label()
        self.tl.set_markup("<span font_weight=\"bold\" size=\"xx-large\">"+ttl
                           +"</span>")
        bttl.pack_start(self.tl, False, False, 0)
        self.grid.attach(bttl, 1, 1, 3, 1 )


    def __update_client(self, button):
        """
        Prend un boutton Gtk et un chemin vers la BD
        sqlite et insert les info client
        """
        self.client=self.__entry2client()
        print(self.client.dump_to_list()[:-1])
        if self.is_valid_for_db(self.client.dump_to_list()):
            self.dao.update(self.client)
            self.header_bar.switch_page(None,"customer_page")
        else:
            print("champs incorrect")


    def __entry2client(self):
        """
        Prend le dictrionaire d'entry
        et retourn une instance de client
        """
        res = Client(email=self.client_entries["Mail "].get_text(),
                  address=self.client_entries["Adresse "].get_text(),
                  phone_number=self.client_entries["Numero "].get_text(),
                  first_name=self.client_entries["Prenom "].get_text(),
                  last_name=self.client_entries["Nom "].get_text(),
                  note=self.client_entries["Remarque "].get_text(),
                  id_=self.num_client)
        return res

    def __swicth_client(self):
        switch_box=Gtk.HBox()
        pro = Gtk.RadioButton.new_with_label_from_widget(None, "Entreprise")
        particulier = Gtk.RadioButton.new_from_widget(pro)
        particulier.set_label("Particulier")
        particulier.connect("toggled", self.on_button_toggled, "0")
        pro.connect("toggled", self.on_button_toggled, "1")
        switch_box.pack_start(particulier, True, True, 0)
        switch_box.pack_start(pro, True, True, 0)
        pro.set_mode(False)
        particulier.set_mode(False)
        Gtk.StyleContext.add_class(switch_box.get_style_context(), "linked")
        self.cent.attach(switch_box, 0, 1, 1, 1)


    def on_button_toggled(self, button, pro):
        if button.get_active() and pro=="1":
            self.is_pro=True
            self.client_entries["Entreprise "].show()
            self.client_label["Entreprise "].show()
            self.client_label["Siret "].show()
            self.client_entries["Siret "].show()
            self.is_pro=True
        elif button.get_active():
            self.is_pro=False
            self.client_entries["Entreprise "].hide()
            self.client_label["Entreprise "].hide()
            self.client_entries["Siret "].hide()
            self.client_label["Siret "].hide()


    def utilisateur(self):
        """
        Affichage pour client
        """
        self.imp = Gtk.Button.new_with_label(label="Modifier")
        self.imp.connect("clicked", self.__update_client)
        self.grid.attach(self.cent, 1, 2, 2, 1)
        self.cent.attach(self.imp, 1, 18, 5, 1)
        self.adrss()
        self.mails()
        self.last_name()
        self.first_name()
        self.nums()
        self.entreprise_name()
        self.siret()
        self.rmq()


    def __space_info(self):
        """
        Ajoute les espace
        pour l'ergonomie
        """
        spacel = Gtk.Label("")
        spacel.set_hexpand(True)
        self.grid.attach(spacel, 0, 1, 1, 1)
        spacer = Gtk.Label("")
        spacer.set_hexpand(True)
        self.grid.attach(spacer, 3, 2, 2, 1)
        spaceh = Gtk.Label("")
        self.grid.attach(spaceh, 0, 0, 5, 1)


    def __creat_labelbox(self,c_txt,pos,ind):
        """
        prend un couple de chaine de charactere ainsi que un
        tuple de postion et affhiche un label avec une boite
        """
        label = Gtk.Label()
        label.set_markup("<b>"+c_txt+"</b>:")
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.client_label[c_txt] = label
        self.cent.attach(label,*pos)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.entry.set_text(str(self.attr_usr[0]))
        self.cent.attach(self.entry,pos[0]+1,pos[1],2,1)
        space = Gtk.Label()
        self.cent.attach(space,pos[0],pos[1]+1,3,1)
        self.client_entries[c_txt] = self.entry


    def adrss(self):
        self.__creat_labelbox("Mail ",(3,8,1,1),3)
        return self


    def mails(self):
        self.__creat_labelbox("Adresse ",(0,10,1,1),4)
        return self


    def first_name(self):
        self.__creat_labelbox("Prenom ",(0,5,1,1),3)
        return self

    def last_name(self):
        self.__creat_labelbox("Nom ",(3,5,1,1),2)
        return self

    def nums(self):
        self.__creat_labelbox("Numero ",(3,10,1,1),5)
        return self


    def entreprise_name(self):
        self.__creat_labelbox("Entreprise ",(0,8,1,1),2)
        return self


    def siret(self):
        self.__creat_labelbox("Siret ",(0,13,1,1),6)
        return self


    def rmq(self):
        label = Gtk.Label()
        label.set_markup("<b>Remarque</b>:")
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.client_label["Remarque "] = label
        self.cent.attach(label,0,15,1,1)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.client_entries["Remarque "] = self.entry
        self.cent.attach(self.entry,1,15,5,3)
        return self
