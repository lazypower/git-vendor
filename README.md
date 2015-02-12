# Git Vendor

This is a utility to aid in vendoring software projects from Git to => [VCS|Directory]

## Why this exists

I like to track my upstream development in github, and I have a hard dependency on some projects that live in bzr/Launchpad. BZR and Launchpad are both great systems, I just have a long running preference for git/github. This python module allows me to track and maintain my history in git, while running exports for tag releases to a directory that is independently tracked by BZR.

I'm not so much concerned with the commit history as I am with ensuring my tags are what make the porting phase, and they are high quality without requiring a joint VCS tree and other plugin wizardry.

## How it works

The plugin only works with git tags, and will not operate on a dirty branch. This allows me to adopt the workflow of cycle until features/bugs are complete in a given milestone. Export that code to the bzr repository and run a checkin of everything that happened from A -> Z along with a Changelog to track what happened independently of the BZR VCS.  This is a fairly simple process that can be done manually without much fuss - but like anything I do repeatedly: it's even nicer to have a tool do the drone work for me.


## Getting Started

Clone the repository

    git clone http://github.com/chuckbutler/git-vendor.git
    cd git-vendor

Create a virtualenv to isolate dependencies from your system

    virtualenv .venv/
    source .venv/bin/activate
    python setup.py install

While the virtual env is active, you can call git-vendor like you would any other executable.

    git-vendor -h

#### Basic Usage

git-vendor works with a single initialized configuration file.

    git-vendor init

This will create a .vendor-rc file which you can edit and place ignored files. It's pre-populated
with some common patterns for you.

    git tag mytag

When you are ready to vendor a git repository to bzr:

    git-vendor sync -d /path/to/bzr/repository

you will be presented with a list of tags from your git repo to pick and export. Now you can head
over to your bzr repository, commit and push as you see fit. Enjoy!


