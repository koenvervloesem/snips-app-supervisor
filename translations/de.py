"""
This module contains the result sentences and intents for the English version
of the Supervisor app.
"""

# Result sentences
RESULT_BACK = "Hallo, ich bin wieder da!"
RESULT_CONFIRM_REBOOT = "Willst du wirklich das System neustarten?"
RESULT_CONFIRM_SHUTDOWN = "Willst du wirklich das System herunterfahren?"
RESULT_DISABLE_APP = "OK, Ich deaktiviere das Programm {} und starte Snips neu."
RESULT_ENABLE_APP = "OK, Ich aktiviere das Programm {} und starte Snips neu."
RESULT_OK = "OK"
RESULT_REBOOT = "Ok, ich starte das System neu. Bis gleich."
RESULT_RESTART_SERVICE = "OK, ich starte den Service {} neu."
RESULT_RESTART_ALL_SERVICES = "OK, ich starte alle Services neu."
RESULT_SHUTDOWN = "OK, ich fahre herunter. Bitte wecke mich bald wieder auf!"
RESULT_SORRY = "Entschuldigung, es ist ein Fehler aufgetragen. Bitte schau die die Logs für Details an."
RESULT_SORRY_PERMISSIONS = "Entschuldigung, Ich konnte die Berechtigung zum Ausführen der Datei nicht ändern."

# Intents
INTENT_CONFIRM_REBOOT = 'Philipp:ConfirmReboot'
INTENT_CONFIRM_SHUTDOWN = 'Philipp:ConfirmShutdown'
INTENT_DISABLE_APP = 'Philipp:DisableApp'
INTENT_ENABLE_APP = 'Philipp:EnableApp'
INTENT_REBOOT = 'Philipp:Reboot'
INTENT_RESTART_SERVICE = 'Philipp:RestartService'
INTENT_SHUTDOWN = 'Philipp:Shutdown'

# Slot types
SLOT_TYPE_APP = 'Philipp/snips-app'
