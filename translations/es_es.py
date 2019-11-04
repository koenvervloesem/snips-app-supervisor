"""
This module contains the result sentences and intents for the English version
of the Supervisor app.
"""

# Result sentences
RESULT_BACK = "Hola, estoy aquí de nuevo"
RESULT_CONFIRM_REBOOT = "¿Quieres realmente reiniciar el sistema?"
RESULT_CONFIRM_SHUTDOWN = "¿Quieres realmente apagar el sistema?"
RESULT_DISABLE_APP = "OK, he deactivado la app {} y he reiniciado Snips action."
RESULT_ENABLE_APP = "OK, he deactivado la app  {} y he reiniciado Snips actions."
RESULT_OK = "OK"
RESULT_REBOOT = "OK, voy a reiniciar. Ahora regreso."
RESULT_RESTART_SERVICE = "OK, reinicio el servicio {}."
RESULT_RESTART_ALL_SERVICES = "OK, reinicio los servicios de Snips."
RESULT_SHUTDOWN = "OK, Voy a apagar. Te espero pronto."
RESULT_SORRY = "LO siento, he encontrado un error. Consulta los logs para resolverlo."
RESULT_SORRY_PERMISSIONS = "LO siento, no puedo cambiar los permisos de los ejecutables de las acciones."

# Intents
INTENT_CONFIRM_REBOOT = 'koan:ConfirmReboot'
INTENT_CONFIRM_SHUTDOWN = 'koan:ConfirmShutdown'
INTENT_DISABLE_APP = 'koan:DisableApp'
INTENT_ENABLE_APP = 'koan:EnableApp'
INTENT_REBOOT = 'koan:Reboot'
INTENT_RESTART_SERVICE = 'koan:RestartService'
INTENT_SHUTDOWN = 'koan:Shutdown'

# Slot types
SLOT_TYPE_APP = 'koan/snips-app'
