import gi
import os
gi.require_version('Gdk', '3.0')
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk

def get_images():
    images_path = "images/"
    images = os.listdir(images_path)
    image_list= []
    for image in images:
        image_list.append(f"images/{image}")
    if len(image_list) != 0:
        return image_list

def getGtkImage():
    gtk_image = []
    gtk_image_box = []
    imageName = []
    for image in get_images():
        # Load the image as a Pixbuf
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(image)
        imageName.append(image.replace('images/',''))
        # Scale down the image while maintaining aspect ratio
        max_width = 300
        max_height = 300
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        if width > max_width or height > max_height:
            if width > height:
                scaled_width = max_width
                scaled_height = int(max_width * height / width)
            else:
                scaled_height = max_height
                scaled_width = int(max_height * width / height)
            pixbuf = pixbuf.scale_simple(scaled_width, scaled_height, GdkPixbuf.InterpType.BILINEAR)
        
        # Create a new Gtk.Image from the scaled Pixbuf
        image_widget = Gtk.Image.new_from_pixbuf(pixbuf)
        image_widget.get_style_context().add_class("image")
        gtk_image.append(image_widget)
    
    # Making a box that will be parsed 
    for i, image in enumerate(gtk_image):
        event_box = Gtk.EventBox()
        TempBox = Gtk.Box.new(Gtk.Orientation(1), 0)
        TempBox.add(image)
        tempLable = Gtk.Label.new(imageName[i])
        TempBox.add(tempLable)
        event_box.add(TempBox)
        event_box.connect("button_press_event", lambda widget, event: on_image_clicked(widget, event, imageName[i]))
        gtk_image_box.append(event_box)
        
    return gtk_image_box
clickedImage=""
def on_image_clicked(event_box, button_press_event, name):
    global clickedImage
    clickedImage = name

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title='')
        self.set_default_size(1000,1000)
        global clickedImage
        self.clickedImage=clickedImage
        self.body=Gtk.ScrolledWindow()
        self.body.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.stack = Gtk.Stack()
        self.add(self.stack)
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        provider.load_from_path("style.css")
        Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
                
        container = Gtk.FlowBox()
        container.set_valign(Gtk.Align.START)
        #container.set_max_children_per_line(30)
        container.set_selection_mode(Gtk.SelectionMode.NONE)
        
        
        self.body.add(container)
        self.stack.add_named(self.body, "main")
        
        self.imageBox= Gtk.Box()
        self.stack.add_named(self.imageBox, "image")
        
        for image in getGtkImage():
            container.add(image)

        # Connect the on_image_clicked function to a method in MyWindow
        for child in container.get_children():
            child.get_children()[0].connect("button_press_event", self.on_image_clicked)

    def on_image_clicked(self, widget, event):
        # Call your custom function or perform actions here
        self.stack.set_visible_child_name("image")
        self.imageBox.append(Gtk.Image.new_from_file(f'images/{self.clickedImage}') )
        

get_images()
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()