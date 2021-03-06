#!/usr/bin/env python3
import i18n
import sqlite3
import gi
from facturio.gui.page_gui import PageGui
from facturio.gui.home import HeaderBarSwitcher
from facturio.classes.user import User
from facturio.db.userdao import UserDAO
from facturio import __path__
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
        self.dao=UserDAO.get_instance()
        self.list_att_par=[i18n.t('gui.business'),i18n.t('gui.email'),i18n.t('gui.address'),
                           i18n.t('gui.phone_number'),i18n.t('gui.siret_number')]
        super().__init__()
        self.header_bar = HeaderBarSwitcher.get_instance()
        self.cent = Gtk.Grid(column_homogeneous=False,
                                  row_homogeneous=False, column_spacing=20,
                                  row_spacing=20)
        self.attr_usr= self.__get_user()
        print(self.attr_usr)
        print(self.attr_usr)
        if self.attr_usr==[]:
            self.attr_usr=["","","",
                           "","","",""]
        self.path=self.attr_usr[1]
        self.client_entries={}
        self.client_label={}
        self.__init_grid()
        self.title__(i18n.t('gui.edit_user'))
        self.__space_info()
        self.utilisateur()


    def __get_user(self):
        """
        Recupere de la bd les info utilisateur
        et les retourne sous forme de liste
        """
        self.user= self.dao.get()
        if self.user is None:
            self.user=User("Aucun", "Aucun", "Aucun",
                           "Aucun", "Aucun", 0,0,
                           __path__[0] + "/data/icons/Moi.png",1)
            print(self.user)
            self.dao.insert(self.user)
        list_client=self.user.dump_to_list()
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
            print(i18n.t('gui.no_logo'))
            return None
        print("avant path=",self.info)
        self.info.append(self.path)
        print("apres path=",self.info)
        for i in self.list_att_par:
            self.info.append(self.client_entries[i].get_text())
        if self.is_usr_valid_for_db(self.info):
            self.info.append("1")
            print("info=",self.info)
            self.dao.update_user(self.user)
            self.header_bar.switch_page(None,"home_page")
        else:
            print("champs incorrect")




    def utilisateur(self):
        """
        Affichage pour client
        """
        self.logo_button = Gtk.Button.new_from_icon_name("image-x-generic-symbolic",
                                                    Gtk.IconSize.BUTTON)
        self.logo_button.set_label('+ Logo')
        self.logo_button.set_always_show_image(True)
        self.logo_button.set_hexpand(True)
        self.cent.attach(self.logo_button, 5, 11, 2, 1)
        self.logo_fn = None
        self.logo_button.connect("clicked", self._logo_dialog)
        self.imp = Gtk.Button.new_with_label(label=i18n.t('gui.edit'))
        self.imp.connect("clicked", self.__add2bd)
        self.grid.attach(self.cent, 1, 2, 2, 1)
        self.cent.attach(self.imp, 2, 16, 5, 1)
        self.first_name()
        self.last_name()
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
        self.entry.set_text(str(self.attr_usr[ind]))
        self.cent.attach(self.entry,pos[0]+1,pos[1],2,1)
        space = Gtk.Label()
        self.cent.attach(space,pos[0],pos[1]+1,3,1)
        self.client_entries[c_txt] = self.entry


    def adrss(self):
        self.__creat_labelbox(i18n.t('gui.email'),(4,5,1,1),2)
        return self


    def mails(self):
        self.__creat_labelbox(i18n.t('gui.address'),(4,7,1,1),3)
        return self


    def nums(self):
        self.__creat_labelbox(i18n.t('gui.phone_number'),(1,7,1,1),4)
        return self


    def entreprise_name(self):
        self.__creat_labelbox(i18n.t('gui.business'),(1,5,1,1),1)
        return self

    def _logo_dialog(self, *args):
        file_chooser = Gtk.FileChooserNative(title=i18n.t('gui.select_picture'),
                                             accept_label=i18n.t('gui.select'),
                                             cancel_label=i18n.t('gui.cancel'))
        filter_ = Gtk.FileFilter()
        filter_.set_name(i18n.t('gui.pictures'))
        filter_.add_pattern("*.jpg")
        filter_.add_pattern("*.png")
        filter_.add_pattern("*.jpeg")
        file_chooser.set_filter(filter_)
        if file_chooser.run() == Gtk.ResponseType.ACCEPT:
           self.path = file_chooser.get_filename()
           self.logo_button.set_sensitive(False)
           self.logo_button.set_label(i18n.t('gui.added'))


    def siret(self):
        self.__creat_labelbox(i18n.t('gui.siret_number'),(1,11,1,1),7)
        return self

    def first_name(self):
        self.__creat_labelbox("Prenom ",(1,2,1,1),6)
        return self

    def last_name(self):
        self.__creat_labelbox("Nom ",(4,2,1,1),5)
        return self

    def rmq(self):
        label = Gtk.Label()
        label.set_markup("<b>" + i18n.t('gui.remark') + "</b>:")
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.client_label[i18n.t('gui.remark')] = label
        self.cent.attach(label,0,13,1,1)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.client_entries[i18n.t('gui.remark')] = self.entry
        self.cent.attach(self.entry,1,13,5,3)
        return self
