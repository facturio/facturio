#!/usr/bin/env python3
import i18n
import gi
from facturio.gui.page_gui import PageGui
import concurrent.futures
from facturio.db.clientdao import ClientDAO
from geopy.geocoders import Nominatim
gi.require_version("Gtk", "3.0")
gi.require_version("OsmGpsMap", "1.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, OsmGpsMap
from facturio import __path__

class Map(PageGui):
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
        self.dao=ClientDAO.get_instance()
        self.grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        self.add(self.grid)
        (
            self.title(i18n.t('gui.map'))
                .space()
                .search((1,3,5,1))
                .__init_map()
        )
        list_obj_client= self.dao.get_all()
        list_client =[]
        for i in list_obj_client:
            list_client.append(i.dump_to_list)
        list_adress=[client[4] for client in list_client ]
        print(list_adress)
        # self.print_all_customer(list_adress)


    def __init_map(self):
        """
        Initialise la map a l'universite de Toulon
        """
        self.osm = OsmGpsMap.Map()
        self.osm.set_property("map-source", OsmGpsMap.MapSource_t.OPENSTREETMAP)
        self.osm.set_center_and_zoom(46.333328 ,2.6, 5)
        self.osm.set_hexpand(True)
        self.grid.attach(self.osm, 1, 4, 5, 6)


    def __get_gps(self,adrss):
        """
        prend une adresse en str et retourne les
        coordonees GPS de l'adresse
        """
        geolocator = Nominatim(user_agent="Nominatim")
        location = geolocator.geocode(adrss)
        if location == None:
            print("adresse non trouver :", adrss)
            return (None,None)
        x, y = location.latitude, location.longitude
        print((x,y))
        return (x,y)


    def mv_map(self, adrss):
        """
        Prend une adress str, et deplace la map de init_map
        aux coordonees GPS de l'adresse avec un marqueur

        ex:
        Map.mv_map("15 chemin jean court le haut Pierrefeu")
        """
        x,y= self.__get_gps(adrss)
        self.osm.set_center_and_zoom(x, y, 17)
        marker = GdkPixbuf.Pixbuf.new_from_file_at_size(__path__[0] + "/data/icons/poi.png", 50, 50)
        self.osm.image_add(x, y, marker)
        return self


    def print_all_customer(self,l_adress):
        """
        Prend une liste d'adresse et renvoie sur la map une
        icone a chquene de leur adresse
        """
        for adresse in l_adress:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.__get_gps, adresse)
                x,y = future.result()
                if x!= None:
                    marker = GdkPixbuf.Pixbuf.new_from_file_at_size(__path__[0] + "/data/icons/poi.png", 25, 25)
                    self.osm.image_add(x, y, marker)
        return self
