import i18n
from facturio.gui.home import HeaderBarSwitcher
from facturio.classes.user import User
from facturio.gui.add_customer import Add_Customer
from facturio.gui.page_gui import PageGui
from facturio import __path__
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("OsmGpsMap", "1.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, OsmGpsMap


class InfoPerson (PageGui):
    """
    Classe IHM de le fenetre d'affichage, elle permet soit d'afficher la page
    d'utilisateur soit la page d'un client
    +--------+
    |---  == |
    |---  -- |
    +--------+
    """
    def __init__(self, is_ut, num_client=0,*args, **kwargs):
        print("num=",num_client)
        self.header_bar = HeaderBarSwitcher.get_instance()
        super().__init__(*args, **kwargs)
        self.cent = Gtk.Grid(column_homogeneous=False,
                                  row_homogeneous=False, column_spacing=20,
                                  row_spacing=20)
        self.__init_grid()
        self.grid.attach(self.cent, 1, 2, 2, 1)
        self.__space_info()
        if is_ut:
            self.utilisateur()
        else:
            self.num_client=num_client
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

    def __title(self, ttl):
        bttl= Gtk.Box()
        bttl.set_name("name")
        self.tl = Gtk.Label()
        self.tl.set_markup("<span font_weight=\"bold\" size=\"xx-large\">"+ttl+"</span>")
        bttl.pack_start(self.tl, False, False, 0)
        self.grid.attach(bttl, 1, 1, 3, 1 )

    def __delete_client(self):
        """
        """
        list_client= self.db.selection_table("user")
        return list_client

    def __get_user(self):
        """
        Recupere de la bd les info utilisateur
        et les retourne sous forme de liste
        """
        list_client= self.db.selection_table("user")
        return list_client

    def __get_client(self):
        """
        Recupere de la bd les info client
        et les retourne sous forme de liste
        """
        list_client= self.db.selection_table("client")
        return list_client[self.num_client-1]

    def __get_ent(self):
        """
        Recupere de la bd les info entreprise
        et les retourne sous forme de liste
        """
        list_client= self.db.selection_table("company")
        return list_client

    def utilisateur(self):
        """
        Affichage pour utilisateur
        """
        att_usr=self.__get_user()
        if att_usr==[]:
            att_usr=[["","","","",
                      "","","",""]]
        self.imp = Gtk.Button(label="Modifier")
        self.cent.attach(self.imp, 6, 12, 3, 1)
        self.imp.connect("clicked", self.header_bar.active_button, "modify_usr")
        att_usr=att_usr[0]
        self.__title(att_usr[1])
        self.first_name(att_usr[2])
        self.last_name(att_usr[3])
        self.adrss(att_usr[5])
        self.mails(att_usr[4])
        self.nums(str(att_usr[6]))
        self.siret(str(att_usr[7]))
        self.logo(__path__[0] + "/data/icons/Moi.png")

    def client(self):
        """
        Affichage pour client
        """
        att_clt=self.__get_client()
        l_entr=self.__get_ent()
        l_id=[l[0] for l in l_entr]
        self.imp = Gtk.Button(label=i18n.t('gui.settings'))
        self.cent.attach(self.imp, 6, 4, 3, 3)
        self.imp.connect("clicked", self.header_bar.active_button, "modify_usr")
        self.button = Gtk.Button(label=i18n.t('gui.delete'))
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
        # self.imp = Gtk.Button(label=i18n.t('gui.edit'))
        # self.cent.attach(self.imp, 6, 12, 3, 1)
        # self.imp.connect("clicked", self.header_bar.active_button, "modify_usr")
        label = Gtk.Label()
        label.set_markup("<b>"+c_txt[0]+"</b>:    ")
        label.set_justify(Gtk.Justification.RIGHT)
        self.cent.attach(label,pos[0],pos[1],2,1)
        label.set_hexpand(True)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_text(c_txt[1])
        entry.set_hexpand(True)
        entry.set_editable(False)
        self.cent.attach(entry,pos[0]+2,pos[1],2,1)
        spacer = Gtk.Label("")
        spacer.set_hexpand(True)
        self.cent.attach(spacer,pos[0]+4,pos[1],1,1)

    def first_name(self,fn):
        self.__creat_labelbox((i18n.t('gui.name'),fn),(1,4,3,1))
        return self

    def last_name(self,nm):
        self.__creat_labelbox((i18n.t('gui.surname'),nm),(1,6,3,1))
        return self

    def adrss(self,adr):
        self.__creat_labelbox((i18n.t('gui.address'),adr),(1,8,3,1))
        return self


    def mails(self,mail):
        self.__creat_labelbox((i18n.t('gui.email'),mail),(1,10,3,1))
        return self


    def nums(self,n):
        self.__creat_labelbox((i18n.t('gui.phone_number'),n),(1,12,3,1))
        return self


    def entreprise(self,ent):
        self.__creat_labelbox((i18n.t('gui.business'),ent),(1,14,3,1))
        return self


    def siret(self,sir):
        self.__creat_labelbox((i18n.t('gui.siret_number'),sir),(1,16,3,1))
        return self

    def logo(self,path):
        log = Gtk.Image.new_from_pixbuf(
            GdkPixbuf.Pixbuf.new_from_file_at_size(path, 200, 200))
        log.set_name("lg")
        self.cent.attach(log, 6, 4, 3, 6 )


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
        self.cent.attach(entry,7,17,2,2)
