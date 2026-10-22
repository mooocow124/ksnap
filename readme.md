# snap v0.0.1
# This project is a WIP, come back later!

Package manager and framework for modern jailbroken Amazon Kindles

Each argument follows a structure of `action:argument`.
For example: `ksnap add:gh://mooocow124/example_snap.latest rm:someotherpackage`

You can install any .snap.zip file as a package.
For a list of commands at this time, run `ksnap help:commands`.
For flags, we use - as a prefix instead of --. For example, `ksnap -help`.

It also has a GUI (Mesquite app or just go to the URL snapcfg.kindle on your Kindle browser).

Tested devices: Kindle Paperwhite 12th gen, OS version 5.20.1, jailbroken with Vera

We'd love it if you contribute!
[https://github.com/mooocow124/ksnap](https://github.com/mooocow124/ksnap)

### To-Do List

- [ ] Add basic dependency resolution
- [ ] Add the ability to update packages
- [ ] Overhaul the CLI
- [ ] Switch to a repo-provides-packages based architecture with Git
- [ ] Dynamic submodule hydration with the above architecture