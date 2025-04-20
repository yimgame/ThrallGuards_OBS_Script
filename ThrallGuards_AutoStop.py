"""
ThrallGuards AutoStop OBS Script

This script was created by Yim with the help of ChatGPT-4o.
It activates an outro source and stops recording after a delay.

Hey everyone!  
I'm Yim, and this is the very first OBS script I've shared.  
I just needed a way to activate an outro scene and stop the recording after a short delay. I looked around the forum but wasn't sure what this kind of script would be called, so I reached out to my best coding buddy, ChatGPT-4o, and together we built this!

It's a simple script, but it gets the job done. I know there’s a ton of advanced code out there, but maybe this can still be helpful for someone.

Any feedback or suggestions are very welcome.  
Best regards from me (and from the Thrall Guards, the greatest WoW guild of all time 😄⚔️)!
"""

import obspython as obs
import threading
import time

# Global variables
source_name = ""
delay_time = 5

# --- Main logic ---
def activate_source_and_stop():
    current_scene_source = obs.obs_frontend_get_current_scene()
    scene = obs.obs_scene_from_source(current_scene_source)
    source = obs.obs_scene_find_source(scene, source_name)

    if source:
        obs.obs_sceneitem_set_visible(source, True)
        print(f"✅ Source '{source_name}' activated")
    else:
        print(f"❌ Source '{source_name}' not found in the current scene")

    obs.obs_source_release(current_scene_source)
    time.sleep(delay_time)

    if obs.obs_frontend_recording_active():
        obs.obs_frontend_recording_stop()
        print(f"🛑 Recording stopped after {delay_time} seconds")
    else:
        print("⚠️ No active recording to stop")

# --- Run in a separate thread ---
def run_with_delay():
    threading.Thread(target=activate_source_and_stop).start()

# --- Shared button/hotkey callback ---
def on_button_pressed(props=None, prop=None):
    run_with_delay()

# --- Hotkey triggers same logic as the button ---
def on_hotkey_pressed(pressed=None):
    if pressed:
        on_button_pressed()

# --- Script UI ---
def script_description():
    return "Activates a source and stops the recording after a delay."

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "source_name", "Source name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "delay_time", "Delay before stopping (seconds)", 1, 600, 1)
    obs.obs_properties_add_button(props, "run_button", "🎬 Run Now", on_button_pressed)
    return props

def script_update(settings):
    global source_name, delay_time
    source_name = obs.obs_data_get_string(settings, "source_name")
    delay_time = obs.obs_data_get_int(settings, "delay_time")

# --- Hotkey setup ---
hotkey_id = obs.OBS_INVALID_HOTKEY_ID

def script_load(settings):
    global hotkey_id
    hotkey_id = obs.obs_hotkey_register_frontend(
        "thrallguards_hotkey_stop_after_outro",
        "🎥 Activate source and stop recording",
        on_hotkey_pressed
    )
    hotkey_saved_array = obs.obs_data_get_array(settings, "thrallguards_hotkey_stop_after_outro")
    obs.obs_hotkey_load(hotkey_id, hotkey_saved_array)
    obs.obs_data_array_release(hotkey_saved_array)

def script_save(settings):
    hotkey_array = obs.obs_hotkey_save(hotkey_id)
    obs.obs_data_set_array(settings, "thrallguards_hotkey_stop_after_outro", hotkey_array)
    obs.obs_data_array_release(hotkey_array)
