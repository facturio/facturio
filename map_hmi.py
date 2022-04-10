#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("OsmGpsMap", "1.0")
from geopy.geocoders import Nominatim
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, OsmGpsMap

class Map(Gtk.ScrolledWindow):
    """
    Classe IHM de la fenetre Map, elle permet de chercher un client
    et d'afficher ca position sur une
    map

    +--------+
    |--| +-+ |
    |__| +-+ |
    +--------+
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        self.add(self.grid)
        self.title("Carte")
        self.space()
        self.search((3,4,3,1))
        self.init_map()
        self.init_result()

    def title(self, ttl):
        facturio_label = Gtk.Label(label=ttl)
        facturio_label.set_markup("<span font_weight=\"bold\" size=\"xx-large\">"+ttl+"</span>")
        self.grid.attach(facturio_label, 0, 2, 6, 1 )

    def search(self,l_attach):
        """
        Prend un emplacement et
        Invoque la barre de recherche
        a cette emplacement
        """
        searchbar = Gtk.SearchEntry()
        self.grid.attach(searchbar, *l_attach)

    def space(self):
        """
        Ajoute les espace
        pour l'ergonomie
        """
        spaceh = Gtk.Label(label="")
        self.grid.attach(spaceh,1,1,10,10)

    def init_map(self):
        """
        Initialise la map a l'universite de Toulon
        """
        self.osm = OsmGpsMap.Map()
        self.osm.set_property("map-source", OsmGpsMap.MapSource_t.OPENSTREETMAP)
        self.osm.set_center_and_zoom(43.13542095, 6.016683572120083,17)
        self.grid.attach(self.osm, 6, 4, 3, 5)

    def mv_map(self, adrss):
        """
        Prend une adress str, et deplace la map de init_map
        aux coordonees GPS de l'adresse avec un marqueur

        ex:
        Map.mv_map("15 chemin jean court le haut Pierrefeu")
        """
        geolocator = Nominatim(user_agent="Nominatim")
        location = geolocator.geocode(adrss)
        x, y = location.latitude, location.longitude
        self.osm.set_center_and_zoom(x, y, 17)
        pb = GdkPixbuf.Pixbuf.new_from_file_at_size("./icons/poi.png", 50, 50)
        self.osm.image_add(x, y, pb)


    def init_result(self):
        """
        Initialise la barre de recherche et permet l'ajout grace
        a la methode add_result
        """
        l_client= [
        ]
        self.liste_client= Gtk.ListStore(str, str, str)
        for client in l_client:
            self.liste_client.append(client)
        self.treeview = Gtk.TreeView(model=self.liste_client)
        for i, column_title in enumerate(["Nom", "entreprise", "Adresse"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.grid.attach(self.scrollable_treelist, 3, 5, 3, 10)
        self.scrollable_treelist.add(self.treeview)
