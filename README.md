A proof-of-concept for a python + qt + qml FAF client. Probably nothing will come of it.

Running
=======

* Setup a py3.6+ virtualenv. Install stuff from requirements.txt.
* Add src/ to PYTHONPATH.
* Run `python3 src/main.py`.


Roadmap
=======

In case this gets somewhere.

Done:
* Connecting to server, logging in/out.
* Managing things from the server (players, games, channels etc.).
* IRC client plus basic views.
* Basic game view.
* Basic news.
* Downloading map previews.

Todo:
* Config, default settings, persistence (probably in yaml).
* Packaging for Windows & Linux.
  * Appveyor plus Travis integration.
* FIXME and TODO fixes.
* More consistent management of irc / lobbyserver connection.
* Tests. It's about time there were some.
* UI improvements, some UI pieces can't be told apart.
* Main menu, with settings.
* FAF api interface, plus a component that uses it.

Future:
* Downloading maps and mods.
* Map and mod vault.
* Interface to FA process - setting it up for a game, running it etc.
* ICE adapter integration.
* Ladder games.
* Coop games.
* Other tabs.
* Bells and whistles like notifications.
