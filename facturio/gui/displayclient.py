from os import EX_USAGE
import gi
from facturio.gui.home import HeaderBarSwitcher
gi.require_version("Gtk", "3.0")
from classes.user import User
from gui.add_customer import Add_Customer
gi.require_version("OsmGpsMap", "1.0")
from facturio.gui.page_gui import PageGui
from facturio.db.clientdao import ClientDAO
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, OsmGpsMap
from facturio import __path__

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
    buttons={}

    @staticmethod
    def get_instance():
        """Renvoie le singleton."""
        if DisplayClient.__instance is None:
            DisplayClient.__instance = DisplayClient()
        return DisplayClient.__instance


    def __init__(self,is_ut=False,num_client=0,*args, **kwargs):
        super().__init__()
        self.dao=ClientDAO.get_instance()
        self.num_client=DisplayClient.num_client
        self.is_ut=is_ut
        print(self.num_client)
        self.num_client=int(num_client)
        DisplayClient.num_client=int(num_client)
        self.header_bar = HeaderBarSwitcher.get_instance()
        super().__init__(*args, **kwargs)
        self.cent = Gtk.Grid(column_homogeneous=False,
                                  row_homogeneous=False, column_spacing=20,
                                  row_spacing=20)
        self.__init_grid()
        self.__title(str(self.num_client))
        self.grid.attach(self.cent, 1, 2, 2, 1)
        self.__space_info()
        if DisplayClient.__instance is None:
            self.ini_page()
        else:
                self.update2client()


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
        imp.connect("clicked", self.header_bar.switch_page, "modify_client")
        DisplayClient.buttons["ModifierClient"]=imp

        button = Gtk.Button(label="Supprimer")
        button.connect("clicked", self.__delete_client, self.num_client)
        self.cent.attach(button, 6, 7, 3, 3)
        DisplayClient.buttons["Supprimer"]=imp


        att_usr=self.__get_user()
        self.__title(att_usr[1])
        self.first_name(att_usr[2])
        self.last_name(att_usr[3])
        self.adrss(att_usr[5])
        self.mails(att_usr[4])
        self.nums(str(att_usr[6]))
        self.siret(str(att_usr[7]))




    def __delete_client(self,button,num_client):
        """
        """
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
        list_client= self.dao.get_with_id(int(self.num_client))
        list_client= list_client.dump_to_list()
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
        self.__title(att_usr[1])
        self.first_name(att_usr[2])
        self.last_name(att_usr[3])
        self.adrss(att_usr[5])
        self.mails(att_usr[4])
        self.nums(str(att_usr[6]))
        self.siret(str(att_usr[7]))


    def new_client(self):
        """
        INATEIGNABLE
        Affichage pour client
        """
        print("error")
        att_clt=self.__get_client()
        l_entr=self.__get_ent()
        l_id=[l[0] for l in l_entr]
        self.imp = Gtk.Button(label="Modifier")
        self.cent.attach(self.imp, 6, 4, 3, 3)
        self.imp.connect("clicked", self.header_bar.switch_page, "modify_usr")
        self.button = Gtk.Button(label="Supprimer")
        self.button.connect("clicked", self.__delete_client, self.num_client)
        self.cent.attach(self.button, 6, 7, 3, 3)
        exporter = Gtk.Button.new_from_icon_name("document-save-symbolic",
                                                    Gtk.IconSize.BUTTON)
        self.cent.attach(exporter, 6, 10, 3, 3)
        self.first_name(att_clt[2])
        self.last_name(att_clt[3])
        self.adrss(att_clt[4])
        self.mails(att_clt[3])
        self.nums(str(att_clt[5]))
        if self.num_client in l_id:
            self.entreprise(l_entr[self.num_client][1])
            self.siret(str(l_entr[self.num_client][2]))
        #self.commentaire(att_clt[6])


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


    def entreprise(self,ent,pos):
        label = Gtk.Label()
        label.set_markup("<b>Entreprise</b>:    ")
        label.set_justify(Gtk.Justification.RIGHT)
        self.cent.attach(label,pos[0],pos[1],2,1)
        label.set_hexpand(True)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_text(ent)
        entry.set_hexpand(True)
        entry.set_editable(False)
        self.cent.attach(entry,pos[0]+2,pos[1],2,1)
        spacer = Gtk.Label("")
        spacer.set_hexpand(True)
        self.cent.attach(spacer,pos[0]+4,pos[1],1,1)


    def update2client(self):
        DisplayClient.buttons["Modifier"].hide()
        attr_clt=self.__get_client()
        if attr_clt is None:
            raise ValueError
        DisplayClient.entrys["Nom "].set_text(attr_clt[1])
        DisplayClient.entrys["Prenom "].set_text(attr_clt[2])
        DisplayClient.entrys["Adresse "].set_text(attr_clt[4])
        DisplayClient.entrys["Numero "].set_text(str(attr_clt[5]))
        DisplayClient.entrys["Mail "].set_text(str(attr_clt[3]))
        DisplayClient.entrys["Siret "].set_text(str(attr_clt[6]))



    def siret(self,sir):
        self.__creat_labelbox(("Siret ",sir),(1,10,3,1))
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
