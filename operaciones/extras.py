import bpy

def MostarMensajeBox(message="", title="Message Box", icon='INFO'):
    """Muestra mensaje en pantalla."""
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
