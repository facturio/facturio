#!/usr/bin/env python3
import sqlite3
import gi
from gui.page_gui import Page_Gui
from db.db import Data_base
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf


class Add_Customer(Page_Gui):
    """
    Classe IHM de le fenetre d'ajoute d'un client
    +--------+
    | --     |
    | --  -- |
    +--------+
    """
    def __init__(self):
        super().__init__()
        self.is_pro=False
        self.cent = Gtk.Grid(column_homogeneous=False,
                                  row_homogeneous=False, column_spacing=20,
                                  row_spacing=20)
        self.client_entries={}
        self.client_label={}
        self.db= Data_base("facturio")
        self.__init_grid()
        self.title__("Ajouter Client")
        self.__space_info()
        self.client()
        self.__swicth_client()
        self.client_entries["nom d'entreprise "].hide()
        self.client_label["nom d'entreprise "].hide()
        self.client_entries["Siret "].hide()
        self.client_label["Siret "].hide()


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


    def __add2bd(self, button):
        """
        Prend un boutton Gtk et un chemin vers la BD
        sqlite et insert les info client
        """
        self.info={}
        self.entry.set_text("")
        for section, entry in self.client_entries.items():
            self.info[section] = entry.get_text()
            entry.set_text("")
        self.db.insertion_client_or_company(list(self.info.values())[:-1],0)


    def __swicth_client(self):
        switch_box=Gtk.HBox()
        pro = Gtk.RadioButton.new_with_label_from_widget(None, "Professionnel")
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
            print(self.client_entries)
            print("pro")
            self.client_entries["nom d'entreprise "].show()
            self.client_label["nom d'entreprise "].show()
            self.client_label["Siret "].show()
            self.client_entries["Siret "].show()
            self.is_pro=True
        elif button.get_active():
            self.client_entries["nom d'entreprise "].hide()
            self.client_label["nom d'entreprise "].hide()
            self.client_entries["Siret "].hide()
            self.client_label["Siret "].hide()
            print("not pro")


    def client(self):
        """
        Affichage pour client
        """
        self.imp = Gtk.Button.new_with_label(label="Ajouter")
        self.imp.connect("clicked", self.__add2bd)
        self.grid.attach(self.cent, 1, 2, 2, 1)
        self.cent.attach(self.imp, 2, 13, 3, 1)
        #self.first_name("test")
        self.last_name("test")
        self.adrss("test")
        self.mails("test")
        self.nums("test")
        self.entreprise_name("test")
        self.siret("test")
        self.rmq("test")


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


    def __creat_labelbox(self,c_txt,pos,show=True):
        """
        prend un couple de chaine de charactere ainsi que un
        tuple de postion et affhiche un label avec une boite
        """
        label = Gtk.Label()
        label.set_markup("<b>"+c_txt[0]+"</b>:")
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.client_label[c_txt[0]] = label
        self.cent.attach(label,*pos)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        #self.entry.set_hexpand(True)
        self.cent.attach(self.entry,pos[0]+1,pos[1],2,1)
        space = Gtk.Label()
        self.cent.attach(space,pos[0],pos[1]+1,3,1)
        self.client_entries[c_txt[0]] = self.entry


    def last_name(self,adr):
        self.__creat_labelbox(("Prenom ",adr),(0,3,1,1))
        return self


    def first_name(self,adr):
        self.__creat_labelbox(("Nom ",adr),(0,5,1,1))
        return self


    def adrss(self,adr):
        self.__creat_labelbox(("Mail ",adr),(3,7,1,1))
        return self


    def mails(self,mail):
        self.__creat_labelbox(("adresse ",mail),(0,7,1,1))
        return self


    def nums(self,n):
        self.__creat_labelbox(("Numero ",n),(3,3,1,1))
        return self


    def entreprise(self,ent):
        self.__creat_labelbox(("Remarque ",ent),(3,5,1,1))
        return self

    def entreprise_name(self,ent):
        self.__creat_labelbox(("nom d'entreprise ",ent),(3,9,1,1),False)
        return self

    def siret(self,sir):
        self.__creat_labelbox(("Siret ",sir),(0,9,1,1),False)
        return self

    def rmq(self,sir):
        label = Gtk.Label()
        label.set_markup("<b>Remarque</b>:")
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.client_label["remarque"] = label
        self.cent.attach(label,0,10,1,1)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.cent.attach(self.entry,1,10,5,3)
        return self


    def commentaire(self,adr):
        boxcom= Gtk.Box()
        boxcom.set_name("box_afficher")
        self.com = Gtk.Label(label=adr)
        self.com.set_line_wrap(True)
        self.com.set_max_width_chars(32)
        boxcom.pack_start(self.com, False, False, 0)
        self.grid.attach(boxcom, 4, 10, 3, 3 )

