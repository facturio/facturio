#!/usr/bin/env python3
import sqlite3
import gi
from gui.page_gui import PageGui
from db.db import Data_base
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf


class ModifyUsr(PageGui):
    """
    Classe IHM de le fenetre de la modification
    de l'utilisateur
    +--------+
    | --     |
    | --  -- |
    +--------+
    """
    def __init__(self):
        self.list_att_par=["Entreprise ","Mail ","Adresse ",
                           "Numero ","Siret "]
        super().__init__()
        self.cent = Gtk.Grid(column_homogeneous=False,
                                  row_homogeneous=False, column_spacing=20,
                                  row_spacing=20)
        self.attr_usr=self.__get_user()
        if self.attr_usr==[]:
            self.attr_usr=[["","","",
                           "","","",""]]
        self.path=self.attr_usr[0][1]
        self.client_entries={}
        self.client_label={}
        self.__init_grid()
        self.title__("Modifier Utilisateur")
        self.__space_info()
        self.utilisateur()

    def __get_user(self):
        """
        Recupere de la bd les info utilisateur
        et les retourne sous forme de liste
        """
        list_client= self.db.selection_table("user")
        return list_client

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
        self.info=[]
        if self.path == None:
            print("pas de logo")
            return None
        print("avant path=",self.info)
        self.info.append(self.path)
        print("apres path=",self.info)
        for i in self.list_att_par:
            self.info.append(self.client_entries[i].get_text())
        if self.is_usr_valid_for_db(self.info):
            self.info.append("1")
            print("info=",self.info)
            self.db.update_user(self.info)
        else:
            print("champs incorrect")


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
        self.logo_button = Gtk.Button.new_from_icon_name("image-x-generic-symbolic",
                                                    Gtk.IconSize.BUTTON)
        self.logo_button.set_label('+ Logo')
        self.logo_button.set_always_show_image(True)
        self.logo_button.set_hexpand(True)
        self.cent.attach(self.logo_button, 4, 11, 2, 1)
        self.logo_fn = None
        self.logo_button.connect("clicked", self._logo_dialog)
        self.imp = Gtk.Button.new_with_label(label="Modifier")
        self.imp.connect("clicked", self.__add2bd)
        self.grid.attach(self.cent, 1, 2, 2, 1)
        self.cent.attach(self.imp, 1, 16, 5, 1)
        self.adrss()
        self.mails()
        self.nums()
        self.entreprise_name()
        self.siret()


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
        self.entry.set_text(str(self.attr_usr[0][ind]))
        self.cent.attach(self.entry,pos[0]+1,pos[1],2,1)
        space = Gtk.Label()
        self.cent.attach(space,pos[0],pos[1]+1,3,1)
        self.client_entries[c_txt] = self.entry


    def adrss(self):
        self.__creat_labelbox("Mail ",(3,5,1,1),3)
        return self


    def mails(self):
        self.__creat_labelbox("Adresse ",(0,7,1,1),4)
        return self


    def nums(self):
        self.__creat_labelbox("Numero ",(3,7,1,1),5)
        return self


    def entreprise_name(self):
        self.__creat_labelbox("Entreprise ",(0,5,1,1),2)
        return self

    def _logo_dialog(self, *args):
        file_chooser = Gtk.FileChooserNative(title="Selectionnez une image",
                                             accept_label="Selectionner",
                                             cancel_label="Annuler")
        filter_ = Gtk.FileFilter()
        filter_.set_name("Images")
        filter_.add_pattern("*.jpg")
        filter_.add_pattern("*.png")
        filter_.add_pattern("*.jpeg")
        file_chooser.set_filter(filter_)
        if file_chooser.run() == Gtk.ResponseType.ACCEPT:
           self.path = file_chooser.get_filename()
           self.logo_button.set_sensitive(False)
           self.logo_button.set_label(" Ajouté")


    def siret(self):
        self.__creat_labelbox("Siret ",(0,11,1,1),6)
        return self


    def rmq(self):
        label = Gtk.Label()
        label.set_markup("<b>Remarque</b>:")
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.client_label["Remarque "] = label
        self.cent.attach(label,0,13,1,1)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.client_entries["Remarque "] = self.entry
        self.cent.attach(self.entry,1,13,5,3)
        return self
