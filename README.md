# Supervisor app for Snips

With this [Snips](https://snips.ai/) app, you can reboot or shutdown the system Snips is running on, as well as restart Snips services.

## Installation

The easiest way to install this app is by adding the Snips app [Supervisor](https://console.snips.ai/store/en/skill_l6qM1pVz2ez) to your assistant in the [Snips Console](https://console.snips.ai).

## Configuration

The app needs permission to reboot and shutdown your computer and to restart system services. If your system is a systemd-based Linux distribution, such as Raspbian or Ubuntu, you can give the app the needed permissions like this:

``` shell
sudo cp /var/lib/snips/skills/snips-app-supervisor/snips-app-supervisor.sudoers /etc/sudoers.d/snips-app-supervisor
sudo chmod 0440 /etc/sudoers.d/snips-app-supervisor
```

The commands to reboot and shutdown your system and to restart Snips services can be changed in the parameters of this app: `reboot_command`, `shutdown_command` and `restart_service_command`. By default they are set up for a systemd-based Linux distribution.

By default the app asks for confirmation if you ask it to reboot or shutdown your system. This can be disabled in the app's parameters `reboot_confirm` and `shutdown_confirm`.

## Usage

This app recognizes the following intents:

*   ConfirmReboot (only enabled after the Reboot intent is activated and the `reboot_confirm` parameter is set to true) - The user confirms that he wants to reboot the system.
*   ConfirmShutdown (only enabled after the Shutdown intent is activated and the `shutdown_confirm` parameter is set to true) - The user confirms that he wants to shutdown the system.
*   Reboot - The user asks to reboot the machine Snips is running on.
*   RestartService - The user asks to restart a Snips service or all Snips services. 
*   Shutdown - The user asks to shutdown the machine Snips is running on.

## Copyright

This app is provided by [Koen Vervloesem](mailto:koen@vervloesem.eu) as open source software. See LICENSE for more information.
