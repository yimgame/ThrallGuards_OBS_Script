import obspython as obs
import threading
import time

# Variables globales
nombre_fuente = ""
tiempo_delay = 5

# --- Lógica principal ---
def activar_fuente_y_detener():
    escena_actual = obs.obs_frontend_get_current_scene()
    escena = obs.obs_scene_from_source(escena_actual)
    fuente = obs.obs_scene_find_source(escena, nombre_fuente)

    if fuente:
        obs.obs_sceneitem_set_visible(fuente, True)
        print(f"✅ Fuente '{nombre_fuente}' activada")
    else:
        print(f"❌ Fuente '{nombre_fuente}' no encontrada en la escena actual")

    obs.obs_source_release(escena_actual)
    time.sleep(tiempo_delay)

    if obs.obs_frontend_recording_active():
        obs.obs_frontend_recording_stop()
        print(f"🛑 Grabación detenida después de {tiempo_delay} segundos")
    else:
        print("⚠️ No hay grabación activa para detener")

# --- Ejecutar en hilo ---
def ejecutar_delay():
    threading.Thread(target=activar_fuente_y_detener).start()

# --- Botón de interfaz y hotkey comparten esta función ---
def boton_ejecutar(props=None, prop=None):
    ejecutar_delay()

# --- Hotkey llama a la misma función que el botón ---
def lanzar_accion(pressed=None):
    if pressed:
        boton_ejecutar()

# --- Interfaz del Script ---
def script_description():
    return "Activa una fuente y detiene la grabación tras un delay."

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "nombre_fuente", "Nombre de la fuente", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "tiempo_delay", "Delay antes de detener (segundos)", 1, 600, 1)
    obs.obs_properties_add_button(props, "boton_ejecutar", "🎬 Ejecutar ahora", boton_ejecutar)
    return props

def script_update(settings):
    global nombre_fuente, tiempo_delay
    nombre_fuente = obs.obs_data_get_string(settings, "nombre_fuente")
    tiempo_delay = obs.obs_data_get_int(settings, "tiempo_delay")

# --- Hotkey ---
hotkey_id = obs.OBS_INVALID_HOTKEY_ID

def script_load(settings):
    global hotkey_id
    hotkey_id = obs.obs_hotkey_register_frontend(
        "mi_hotkey_fuente_y_detener",
        "🎥 Activar fuente y detener grabación",
        lanzar_accion
    )
    hotkey_saved_array = obs.obs_data_get_array(settings, "mi_hotkey_fuente_y_detener")
    obs.obs_hotkey_load(hotkey_id, hotkey_saved_array)
    obs.obs_data_array_release(hotkey_saved_array)

def script_save(settings):
    hotkey_array = obs.obs_hotkey_save(hotkey_id)
    obs.obs_data_set_array(settings, "mi_hotkey_fuente_y_detener", hotkey_array)
    obs.obs_data_array_release(hotkey_array)
