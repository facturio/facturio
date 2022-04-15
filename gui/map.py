#!/usr/bin/env python3
import gi
from gui.page_gui import Page_Gui
gi.require_version("Gtk", "3.0")
gi.require_version("OsmGpsMap", "1.0")
from geopy.geocoders import Nominatim
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, OsmGpsMap

class Map(Page_Gui):
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
        (
            self.title("Carte")
                .space()
                .search((1,3,4,1))
                .__init_map()
        )
        self.mv_map("Paris")


    def __init_map(self):
        """
        Initialise la map a l'universite de Toulon
        """
        self.osm = OsmGpsMap.Map()
        self.osm.set_property("map-source", OsmGpsMap.MapSource_t.OPENSTREETMAP)
        self.osm.set_center_and_zoom(43.13542095, 6.016683572120083,17)
        self.osm.set_hexpand(True)
        self.grid.attach(self.osm, 1, 4, 4, 6)


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
        marker = GdkPixbuf.Pixbuf.new_from_file_at_size("../icons/poi.png", 50, 50)
        self.osm.image_add(x, y, marker)
        return self


