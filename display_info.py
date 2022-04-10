import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class InfoPerson (Gtk.ScrolledWindow):
    """
    Classe IHM de le fenetre Map, elle permet soit d'afficher la page
    d'utilisateur soit la page d'un client
    +--------+
    |---  == |
    |---  -- |
    +--------+
    """
    def __init__(self, is_ut, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_grid()
        self.space()
        #doit devenir une variable
        self.title("Moi")
        if is_ut:
            self.utilisateur()
        else:
            self.client()


    def title(self, ttl):
        facturio_label = Gtk.Label(label=ttl)
        facturio_label.set_markup("<span font_weight=\"bold\" size=\"xx-large\">"+ttl+"</span>")
        self.grid.attach(facturio_label, 0, 2, 1, 1 )


    def utilisateur(self):
        """
        Affichage pour utilisateur
        """
        self.adrss("test")
        self.mails("test")
        self.nums("test")
        self.entreprise("test")
        self.siret("test")
        self.logo("./icons/Moi.jpg")
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

    def space(self):
        """
        Ajoute les espace
        pour l'ergonomie
        """
        spaceh = Gtk.Label(label="")
        spacel = Gtk.Label(label="")
        self.grid.attach(spacel,7,0,1,1)
        self.grid.attach(spaceh,0,1,4,1)

    def adrss(self,adr):
        boxadress= Gtk.Box()
        boxadress.set_name("box_afficher")
        self.adrs = Gtk.Label()
        self.adrs.set_markup("<b>Adres.</b>:"+adr)
        boxadress.pack_start(self.adrs, False, False, 0)
        self.grid.attach(boxadress, 1, 4, 3, 1 )
        self.spaceadrss = Gtk.Label(label="")
        self.grid.attach(self.spaceadrss,0,5,1,10)

    def mails(self,adr):
        boxmail= Gtk.Box()
        boxmail.set_name("box_afficher")
        self.mail = Gtk.Label()
        self.mail.set_markup("<b>Mail</b>:"+adr)
        boxmail.pack_start(self.mail, False, False, 0)
        self.grid.attach(boxmail, 1, 6, 3, 1 )
        self.spacemails = Gtk.Label(label="")
        self.grid.attach(self.spacemails,0,7,1,10)

    def nums(self,adr):
        boxnum= Gtk.Box()
        boxnum.set_name("box_afficher")
        self.num = Gtk.Label()
        self.num.set_markup("<b>Num.</b>:"+adr)
        boxnum.pack_start(self.num, False, False, 0)
        self.grid.attach(boxnum, 1, 8, 3, 1 )
        self.spacenums = Gtk.Label(label="")
        self.grid.attach(self.spacenums,0,9,1,10)

    def entreprise(self,adr):
        boxentr= Gtk.Box()
        boxentr.set_name("box_afficher")
        self.entr = Gtk.Label()
        self.entr.set_markup("<b>Entr.</b>:"+adr)
        boxentr.pack_start(self.entr, False, False, 0)
        self.grid.attach(boxentr, 1, 10, 3, 1 )
        self.spaceentrs = Gtk.Label(label="")
        self.grid.attach(self.spaceentrs,0,11,1,10)

    def siret(self,adr):
        boxsir= Gtk.Box()
        boxsir.set_name("box_afficher")
        self.sir = Gtk.Label()
        self.sir.set_markup("<b>Siret.</b>:"+adr)
        boxsir.pack_start(self.sir, False, False, 0)
        self.grid.attach(boxsir, 1, 12, 3, 1 )

    def logo(self,path):
        lg = Gtk.Image()
        lg.set_from_file(path)
        lg.set_name("lg")
        self.grid.attach(lg, 4, 4, 3, 6 )

    def commentaire(self,adr):
        boxcom= Gtk.Box()
        boxcom.set_name("box_afficher")
        self.com = Gtk.Label(label=adr)
        self.com.set_line_wrap(True)
        self.com.set_max_width_chars(32)
        boxcom.pack_start(self.com, False, False, 0)
        self.grid.attach(boxcom, 4, 10, 3, 3 )

    def init_grid(self):
        """
        Propriete de la Grid Gtk
        voir doc
        """
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(20)
