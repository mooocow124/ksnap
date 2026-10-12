# How does ksnap work?

### This file is a WIP

The package manager itself uses a relatively simple architecture that is self-contained in [main.py](./main.py) and [actions.py](./actions.py). See later why MicroPython was chosen over standard CPython.

These are MicroPython files and are run by ksnap's bundled MicroPython runtime (compilation settings: armv7l 32 bit hard float, statically linked with musl, compiled with gcc 11 on WSL Ubuntu Resolute, everything enabled except FFI).

The greater framework including kwebonise and its related Mesquite autoregistration, as well as automatic package installation from downloading .snap.txt, are all managed by the monolith shell script daemon ksnapd, which is majorly an architectural crime.

ksnapd is registered as an Upstart service (the Kindle's init system) by ksnap's install script. It performs two tasks:
* To perform and manage ksnap and kwebonise's necessary bind mounts (see later)
* To supervise other registered daemons (such as inetd) and bind them to 