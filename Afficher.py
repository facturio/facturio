#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf

class Afficher(Gtk.Window):
    def __init__(self,is_ut):
        super().__init__(title="Facturio: Afficher")
        self.resize(1920, 1080)
        self.set_hexpand(False)
        provider = Gtk.CssProvider()
        provider.load_from_path("./main.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        #grid
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(20)
        # spaces
        self.spaceHeader = Gtk.Label(label="")
        self.grid.attach(self.spaceHeader,1,1,10,10)
        self.spaceFooter = Gtk.Label(label="")
        self.grid.attach(self.spaceFooter,7,5,1,1)
        self.facturio_label = Gtk.Label(label="Afficher")
        self.grid.attach(self.facturio_label, 3, 2, 6, 1 )
        if is_ut:
            # logo
            self.adrss("test")
            self.mails("test")
            self.nums("test")
            self.entreprise("test")
            self.siret("test")
            self.logo("./icons/Moi.jpg")
            self.commentaire("./icons/Moi.jpg")
        else:
            self.imp = Gtk.Button(label="Parameter")
            self.grid.attach(self.imp, 7, 2, 2, 1)
            self.button = Gtk.Button(label="Supprimer")
            self.grid.attach(self.button, 9, 2, 2, 1)
            self.adrss("test")
            self.mails("test")
            self.nums("test")
            self.entreprise("test")
            self.siret("test")

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

#########################
#######TEST##############
#########################
win =Afficher(False)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
