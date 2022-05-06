import gi
from facturio.gui.home import HeaderBarSwitcher
gi.require_version("Gtk", "3.0")
from classes.user import User
from gui.add_customer import Add_Customer
gi.require_version("OsmGpsMap", "1.0")
from facturio.gui.page_gui import PageGui
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, OsmGpsMap
from facturio import __path__

class InfoPerson (PageGui):
    """
    Classe IHM de le fenetre d'affichage, elle permet soit d'afficher la page
    d'utilisateur soit la page d'un client
    +--------+
    |---  == |
    |---  -- |
    +--------+
    """
    def __init__(self, header_bar: HeaderBarSwitcher, is_ut, num_client=None,*args, **kwargs):
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


    def __get_user(self):
        """
        Recupere de la bd les info utilisateur
        et les retourne sous forme de liste
        """
        list_client= self.db.selection_table("user")
        return list_client


    def utilisateur(self):
        """
        Affichage pour utilisateur
        """
        att_usr=self.__get_user()[0]
        self.__title(att_usr[2])
        self.adrss(att_usr[4])
        self.mails(att_usr[3])
        self.nums(str(att_usr[5]))
        self.siret(str(att_usr[6]))
        self.logo("./data/icons/Moi.png")


    def client(self):
        """
        Affichage pour client
        """
        self.imp = Gtk.Button(label="Parameter")
        self.grid.attach(self.imp, 7, 2, 2, 1)
        self.button = Gtk.Button(label="Supprimer")
        self.grid.attach(self.button, 9, 2, 2, 1)
        self.adrss("test")
        self.mails("test")
        self.nums("test")
        self.entreprise("test")
        self.siret("test")
        self.commentaire("ldhfskjv xbvhxknvkhxfvkjzx vjgcxbv jlkmc jcbui jmcljbuxvn kjxvhofxv dvudhvbdhkvn kbhvdubn kfuhvxovnludhvod")


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
        self.imp = Gtk.Button(label="Modifier")
        self.cent.attach(self.imp, 6, 12, 3, 1)
        self.imp.connect("clicked", self.header_bar.active_button, "modify_usr")
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


    def adrss(self,adr):
        self.__creat_labelbox(("Adresse ",adr),(1,4,3,1))
        return self


    def mails(self,mail):
        self.__creat_labelbox(("Mail ",mail),(1,6,3,1))
        return self


    def nums(self,n):
        self.__creat_labelbox(("Numero ",n),(1,8,3,1))
        return self


    def entreprise(self,ent):
        self.__creat_labelbox(("entreprise ",ent),(1,10,3,1))
        return self


    def siret(self,sir):
        self.__creat_labelbox(("Siret ",sir),(1,12,3,1))
        return self


    def logo(self,path):
        log = Gtk.Image.new_from_pixbuf(
            GdkPixbuf.Pixbuf.new_from_file_at_size("./data/icons/Moi.png", 200, 200))
        log.set_name("lg")
        self.cent.attach(log, 6, 4, 3, 6 )


    def commentaire(self,adr):
        boxcom= Gtk.Box()
        boxcom.set_name("box_afficher")
        self.com = Gtk.Label(label=adr)
        self.com.set_line_wrap(True)
        self.com.set_max_width_chars(32)
        boxcom.pack_start(self.com, False, False, 0)
        self.cent.attach(boxcom, 4, 10, 3, 3 )

