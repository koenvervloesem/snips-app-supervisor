"""
This module contains the result sentences and intents for the French version
of the Supervisor app.
"""

# Result sentences
RESULT_BACK = "Bonjour, je suis de retour !"
RESULT_CONFIRM_REBOOT = "Voulez vous vraiment redémarrer le système ?"
RESULT_CONFIRM_SHUTDOWN = "Voulez vous vraiment arrêter le système ?"
RESULT_DISABLE_APP = "OK, je vais désactiver l'application {} et redémarrer Snips."
RESULT_ENABLE_APP = "OK, je vais activer l'application {} et redémarrer Snips."
RESULT_OK = "OK"
RESULT_REBOOT = "OK, je vais redémarrer maintenant. Je reviens."
RESULT_RESTART_SERVICE = "OK, je vais redémarrer le service {}."
RESULT_RESTART_ALL_SERVICES = "OK, je vais redémarrer tous les services de Snips."
RESULT_SHUTDOWN = "OK, je vais m'éteindre maintenant. Réveille moi bientôt s'il te plaît."
RESULT_SORRY = "Désolé, j'ai rencontré une erreur. Regardez dans les logs pour résoudre le problème."
RESULT_SORRY_PERMISSIONS = "Désolé, je ne peux pas changer les permissions des fichiers d'éxècution."

# Intents
INTENT_CONFIRM_REBOOT = 'Sanlokii:ConfirmReboot'
INTENT_CONFIRM_SHUTDOWN = 'Sanlokii:ConfirmShutdown'
INTENT_DISABLE_APP = 'Sanlokii:DisableApp'
INTENT_ENABLE_APP = 'Sanlokii:EnableApp'
INTENT_REBOOT = 'Sanlokii:Reboot'
INTENT_RESTART_SERVICE = 'Sanlokii:RestartService'
INTENT_SHUTDOWN = 'Sanlokii:Shutdown'

# Slot types
SLOT_TYPE_APP = 'Sanlokii/snips-app'
