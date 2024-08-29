.. _manual:


.. raw:: html

    <br>


.. title:: Manual


.. raw:: html

    <center>

manual
######


.. raw:: html

    </center>
    <br>

**NAME**

 | ``PRESIDENT`` - Reconsider OTP-CR-117/19


**SYNOPSIS**

 ::

  president <cmd> [key=val] 
  president <cmd> [key==val]
  president [-c] [-d] [-v]


**DESCRIPTION**


 ``PRESIDENT`` is a python3 IRC bot is intended to be programmable  in a
 static, only code, no popen, no user imports and no reading modules from
 a directory, way. It can show genocide and suicide stats of king netherlands
 his genocide into a IRC channel, display rss feeds and log simple text
 messages, source is `here <source.html>`_.



**INSTALL**

 with sudo::

  $ python3 -m pip install president

 as user::

  $ pipx install president

 or download the tar, see::

  https://pypi.org/project/president


**USAGE**


 list of commands::

    $ president cmd
    cmd,err,flt,sts,thr,upt

 start a console::

    $ president -c
    >

 start additional modules::

    $ president mod=<mod1,mod2> -c
    >

 list of modules::

    $ president mod
    cmd,err,flt,fnd,irc,log,mdl,mod,
    req, rss,slg,sts,tdo,thr,upt,ver

 to start irc, add mod=irc when
 starting::

     $ president mod=irc -c

 to start rss, also add mod=rss
 when starting::

     $ president mod=irc,rss -c

 start as daemon::

     $ president mod=irc,rss -d
     $ 


**CONFIGURATION**


 *irc*

 ::

    $ president cfg server=<server>
    $ president cfg channel=<channel>
    $ president cfg nick=<nick>

 *sasl*

 ::

    $ president pwd <nsvnick> <nspass>
    $ president cfg password=<frompwd>

 *rss*

 ::

    $ president rss <url>
    $ president dpl <url> <item1,item2>
    $ president rem <url>
    $ president nme <url< <name>


**COMMANDS**


 ::

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    ftc - runs a fetching batch
    fnd - find objects 
    flt - instances registered
    log - log some text
    mdl - genocide model
    met - add a user
    mre - displays cached output
    nck - changes nick on irc
    now - genocide stats
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    req - reconsider
    rss - add a feed
    slg - slogan
    thr - show the running threads
    tpc - genocide stats into topic


**FILES**

 ::

    ~/.local/bin/president
    ~/.local/pipx/venvs/president/
    /usr/local/bin/president
    /usr/local/share/doc/president


**AUTHOR**


 ::
 
    Bart Thate <bthate@dds.nl>


**COPYRIGHT**

 ::

    PRESIDENT is Public Domain.
