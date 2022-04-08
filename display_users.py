#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf

class DisplayUsers(Gtk.Window):
    """
    Classe IHM de le fenetre Map, elle permet soit d'afficher la page
    d'utilisateur soit la page d'un client
    +--------+
    |---  == |
    |---  -- |
    +--------+
    """
    def __init__(self,is_ut):
        super().__init__(title="Facturio: Afficher")
        self.set_hexpand(False)
        provider = Gtk.CssProvider()
        provider.load_from_path("./main.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.init_grid()
        self.space()
        self.facturio_label = Gtk.Label(label="Afficher")
        self.grid.attach(self.facturio_label, 3, 2, 6, 1 )
        if is_ut:
            self.utulisateur()
        else:
            self.client()

    def utulisateur(self):
        """
        Affichage pour utulisateur
        """
        self.adrss("test")
        self.mails("test")
        self.nums("test")
        self.entreprise("test")
        self.siret("test")
        self.logo("./icons/Moi.jpg")
        self.commentaire("./icons/Moi.jpg")

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
        self.grid.attach(spaceh,1,1,10,10)
        spacef = Gtk.Label(label="")
        self.grid.attach(spacef,7,5,1,1)

    def adrss(self,adr):
        boxadress= Gtk.Box()
        self.adrs = Gtk.Label(label=adr)
        boxadress.pack_start(self.adrs, False, False, 0)
        boxadress.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,.5))
        self.grid.attach(boxadress, 3, 4, 3, 1 )
        self.spaceadrss = Gtk.Label(label="")
        self.grid.attach(self.spaceadrss,1,5,10,10)

    def mails(self,adr):
        boxmail= Gtk.Box()
        self.mail = Gtk.Label(label=adr)
        boxmail.pack_start(self.mail, False, False, 0)
        boxmail.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,.5))
        self.grid.attach(boxmail, 3, 6, 3, 1 )
        self.spacemails = Gtk.Label(label="")
        self.grid.attach(self.spacemails,1,7,10,10)

    def nums(self,adr):
        boxnum= Gtk.Box()
        self.num = Gtk.Label(label=adr)
        boxnum.pack_start(self.num, False, False, 0)
        boxnum.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,.5))
        self.grid.attach(boxnum, 3, 8, 3, 1 )
        self.spacenums = Gtk.Label(label="")
        self.grid.attach(self.spacenums,1,9,10,10)

    def entreprise(self,adr):
        boxentr= Gtk.Box()
        self.entr = Gtk.Label(label=adr)
        boxentr.pack_start(self.entr, False, False, 0)
        boxentr.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,.5))
        self.grid.attach(boxentr, 3, 10, 3, 1 )
        self.spaceentrs = Gtk.Label(label="")
        self.grid.attach(self.spaceentrs,1,11,10,10)

    def siret(self,adr):
        boxsir= Gtk.Box()
        self.sir = Gtk.Label(label=adr)
        boxsir.pack_start(self.sir, False, False, 0)
        boxsir.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,.5))
        self.grid.attach(boxsir, 3, 12, 3, 1 )

    def logo(self,path):
        lg = Gtk.Image()
        lg.set_from_file(path)
        boxlg= Gtk.Box()
        boxlg.pack_start(lg, False, False, 0)
        boxlg.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,.5))
        self.grid.attach(boxlg, 7, 4, 3, 6 )

    def commentaire(self,adr):
        boxcom= Gtk.Box()
        self.com = Gtk.Label(label=adr)
        boxcom.pack_start(self.com, False, False, 0)
        boxcom.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,.5))
        self.grid.attach(boxcom, 7, 10, 3, 3 )

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

#########################
#######TEST##############
#########################
win =Afficher(True)
win.show_all()
Gtk.main()
