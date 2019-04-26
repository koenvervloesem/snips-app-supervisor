#!/usr/bin/env python3
"""
This module contains a Snips app that lets you reboot or shutdown the system
and restart Snips services.
"""

import importlib
from pathlib import Path
from subprocess import run, CalledProcessError
from threading import Timer

import yaml

from snipskit.apps import SnipsAppMixin
from snipskit.config import AppConfig
from snipskit.hermes.apps import HermesSnipsApp
from snipskit.hermes.decorators import intent, intent_not_recognized
from snipskit.mqtt.client import publish_single

# Use the assistant's language.
i18n = importlib.import_module('translations.' + SnipsAppMixin().assistant['language'])

DELAY_SHUTDOWN = 5
DELAY_GREET = 5
DELAY_RESTART_SERVICE = 5

INJECTION_PERFORM = 'hermes/injection/perform'


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

        # Inject the names of the installed apps.
        apps = list(self.app_directories().keys())
        injections = {'operations': [['add', {i18n.SLOT_TYPE_APP: apps}]]}
        publish_single(self.snips.mqtt, INJECTION_PERFORM, injections)

    @intent_not_recognized
    def handle_intent_not_recognized(self, hermes, intent_message):
        """Handle unrecognized intents in our dialogue.

        This ends the session with an 'OK' confirmation when we asked the user
        for confirmation and he didn't confirm."""
        session_type = intent_message.custom_data
        if session_type == 'Reboot' or session_type == 'Shutdown':
            hermes.publish_end_session(intent_message.session_id,
                                       i18n.RESULT_OK)

    def app_directories(self):
        """Get a dict of the installed apps and their directory."""
        apps = [app.name for app in (Path(self.assistant.filename).parent / 'snippets').iterdir()]

        try:
            skills_dir = Path(self.snips['user_dir']) / 'skills'
        except KeyError:
            skills_dir = Path('/var/lib/snips/skills')

        with (Path(self.assistant.filename).parent / 'Snipsfile.yaml').open('rt') as snips_file:
            skill_repos = yaml.safe_load(snips_file)['skills']

        app_repo_names = {item['name']: Path(item['url']).name for item in skill_repos}

        app_dirs = {}
        for app in apps:
            app_name = app[app.find('.')+1:].replace('_', ' ')
            if app in app_repo_names:
                app_dirs[app_name] = skills_dir / app_repo_names[app]
            else:
                app_dirs[app_name] = skills_dir / app

        return app_dirs

    def chmod_app(self, hermes, intent_message, result_sentence, mode):
        """Change the permissions of an app."""
        if intent_message.slots and intent_message.slots.app:
            app = intent_message.slots.app.first().value
            hermes.publish_end_session(intent_message.session_id,
                                       result_sentence.format(app))
            app_dir = self.app_directories()[app]
            for action in list(app_dir.glob('action-*')):
                try:
                    action.chmod(mode)
                except CalledProcessError:
                    hermes.publish_end_session(intent_message.session_id,
                                               i18n.RESULT_SORRY_PERMISSIONS)
            restart_service_command = self.config['global']['restart_service_command']
            Timer(DELAY_RESTART_SERVICE,
                  self.restart_service,
                  [intent_message.site_id, restart_service_command, 'snips-skill-server']).start()

    # Disable app
    @intent(i18n.INTENT_DISABLE_APP)
    def handle_disable_app(self, hermes, intent_message):
        """Handle the intent DisableApp."""
        self.chmod_app(hermes, intent_message, i18n.RESULT_DISABLE_APP, 0o644)

    # Enable app
    @intent(i18n.INTENT_ENABLE_APP)
    def handle_enable_app(self, hermes, intent_message):
        """Handle the intent EnableApp."""
        self.chmod_app(hermes, intent_message, i18n.RESULT_ENABLE_APP, 0o755)

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
            service = 'snips-analytics snips-asr snips-audio-server'
                      ' snips-dialogue snips-hotword snips-injection snips-nlu'
                      ' snips-skill-server snips-tts'

        try:
            run(restart_service_command.format(service).split(), check=True)
        except CalledProcessError:
            self.hermes.publish_start_session_notification(site_id, i18n.RESULT_SORRY, '')

    def confirm_and_do(self, intent_message, confirm_option, result_sentence, confirm_intent, custom_data, function):
        """Ask confirmation and do something."""
        confirmation_needed = self.config.getboolean('global',
                                                     confirm_option,
                                                     fallback=True)
        if confirmation_needed:
            self.hermes.publish_continue_session(intent_message.session_id,
                                                 result_sentence,
                                                 [confirm_intent],
                                                 custom_data=custom_data,
                                                 send_intent_not_recognized=True)
        else:
            function(intent_message)

    # Reboot
    @intent(i18n.INTENT_REBOOT)
    def handle_reboot(self, hermes, intent_message):
        """Handle the intent Reboot."""
        self.confirm_and_do(intent_message,
                            'reboot_confirm',
                            i18n.RESULT_CONFIRM_REBOOT,
                            i18n.INTENT_CONFIRM_REBOOT,
                            'Reboot',
                            self.announce_and_reboot)

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
        self.confirm_and_do(intent_message,
                            'shutdown_confirm',
                            i18n.RESULT_CONFIRM_SHUTDOWN,
                            i18n.INTENT_CONFIRM_SHUTDOWN,
                            'Shutdown',
                            self.announce_and_shutdown)

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
