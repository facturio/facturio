from os import EX_USAGE
import gi
from facturio.gui import modify_client
from facturio.gui.home import HeaderBarSwitcher
gi.require_version("Gtk", "3.0")
from facturio.classes.user import User
from facturio.classes.client import Client
from facturio.gui.add_customer import Add_Customer
from facturio.gui.modify_client import ModifyClient
gi.require_version("OsmGpsMap", "1.0")
from facturio.gui.page_gui import PageGui
from facturio.db.companydao import CompanyDAO
from facturio.db.clientdao import ClientDAO
from facturio import __path__
gi.require_version("Gtk", "3.0")
gi.require_version("OsmGpsMap", "1.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, OsmGpsMap

class DisplayClient (PageGui):
    """
    Classe IHM de le fenetre d'affichage, elle permet soit d'afficher la page
    d'utilisateur soit la page d'un client
    +--------+
    |---  == |
    |---  -- |
    +--------+
    """
    __instance = None
    num_client=0
    entrys={}
    label={}
    buttons={}
    is_pro=False

    @staticmethod
    def get_instance():
        """Renvoie le singleton."""
        if DisplayClient.__instance is None:
            DisplayClient.__instance = DisplayClient()
        return DisplayClient.__instance


    def __init__(self,is_ut=False,num_client=0,*args, **kwargs):
        super().__init__()
        self.dao=ClientDAO.get_instance()
        self.cdao=CompanyDAO.get_instance()
        self.num_client=DisplayClient.num_client
        self.is_ut=is_ut
        print("is_pro=",DisplayClient.is_pro)
        self.num_client=int(num_client)
        DisplayClient.num_client=int(num_client)
        self.header_bar = HeaderBarSwitcher.get_instance()
        super().__init__(*args, **kwargs)
        self.cent = Gtk.Grid(column_homogeneous=False,
                                  row_homogeneous=False, column_spacing=20,
                                  row_spacing=20)
        self.__init_grid()
        self.grid.attach(self.cent, 1, 2, 2, 1)
        self.__space_info()
        if DisplayClient.__instance is None:
            self.ini_page()
        else:
                self.update2client()
        if self.is_ut:
            DisplayClient.entrys["Siret "].show()
            DisplayClient.label["Siret "].show()
            DisplayClient.entrys["Entreprise "].show()
            DisplayClient.label["Entreprise "].show()
            DisplayClient.entrys["Siret "].set_text("ESTUN")
            DisplayClient.entrys["Entreprise "].set_text("ESTUN")
        else:
            DisplayClient.entrys["Siret "].hide()
            DisplayClient.label["Siret "].hide()
            DisplayClient.entrys["Entreprise "].hide()
            DisplayClient.label["Entreprise "].hide()

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


    def __title(self, ttl):
        bttl= Gtk.Box()
        bttl.set_name("name")
        self.tl = Gtk.Label()
        self.tl.set_markup("<span font_weight=\"bold\" size=\"xx-large\">"+ttl+"</span>")
        bttl.pack_start(self.tl, False, False, 0)
        self.grid.attach(bttl, 1, 1, 3, 1 )

    def ini_page(self):
        att_usr=self.__get_user()
        if att_usr==[]:
            att_usr=[["","","","",
                      "","","",""]]
        imp = Gtk.Button(label="Modifier")
        self.cent.attach(imp, 6, 10, 2, 1)
        imp.connect("clicked", self.header_bar.switch_page, "modify_client")
        DisplayClient.buttons["Modifier"]=imp


        imp = Gtk.Button(label="Modifier")
        self.cent.attach(imp, 6, 4, 3, 3)
        clss=ModifyClient.get_instance()
        clss.num=DisplayClient.num_client
        imp.connect("clicked", self.header_bar.switch_page, "modify_client")
        DisplayClient.buttons["ModifierClient"]=imp

        button = Gtk.Button(label="Supprimer")
        button.connect("clicked", self.__delete_client, self.num_client)
        self.cent.attach(button, 6, 7, 3, 3)
        DisplayClient.buttons["Supprimer"]=imp


        att_usr=self.__get_user()
        self.first_name(att_usr[4])
        self.last_name(att_usr[3])
        self.adrss(att_usr[5])
        self.mails(att_usr[2])
        self.nums(str(att_usr[6]))
        self.siret(str(att_usr[7]))
        self.entreprise(str(att_usr[7]))




    def __delete_client(self,button,num_client):
        """
        """
        self.client= self.dao.get_with_id(DisplayClient.num_client)
        self.dao.delete(self.client)
        self.header_bar.switch_page(None,"home_page")


    def __get_user(self):
        """
        Recupere de la bd les info utilisateur
        et les retourne sous forme de liste
        """
        if self.num_client==0:
            list_client=['Aucun', 'Aucun', 'Aucun', 'Aucun',
                         'Aucun', 'Aucun', 'Aucun', 'Aucun']
            return list_client
        else:
            self.client= self.dao.get_with_id(self.num_client)
            list_client=self.client.dump_to_list()
            return list_client

    def __get_client(self):
        """
        Recupere de la bd les info client
        et les retourne sous forme de liste
        """
        print("num=",self.num_client)
        self.client= self.dao.get_with_id((self.num_client))
        list_client= self.client.dump_to_list()
        print(list_client)
        return list_client


    def __get_ent(self):
        """
        Recupere de la bd les info entreprise
        et les retourne sous forme de liste
        """
        list_client= self.db.selection_table("company")
        return list_client


    def new_utilisateur(self):
        """
        Affichage pour utilisateur
        """
        att_usr=self.__get_user()
        if att_usr==[]:
            att_usr=[["","","","",
                      "","","",""]]

        imp = Gtk.Button(label="Modifier")
        self.cent.attach(imp, 6, 10, 2, 1)
        imp.connect("clicked", self.header_bar.switch_page, "modify_client")
        DisplayClient.buttons["Modifier"]=imp

        att_usr=att_usr[0]
        self.first_name(att_usr[2])
        self.last_name(att_usr[3])
        self.adrss(att_usr[5])
        self.mails(att_usr[4])
        self.nums(str(att_usr[6]))
        self.siret(str(att_usr[7]))
        self.entreprise(str(att_usr[7]))




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
        label.set_markup("<b>"+c_txt[0]+"</b>:    ")
        label.set_justify(Gtk.Justification.RIGHT)
        self.cent.attach(label,pos[0],pos[1],2,1)
        label.set_hexpand(True)
        label.set_hexpand(True)
        DisplayClient.label[c_txt[0]] = label
        entry = Gtk.Entry()
        entry.set_text(str(self.num_client))
        entry.set_hexpand(True)
        entry.set_editable(False)
        self.cent.attach(entry,pos[0]+2,pos[1],2,1)
        spacer = Gtk.Label("")
        spacer.set_hexpand(True)
        DisplayClient.entrys[c_txt[0]] = entry
        self.cent.attach(spacer,pos[0]+4,pos[1],1,1)

    def first_name(self,fn):
        self.__creat_labelbox(("Prenom ",fn),(1,2,3,1))
        return self

    def last_name(self,nm):
        self.__creat_labelbox(("Nom ",nm),(5,2,3,1))
        return self

    def adrss(self,adr):
        self.__creat_labelbox(("Adresse ",adr),(1,4,3,1))
        return self


    def mails(self,mail):
        self.__creat_labelbox(("Mail ",mail),(1,6,3,1))
        return self


    def nums(self,n):
        self.__creat_labelbox(("Numero ",n),(1,8,3,1))
        return self


    def update2client(self):
        DisplayClient.buttons["Modifier"].hide()
        attr_clt=self.__get_client()
        if attr_clt is None:
            raise ValueError
        DisplayClient.entrys["Nom "].set_text(attr_clt[0])
        DisplayClient.entrys["Prenom "].set_text(attr_clt[1])
        DisplayClient.entrys["Adresse "].set_text(attr_clt[3])
        DisplayClient.entrys["Numero "].set_text(str(attr_clt[4]))
        DisplayClient.entrys["Mail "].set_text(str(attr_clt[2]))



    def siret(self,sir):
        self.__creat_labelbox(("Siret ",sir),(1,10,3,1))
        return self

    def entreprise(self,ent):
        self.__creat_labelbox(("Entreprise ",ent),(1,12,3,1))
        return self

    def commentaire(self,com):
        label = Gtk.Label()
        label.set_markup("<b>"+c_txt[0]+"</b>:    ")
        label.set_justify(Gtk.Justification.RIGHT)
        self.cent.attach(label,6,16,2,1)
        label.set_hexpand(True)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_text(com)
        entry.set_hexpand(True)
        entry.set_editable(False)
        DisplayClient.entrys["Com "]=entry
        self.cent.attach(entry,7,17,2,2)
