NAME

::

    SPLG - Stop Poison Law Genocide. Elderly, Wicked, Criminals, Handicapped.


SYNOPSIS

::

    splg  <cmd> [key=val] [key==val]
    splg  [-c] [-v]

    options are:

    -c     start console
    -v     use verbose


INSTALL

::

    $ pipx install splg
    $ pipx ensurepath


DESCRIPTION

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


USAGE

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

    use -c to start a console

    $ splg -c

    use mod=<name1,name2> to load additional modules

    $ splg -c mod=irc,rss
    >

    use -v for verbose

    $ splg -cv mod=irc
    Jul 11 23:13:32 2024 SPLG CV MOD,CMD,ERR,THR,CMD,ERR,HLP,IRC,MOD,REQ,RSS,THR,UPT

    use the -i options to start service defined in one of the loaded modules


COMMANDS

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


CONFIGURATION

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


SYSTEMD

::

    save the following it in /etc/systemd/system/splg.service and
    replace "<user>" with the user running pipx

    [Unit]
    Description=Stop Poison Law Genocide. Elderly, Wicked, Criminals, Handicapped.
    Requires=network-online.target
    After=network-online.target

    [Service]
    Type=simple
    User=<user>
    Group=<user>
    WorkingDirectory=/home/<user>/.splg
    ExecStart=/home/<user>/.local/pipx/venvs/splg/bin/splg -d
    RemainAfterExit=yes

    [Install]
    WantedBy=default.target

    then run this

    $ mkdir ~/.splg
    $ sudo systemctl enable splg --now

    default channel/server is #splg on localhost

FILES

::

    ~/.splg
    ~/.local/bin/splg
    ~/.local/pipx/venvs/splg/

AUTHOR

::

    Bart Thate <bthate@dds.nl>

COPYRIGHT

::

    SPLG is Public Domain.
