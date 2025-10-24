import bpy


def mostrarMensajeBox(message: str = "", title: str = "Message Box", icon: str = 'INFO'):
    """Muestra mensaje en pantalla.
    
    args:
        mensaje: str
    """

    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
