#!/usr/bin/env python3
import gi
from gui.page_gui import Page_Gui
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
        self.cent = Gtk.Grid(column_homogeneous=False,
                                  row_homogeneous=False, column_spacing=20,
                                  row_spacing=20)
        self.client_entries={}
        self.__init_grid()
        self.title__("Ajouter Client")
        self.__space_info()
        self.client()


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
        self.tl.set_markup("<span font_weight=\"bold\" size=\"xx-large\">"+ttl+"</span>")
        bttl.pack_start(self.tl, False, False, 0)
        self.grid.attach(bttl, 2, 1, 3, 1 )


    def client(self):
        """
        Affichage pour client
        """
        self.imp = Gtk.Button(label="Ajouter")
        self.grid.attach(self.cent, 1, 2, 2, 1)
        self.cent.attach(self.imp, 4, 8, 2, 1)
        self.first_name("test")
        self.last_name("test")
        self.adrss("test")
        self.mails("test")
        self.nums("test")
        self.entreprise("test")
        self.siret("test")


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


    def __creat_labelbox(self,c_txt,pos):
        """
        prend un couple de chaine de charactere ainsi que un
        tuple de postion et affhiche un label avec une boite
        """
        label = Gtk.Label()
        label.set_markup("<b>"+c_txt[0]+"</b>:")
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.cent.attach(label,*pos)
        entry = Gtk.Entry()
        self.cent.attach(entry,pos[0]+1,pos[1],2,1)
        self.client_entries[c_txt[0]] = entry
        space = Gtk.Label()
        self.cent.attach(space,pos[0],pos[1]+1,3,1)

    def last_name(self,adr):
        self.__creat_labelbox(("Nom ",adr),(0,2,1,1))
        return self

    def first_name(self,adr):
        self.__creat_labelbox(("Prenom ",adr),(0,4,1,1))
        return self

    def adrss(self,adr):
        self.__creat_labelbox(("Adresse ",adr),(0,6,1,1))
        return self


    def mails(self,mail):
        self.__creat_labelbox(("Mail ",mail),(0,8,1,1))
        return self


    def nums(self,n):
        self.__creat_labelbox(("Numero ",n),(3,2,1,1))
        return self


    def entreprise(self,ent):
        self.__creat_labelbox(("entreprise ",ent),(3,4,1,1))
        return self


    def siret(self,sir):
        self.__creat_labelbox(("Siret ",sir),(3,6,1,1))
        return self


    def commentaire(self,adr):
        boxcom= Gtk.Box()
        boxcom.set_name("box_afficher")
        self.com = Gtk.Label(label=adr)
        self.com.set_line_wrap(True)
        self.com.set_max_width_chars(32)
        boxcom.pack_start(self.com, False, False, 0)
        self.grid.attach(boxcom, 4, 10, 3, 3 )

