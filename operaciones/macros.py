import bpy
addon_keymaps = []

def add_hotkey():
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon

        km = kc.keymaps.new(name='Sequencer', space_type='SEQUENCE_EDITOR')

        kmi = km.keymap_items.new("scene.superinsertar", type="Y", value="PRESS", ctrl=True, shift=True)
        kmi.properties.macros = True

        kmi = km.keymap_items.new("scene.insertaraudio", 'O', 'PRESS', ctrl=True, shift=True)
        kmi.properties.macros = True

        kmi = km.keymap_items.new("scene.superaliniar", type="R", value="PRESS", ctrl=True, shift=False)
        kmi.properties.macros = True

        kmi = km.keymap_items.new("scene.superzoon", type="P", value="PRESS", ctrl=True, shift=False)
        kmi.properties.macros = True
        kmi.properties.incrementro = False

        kmi = km.keymap_items.new("scene.superzoon", type="U", value="PRESS", ctrl=True, shift=False)
        kmi.properties.macros = True
        kmi.properties.incrementro = True

        kmi = km.keymap_items.new("scene.moverclip", type="J", value="PRESS", ctrl=True, shift=False)
        kmi.properties.macros = True

        addon_keymaps.append((km, kmi))

def remove_hotkey():
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
        addon_keymaps.clear()