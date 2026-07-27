BLENDER ?= flatpak run org.blender.Blender
PLUGIN_DIR ?= $(CURDIR)
ADDON_MODULE ?= ChepeCarlos_Plugin_Blender
DIST_DIR ?= dist
BLENDER_CONFIG_BASE := $(HOME)/.var/app/org.blender.Blender/config/blender
BLENDER_CONFIG_VERSION ?= $(shell ls -d $(BLENDER_CONFIG_BASE)/[0-9]*.[0-9]* 2>/dev/null | sort -V | tail -1 | xargs basename 2>/dev/null)
ADDONS_DIR ?= $(BLENDER_CONFIG_BASE)/$(BLENDER_CONFIG_VERSION)/scripts/addons
ZIP_NAME ?= $(ADDON_MODULE)-$(shell date +%Y%m%d-%H%M%S).zip

LOAD_PLUGIN := import sys, importlib.util; spec = importlib.util.spec_from_file_location('$(ADDON_MODULE)', '$(PLUGIN_DIR)/__init__.py', submodule_search_locations=['$(PLUGIN_DIR)']); addon = importlib.util.module_from_spec(spec); sys.modules['$(ADDON_MODULE)'] = addon; spec.loader.exec_module(addon)

.PHONY: blenderaddon blenderaddon-dev blenderaddon-bg blenderaddon-check blenderaddon-reload zip zlip install-local info

info:
	@echo "Blender:  $(BLENDER)"
	@echo "Version:  $(BLENDER_CONFIG_VERSION)"
	@echo "Addons:   $(ADDONS_DIR)"

blenderaddon:
	$(BLENDER) --factory-startup --python-expr "$(LOAD_PLUGIN); addon.register()"

blenderaddon-dev:
	$(BLENDER) --python-expr "$(LOAD_PLUGIN); addon.register(); print('ADDON_DEV_LOADED')"

blenderaddon-bg:
	$(BLENDER) --background --factory-startup --python-expr "$(LOAD_PLUGIN); addon.register(); print('REGISTER_OK'); addon.unregister(); print('UNREGISTER_OK')"

blenderaddon-check:
	$(BLENDER) --background --factory-startup --python-expr "import bpy; print(bpy.app.version_string)"

blenderaddon-reload:
	$(BLENDER) --background --factory-startup --python-expr "$(LOAD_PLUGIN); addon.register(); addon.unregister(); [sys.modules.pop(k) for k in list(sys.modules) if '$(ADDON_MODULE)' in k]; $(LOAD_PLUGIN); addon.register(); addon.unregister(); print('ADDON_RELOAD_OK')"

zip:
	mkdir -p "$(DIST_DIR)/.zip_tmp/$(ADDON_MODULE)"
	rsync -a --delete \
		--exclude ".git/" \
		--exclude ".mypy_cache/" \
		--exclude ".vscode/" \
		--exclude "__pycache__/" \
		--exclude "operaciones/__pycache__/" \
		--exclude "$(DIST_DIR)/" \
		./ "$(DIST_DIR)/.zip_tmp/$(ADDON_MODULE)/"
	cd "$(DIST_DIR)/.zip_tmp" && zip -r "../$(ZIP_NAME)" "$(ADDON_MODULE)"
	rm -rf "$(DIST_DIR)/.zip_tmp"
	@echo "ZIP listo en $(DIST_DIR)/$(ZIP_NAME)"

zlip: zip

install-local:
	mkdir -p "$(ADDONS_DIR)/$(ADDON_MODULE)"
	rsync -a --delete \
		--exclude ".git/" \
		--exclude ".mypy_cache/" \
		--exclude ".vscode/" \
		--exclude "__pycache__/" \
		--exclude "operaciones/__pycache__/" \
		--exclude "$(DIST_DIR)/" \
		./ "$(ADDONS_DIR)/$(ADDON_MODULE)/"
	@echo "Addon instalado en $(ADDONS_DIR)/$(ADDON_MODULE)"
