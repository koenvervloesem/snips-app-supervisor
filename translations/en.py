"""
This module contains the result sentences and intents for the English version
of the Supervisor app.
"""

# Result sentences
RESULT_BACK = "Hi, I'm back!"
RESULT_CONFIRM_REBOOT = "Do you really want to reboot the system?"
RESULT_CONFIRM_SHUTDOWN = "Do you really want to shutdown the system?"
RESULT_DISABLE_APP = "OK, I'll disable the {} app and restart all Snips actions."
RESULT_ENABLE_APP = "OK, I'll enable the {} app and restart all Snips actions."
RESULT_OK = "OK"
RESULT_REBOOT = "OK, I'll reboot now. I'll be back."
RESULT_RESTART_SERVICE = "OK, I'll restart the {} service."
RESULT_RESTART_ALL_SERVICES = "OK, I'll restart all Snips services."
RESULT_SHUTDOWN = "OK, I'll shutdown now. Please wake me up soon."
RESULT_SORRY = "Sorry, I encountered an error. Have a look at the logs to solve it."
RESULT_SORRY_PERMISSIONS = "Sorry, I couldn't change the execute permissions of the action files."

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
