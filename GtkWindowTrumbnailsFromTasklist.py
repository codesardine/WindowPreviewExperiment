import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
from gi.repository import Gdk
from gi.repository import GdkX11, GdkPixbuf   

class IconViewWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(200, 200)

        liststore = Gtk.ListStore(Pixbuf, str)
        iconview = Gtk.IconView.new()
        iconview.set_model(liststore)
        iconview.set_pixbuf_column(0)

        screen = Wnck.Screen.get_default()
        screen.force_update()
        window_list = screen.get_windows()

        print(window_list)
        for window in window_list:
            _type = window.get_window_type()
            if _type is Wnck.WindowType.NORMAL and not window.is_skip_tasklist():
                print(window.get_name())
                xid = window.get_xid()
                w = GdkX11.X11Window.foreign_new_for_display(Gdk.Display.get_default(), xid)
                width = Gdk.Window.get_width(w)
                height = Gdk.Window.get_height(w)
                pixbuf = Gdk.pixbuf_get_from_window(w, 1, 1, width-3, height-3)
                ratio = (height*300)/width
                scale = pixbuf.scale_simple(300, ratio, GdkPixbuf.InterpType.BILINEAR)
                liststore.append([scale, ""])

        self.add(iconview)

win = IconViewWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
