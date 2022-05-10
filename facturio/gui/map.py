#!/usr/bin/env python3
import i18n
import gi
from facturio.gui.page_gui import PageGui
from facturio.classes.client import Client
import concurrent.futures
from facturio.db.clientdao import ClientDAO
from facturio.gui.omnisearch import FacturioOmnisearch
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
        self.cent = Gtk.Grid(column_homogeneous=True,
                                  row_homogeneous=True, column_spacing=20,
                                  row_spacing=20)
        self.__init_grid()
        self.add(self.grid)
        (
            self.title(i18n.t('gui.map'))
                .space()
                .__init_map()
        )
        self.__space_info()
        self.search_bar_client()
        list_obj_client= self.dao.get_all()
        list_client =[]
        #for i in list_obj_client:
        #    l=i.dump_to_list()
        #    list_client.append(i)
        #list_adress=[client[4] for client in list_client ]
        #print(list_adress)
        # self.print_all_customer(list_adress)


    def __space_info(self):
        """
        Ajoute les espace
        pour l'ergonomie
        """
        spacel = Gtk.Label("")
        self.cent.attach(spacel, 0, 1, 1, 1)
        spacer = Gtk.Label("")
        self.cent.attach(spacer, 10, 2, 1, 1)
        spaceb = Gtk.Label("")

    def __init_grid(self):
        """
        Propriete de la Grid Gtk
        voir doc
        """
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(False)
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(20)
        self.grid.attach(self.cent, 2, 2, 6, 3)
        return self

    def __init_map(self):
        """
        Initialise la map a l'universite de Toulon
        """
        self.osm = OsmGpsMap.Map()
        self.osm.set_property("map-source", OsmGpsMap.MapSource_t.OPENSTREETMAP)
        self.osm.set_center_and_zoom(46.333328 ,2.6, 5)
        self.osm.set_hexpand(True)
        self.cent.attach(self.osm, 2, 4, 5, 6)


    def __get_gps(self,adrss):
        """
        prend une adresse en str et retourne les
        coordonees GPS de l'adresse
        """
        geolocator = Nominatim(user_agent="Nominatim")
        location = geolocator.geocode(adrss)
        if location == None:
            # print("adresse non trouver :", adrss)
            return (None,None)
        x, y = location.latitude, location.longitude
        # print((x,y))
        return (x,y)

    def search_bar_client(self):
        """
        Affiche tout les clients de la base de donner
        """
        list_obj_client= self.dao.get_all()
        list_client =[]
        for i in list_obj_client:
            list_client.append(i.dump_to_list())
        searchbar = FacturioOmnisearch(list_client)
        searchbar.completion.connect('match-selected', self.switch_to_local)
        self.cent.attach(searchbar, 2,3,5,1)

    def switch_to_local(self, completion, model, iter):
        """
        recupere les info de la completion et les affiche
        avec la page info_persone
        """
        # print("insdie")
        iterr = ((list((completion.props.model.get_value(iter, 0)))))
        iterr = iterr[:-1]
        num_client=""
        for i in reversed(iterr):
            if i == ' ':
                break
            else:
                num_client+=i
        client=self.dao.get_with_id(num_client)
        if client!=None:
            # print(client.dump_to_list()[3])
            self.mv_map(client.dump_to_list()[2])
        else:
            # print("erreur")
            pass

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
