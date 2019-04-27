# Supervisor app for Snips
[![Build status](https://api.travis-ci.com/koenvervloesem/snips-app-supervisor.svg?branch=master)](https://travis-ci.com/koenvervloesem/snips-app-supervisor) [![Maintainability](https://api.codeclimate.com/v1/badges/b3a76052925c4dfb5941/maintainability)](https://codeclimate.com/github/koenvervloesem/snips-app-supervisor/maintainability) [![Code quality](https://api.codacy.com/project/badge/Grade/42c7678a1b1b4f4aa6059c054bfe98cf)](https://app.codacy.com/app/koenvervloesem/snips-app-supervisor) [![Python versions](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org) [![GitHub license](https://img.shields.io/github/license/koenvervloesem/snips-app-supervisor.svg)](https://github.com/koenvervloesem/snips-app-supervisor/blob/master/LICENSE) [![Languages](https://img.shields.io/badge/i18n-en|fr-brown.svg)](https://github.com/koenvervloesem/snips-supervisor/tree/master/translations) [![Snips App Store](https://img.shields.io/badge/snips-app-blue.svg)](https://console.snips.ai/store/en/skill_l6qM1pVz2ez)

With this [Snips](https://snips.ai/) app, you can reboot or shutdown the system Snips is running on, as well as restart Snips services.

## Installation

The easiest way to install this app is by adding the corresponding Snips app to your assistant in the [Snips Console](https://console.snips.ai):

*   English: [Supervisor](https://console.snips.ai/store/en/skill_l6qM1pVz2ez)
*   French: [Superviseur](https://console.snips.ai/store/fr/skill_BWAwo87MxrW)

## Configuration

The app needs permission to reboot and shutdown your computer and to restart system services. If your system is a systemd-based Linux distribution, such as Raspbian or Ubuntu, you can give the app the needed permissions like this:

``` shell
sudo cp /var/lib/snips/skills/snips-app-supervisor/snips-app-supervisor.sudoers /etc/sudoers.d/snips-app-supervisor
sudo chmod 0440 /etc/sudoers.d/snips-app-supervisor
```

The commands to reboot and shutdown your system and to restart Snips services can be changed in the parameters of this app: `reboot_command`, `shutdown_command` and `restart_service_command`. By default they are set up for a systemd-based Linux distribution.

By default the app asks for confirmation if you ask it to reboot or shutdown your system. This can be disabled in the app's parameters `reboot_confirm` and `shutdown_confirm`.

For disabling and enabling apps, the `snips-injection` service should be running, because the names of the installed apps are injected in the vocabulary of Snips.

## Usage

This app recognizes the following intents:

*   ConfirmReboot (only enabled after the Reboot intent is activated and the `reboot_confirm` parameter is set to true) - The user confirms that he wants to reboot the system.
*   ConfirmShutdown (only enabled after the Shutdown intent is activated and the `shutdown_confirm` parameter is set to true) - The user confirms that he wants to shutdown the system.
*   EnableApp - The user asks to enable a Snips app.
*   DisableApp - The user asks to disable a Snips app.
*   Reboot - The user asks to reboot the machine Snips is running on.
*   RestartService - The user asks to restart a Snips service or all Snips services.
*   Shutdown - The user asks to shutdown the machine Snips is running on.

## Copyright

This app is provided by [Koen Vervloesem](mailto:koen@vervloesem.eu) as open source software. See LICENSE for more information.
