import gi
gi.require_version("Gtk", "3.0")
from gui.page_gui import Page_Gui
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, OsmGpsMap

class InfoPerson (Page_Gui):
    """
    Classe IHM de le fenetre d'affichage, elle permet soit d'afficher la page
    d'utilisateur soit la page d'un client
    +--------+
    |---  == |
    |---  -- |
    +--------+
    """
    def __init__(self, is_ut, name,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_grid()
        self.__space_info()
        self.title(name)
        if is_ut:
            self.utilisateur()
        else:
            self.client()


    def title__(self, ttl):
        bttl= Gtk.Box()
        bttl.set_name("name")
        self.tl = Gtk.Label()
        self.tl.set_markup("<span font_weight=\"bold\" size=\"xx-large\">"+ttl+"</span>")
        bttl.pack_start(self.tl, False, False, 0)
        self.grid.attach(bttl, 2, 2, 1, 1 )


    def utilisateur(self):
        """
        Affichage pour utilisateur
        """
        self.adrss("test")
        self.mails("test")
        self.nums("test")
        self.entreprise("test")
        self.siret("test")
        self.logo("../icons/Moi.png")
        self.commentaire("ldhfskjv xbvhxknvkhxfvkjzx vjgcxbv jlkmc jcbui jmcljbuxvn kjxvhofxv dvudhvbdhkvn kbhvdubn kfuhvxovnludhvod")



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


    def __space_info(self):
        """
        Ajoute les espace
        pour l'ergonomie
        """
        spaceh = Gtk.Label(label="")
        spacel = Gtk.Label(label="")
        self.grid.attach(spacel,7,0,1,1)
        self.grid.attach(spaceh,0,0,1,1)


    def __creat_labelbox(self,c_txt,pos):
        """
        prend un couple de chaine de charactere ainsi que un
        tuple de postion et affhiche un label avec une boite
        """
        boxadress= Gtk.Box()
        boxadress.set_name("box_afficher")
        self.adrs = Gtk.Label()
        self.adrs.set_markup("<b>"+c_txt[0]+"</b>:")
        self.txt = Gtk.Label(c_txt[1])
        boxadress.pack_start(self.txt, False, False, 0)
        self.grid.attach(boxadress, *pos)
        self.grid.attach_next_to(self.adrs,boxadress,Gtk.PositionType.LEFT,1,1)
        self.spaceadrss = Gtk.Label(label="")
        self.grid.attach(self.spaceadrss,0,pos[1]+1,1,1)


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
            GdkPixbuf.Pixbuf.new_from_file_at_size(path, 200, 200))
        log.set_name("lg")
        self.grid.attach(log, 4, 4, 3, 6 )


    def commentaire(self,adr):
        boxcom= Gtk.Box()
        boxcom.set_name("box_afficher")
        self.com = Gtk.Label(label=adr)
        self.com.set_line_wrap(True)
        self.com.set_max_width_chars(32)
        boxcom.pack_start(self.com, False, False, 0)
        self.grid.attach(boxcom, 4, 10, 3, 3 )

