#!/usr/bin/env python3
import i18n
import sqlite3
import gi
from facturio.classes.client import Client, Company
from facturio.gui.home import HeaderBarSwitcher
from facturio.gui.page_gui import PageGui
from facturio.db.clientdao import ClientDAO
from facturio.db.companydao import CompanyDAO
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf


class Add_Customer(PageGui):
    """
    Classe IHM de le fenetre d'ajoute d'un client
    +--------+
    | --     |
    | --  -- |
    +--------+
    """
    #TODO fix bug rmq
    def __init__(self):
        self.list_att_par=[i18n.t('gui.surname'),i18n.t('gui.name'),i18n.t('gui.email'),i18n.t('gui.address'),
                           i18n.t('gui.phone_number'), i18n.t('gui.remark')]
        super().__init__()
        self.dao=ClientDAO.get_instance()
        self.cdao=CompanyDAO.get_instance()
        self.is_pro=True
        self.header_bar = HeaderBarSwitcher.get_instance()
        self.cent = Gtk.Grid(column_homogeneous=False,
                                  row_homogeneous=False, column_spacing=20,
                                  row_spacing=20)
        self.client_entries={}
        self.client_space={}
        self.client_label={}
        self.__init_grid()
        self.title__(i18n.t('gui.add_client'))
        self.__space_info()
        self.client()
        self.__swicth_client()


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
        self.entry.set_text("")
        for i in self.list_att_par:
            # print(i)
            self.info.append(self.client_entries[i].get_text())
            self.client_entries[i].set_text("")
        if self.is_pro:
            self.info.append(self.client_entries[i18n.t('gui.business')].get_text())
            self.client_entries[i18n.t('gui.business')].set_text("")
            self.info.append(self.client_entries[i18n.t('gui.siret_number')].get_text())
            self.client_entries[i18n.t('gui.siret_number')].set_text("")
            if self.is_valid_for_db(self.info) and self.info[-1].isnumeric():
                # print("info",self.info)
                Cls=Company(self.info[6],self.info[0], self.info[1], self.info[2],
                           self.info[3], self.info[4], self.info[5],self.info[7])
                self.cdao.insert(Cls)
                self.header_bar.switch_page(None,"home_page")
            else:
                pass
                # print("champs incorrect")
        else:
            if self.is_valid_for_db(self.info):
                Cls=Client(self.info[0], self.info[1], self.info[2],
                           self.info[3], self.info[4], self.info[5],)
                self.dao.insert(Cls)
                self.header_bar.switch_page(page="home_page")
            else:
                pass
                # print("champs incorrect")


    def __swicth_client(self):
        switch_box=Gtk.HBox()
        pro = Gtk.RadioButton.new_with_label_from_widget(None, i18n.t('gui.business'))
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
            self.client_entries[i18n.t('gui.business')].show()
            self.client_label[i18n.t('gui.business')].show()
            self.client_label[i18n.t('gui.siret_number')].show()
            self.client_entries[i18n.t('gui.siret_number')].show()
            self.is_pro=True
        elif button.get_active():
            self.is_pro=False
            self.client_entries[i18n.t('gui.business')].hide()
            self.client_label[i18n.t('gui.business')].hide()
            self.client_space[i18n.t('gui.business')].hide()
            self.client_entries[i18n.t('gui.siret_number')].hide()
            self.client_label[i18n.t('gui.siret_number')].hide()
            self.client_space[i18n.t('gui.siret_number')].hide()


    def client(self):
        """
        Affichage pour client
        """
        self.imp = Gtk.Button.new_with_label(label=i18n.t('gui.add'))
        self.imp.connect("clicked", self.__add2bd)
        self.grid.attach(self.cent, 1, 2, 2, 1)
        self.cent.attach(self.imp, 1, 16, 5, 1)
        self.first_name()
        self.last_name()
        self.adrss()
        self.mails()
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
        self.grid.attach(spacer, 3, 1, 1, 1)


    def __creat_labelbox(self,c_txt,pos):
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
        self.cent.attach(self.entry,pos[0]+1,pos[1],2,1)
        self.space = Gtk.Label()
        self.cent.attach(self.space,pos[0],pos[1]+1,3,1)
        self.client_entries[c_txt] = self.entry
        self.client_space[c_txt] = self.space


    def last_name(self):
        self.__creat_labelbox(i18n.t('gui.name'),(0,3,1,1))
        return self


    def first_name(self):
        self.__creat_labelbox(i18n.t('gui.surname'),(3,3,1,1))
        return self


    def adrss(self):
        self.__creat_labelbox(i18n.t('gui.email'),(3,5,1,1))
        return self


    def mails(self):
        self.__creat_labelbox(i18n.t('gui.address'),(0,7,1,1))
        return self


    def nums(self):
        self.__creat_labelbox(i18n.t('gui.phone_number'),(0,5,1,1))
        return self


    def entreprise(self):
        self.__creat_labelbox(i18n.t('gui.remark'),(3,5,1,1))
        return self


    def entreprise_name(self):
        self.__creat_labelbox(i18n.t('gui.business'),(3,7,1,1))
        return self


    def siret(self):
        self.__creat_labelbox(i18n.t('gui.siret_number'),(0,11,1,1))
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

