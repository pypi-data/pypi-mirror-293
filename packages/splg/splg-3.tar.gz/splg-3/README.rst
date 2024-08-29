**NAME**

::

    ``SPLG`` - Elderly, Wicked, Criminals, Handicapped


**SYNOPSIS**

::

    splg  <cmd> [key=val] [key==val]
    splgc 
    splgd


**INSTALL**

::

    $ pipx install splg
    $ pipx ensurepath

    <new terminal>

    $ splg srv > splg.service
    # mv *.service /etc/systemd/system/
    # systemctl enable splg --now

    joins #splg on localhost


**DESCRIPTION**

::

    In 2018 i informed the king of the netherlands that what he calls
    medicine in his "care" laws are not medicine but poison. Proof of
    these medicine being poison were shown to the king, who's (personal)
    kabinet wrote back that "the king took note of what i have written".

    Using poison makes the care laws used in the netherlands to provide
    care to elderly and handicapped, criminals and psychiatric patients
    not care laws but genocide laws with which the king is killing groups
    of the population by giving them poison instead of medicine in
    the "care" they are forced to undergo.

    I wrote the prosecutor asking for an arrest of the king (make him
    stop), the prosecutor decided to call it a "no basis to proceed".

    It requires a `basis to prosecute` of the prosecutor
    to get the king in his cell and his genocide, thereby, stopped.


**USAGE**

::

    without any argument the program does nothing

    $ splg
    $

    see list of commands

    $ splg cmd
    cmd,err,mod,req,thr,ver

    list of modules

    $ splg mod
    cmd,err,fnd,irc,log,mod,req,rss,tdo,thr

    start a console

    $ splgc
    >

    start a daemon

    $ splgd
    $    

**COMMANDS**

::

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    fnd - find objects 
    log - log some text
    met - add a user
    mre - displays cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    rss - add a feed
    thr - show the running threads


**CONFIGURATION**

::

    $ splg cfg 
    channel=#splg commands=True nick=splg port=6667 server=localhost

    irc

    $ splg cfg server=<server>
    $ splg cfg channel=<channel>
    $ splg cfg nick=<nick>

    sasl

    $ splg pwd <nsvnick> <nspass>
    $ splg cfg password=<frompwd>

    rss

    $ splg rss <url>
    $ splg dpl <url> <item1,item2>
    $ splg rem <url>
    $ splg nme <url> <name>

**FILES**

::

    ~/.splg
    ~/.local/bin/splg
    ~/.local/bin/splgc
    ~/.local/bin/splgd
    ~/.local/pipx/venvs/splg/

**AUTHOR**

::

    Bart Thate <bthate@dds.nl>

**COPYRIGHT**

::

    SPLG is Public Domain.
