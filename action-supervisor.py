#!/usr/bin/env python3
"""
This module contains a Snips app that lets you reboot or shutdown the system
and restart Snips services.
"""

import importlib
from subprocess import run, CalledProcessError
from threading import Timer

from snipskit.apps import SnipsAppMixin
from snipskit.config import AppConfig
from snipskit.hermes.apps import HermesSnipsApp
from snipskit.hermes.decorators import intent, intent_not_recognized

# Use the assistant's language.
i18n = importlib.import_module('translations.' + SnipsAppMixin().assistant['language'])

DELAY_SHUTDOWN = 5
DELAY_GREET = 5
DELAY_RESTART_SERVICE = 5


class Supervisor(HermesSnipsApp):
    """
    This app lets you reboot or shutdown the system and restart Snips services.
    """

    def initialize(self):
        """Initialize the app."""

        # Greet the user on the site ID where he has asked to reboot.
        try:
            site_id = self.config['global']['reboot_site_id']
            Timer(DELAY_GREET,
                  self.hermes.publish_start_session_notification,
                  [site_id, i18n.RESULT_BACK, '']).start()
            self.config.remove_option('global', 'reboot_site_id')
            self.config.write()
        except KeyError:  # The user hasn't asked for a reboot.
            pass

    @intent_not_recognized
    def handle_intent_not_recognized(self, hermes, intent_message):
        """Handle unrecognized intents in our dialogue.

        This ends the session with an 'OK' confirmation when we asked the user
        for confirmation and he didn't confirm."""
        session_type = intent_message.custom_data
        if session_type == 'Reboot' or session_type == 'Shutdown':
            hermes.publish_end_session(intent_message.session_id,
                                       i18n.RESULT_OK)

    # Restart service

    @intent(i18n.INTENT_RESTART_SERVICE)
    def handle_restart_service(self, hermes, intent_message):
        """Handle the intent RestartService."""
        if intent_message.slots and intent_message.slots.snips_service:
            service = intent_message.slots.snips_service.first().value
        else:
            service = ''

        self.announce_and_restart_service(intent_message, service)

    def announce_and_restart_service(self, intent_message, service=''):
        """Announce that a Snips service or all Snips services will be
        restarted and then restart it/them.
        """
        if service:
            result_sentence = i18n.RESULT_RESTART_SERVICE.format(service)
        else:
            result_sentence = i18n.RESULT_RESTART_ALL_SERVICES

        self.hermes.publish_end_session(intent_message.session_id, result_sentence)
        restart_service_command = self.config['global']['restart_service_command']
        Timer(DELAY_RESTART_SERVICE,
              self.restart_service,
              [intent_message.site_id, restart_service_command, service]).start()

    def restart_service(self, site_id, restart_service_command, service=''):
        """Run the restart service command."""
        if not service:
            service = 'snips-*'

        try:
            run(restart_service_command.format(service).split(), check=True)
        except CalledProcessError:
            self.hermes.publish_start_session_notification(site_id, i18n.RESULT_SORRY, '')

    # Reboot

    @intent(i18n.INTENT_REBOOT)
    def handle_reboot(self, hermes, intent_message):
        """Handle the intent Reboot."""
        try:
            confirmation_needed = self.config.getboolean('global',
                                                         'reboot_confirm',
                                                         fallback=True)
        except ValueError:
            confirmation_needed = True

        if confirmation_needed:
            result_sentence = i18n.RESULT_CONFIRM_REBOOT
            hermes.publish_continue_session(intent_message.session_id,
                                            result_sentence,
                                            [i18n.INTENT_CONFIRM_REBOOT],
                                            custom_data='Reboot',
                                            send_intent_not_recognized=True)
        else:
            self.announce_and_reboot(intent_message)

    @intent(i18n.INTENT_CONFIRM_REBOOT)
    def handle_confirm_reboot(self, hermes, intent_message):
        """Handle the intent ConfirmReboot."""
        self.announce_and_reboot(intent_message)

    def announce_and_reboot(self, intent_message):
        """Announce that the system will be rebooted and reboot after a delay.
        """
        result_sentence = i18n.RESULT_REBOOT
        self.hermes.publish_end_session(intent_message.session_id, result_sentence)
        self.config['global']['reboot_site_id'] = intent_message.site_id
        self.config.write()
        reboot_command = self.config['global']['reboot_command']
        Timer(DELAY_SHUTDOWN, self.reboot, [intent_message.site_id,
                                            reboot_command]).start()

    def reboot(self, site_id, reboot_command):
        """Run the reboot command."""
        try:
            run(reboot_command.split(), check=True)
        except CalledProcessError:
            self.hermes.publish_start_session_notification(site_id, i18n.RESULT_SORRY, '')
            self.config.remove_option('global', 'reboot_site_id')
            self.config.write()

    # Shutdown

    @intent(i18n.INTENT_SHUTDOWN)
    def handle_shutdown(self, hermes, intent_message):
        """Handle the intent Shutdown."""
        try:
            confirmation_needed = self.config.getboolean('global',
                                                         'shutdown_confirm',
                                                         fallback=True)
        except ValueError:
            confirmation_needed = True

        if confirmation_needed:
            result_sentence = i18n.RESULT_CONFIRM_SHUTDOWN
            hermes.publish_continue_session(intent_message.session_id,
                                            result_sentence,
                                            [i18n.INTENT_CONFIRM_SHUTDOWN],
                                            custom_data='Shutdown',
                                            send_intent_not_recognized=True)
        else:
            self.announce_and_shutdown(intent_message)

    @intent(i18n.INTENT_CONFIRM_SHUTDOWN)
    def handle_confirm_shutdown(self, hermes, intent_message):
        """Handle the intent ConfirmShutdown."""
        self.announce_and_shutdown(intent_message)

    def announce_and_shutdown(self, intent_message):
        """Announce that the system will be shutdown and shutdown after a
        delay.
        """
        result_sentence = i18n.RESULT_SHUTDOWN
        self.hermes.publish_end_session(intent_message.session_id, result_sentence)
        shutdown_command = self.config['global']['shutdown_command']
        Timer(DELAY_SHUTDOWN, self.shutdown, [intent_message.site_id,
                                              shutdown_command]).start()

    def shutdown(self, site_id, shutdown_command):
        """Run the shutdown command."""
        try:
            run(shutdown_command.split(), check=True)
        except CalledProcessError:
            self.hermes.publish_start_session_notification(site_id, i18n.RESULT_SORRY, '')


if __name__ == "__main__":
    Supervisor(config=AppConfig())
