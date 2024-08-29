.. _manual:

.. raw:: html

    <br><br>

.. title:: Manual


**NAME**

    ``PRESIDENT`` - Bejaarden, Gehandicapten, Criminelen, Psychiatrische Patienten `! <source.html>`_


**SYNOPSIS**

    ::

        president  <cmd> [key=val] [key==val]
        presidentc [-i] [-v]
        presidentd 


**DESCRIPTION**


    Op 20 Oktober 2012 heb ik na correspondentie met de Koningin een klacht tegen de Nederland ingedient (Thate tegen Nederland 69389/12). De klacht betrof het falen van de
    (F)ACT methodiek, de methode die GGZ Nederland gebruikt om vorm te geven aan de wetten die gedwongen behandeling in Nederland mogelijk maken. De uitspraak is niet-ontvankelijk.


**INSTALL**

    ::

        $ pipx install president
        $ pipx ensurepath

        <new terminal>

        $ president srv > president.service
        $ sudo mv *.service /etc/systemd/system/
        $ sudo systemctl enable president --now

        joins #president on localhost


**USAGE**

    without any argument the bot does nothing

    ::

        $ president
        $

    see list of commands

    ::

        $ president cmd
        cmd,req,skl,srv


    start a console

    ::

        $ presidentc
        >

    start daemon

    ::

        $ presidentd
        $ 


    show request to the prosecutor

    ::

        $ president req
        Information and Evidence Unit
        Office of the Prosecutor
        Post Office Box 19519
        2500 CM The Hague
        The Netherlands


**CONFIGURATION**

    irc

    ::

        $ president cfg server=<server>
        $ president cfg channel=<channel>
        $ president cfg nick=<nick>

    sasl

    ::

        $ president pwd <nsvnick> <nspass>
        $ president cfg password=<frompwd>

    rss

    ::

        $ president rss <url>
        $ president dpl <url> <item1,item2>
        $ president rem <url>
        $ president nme <url> <name>


**COMMANDS**

    ::

        cfg - irc configuration
        cmd - commands
        mre - displays cached output
        pwd - sasl nickserv name/pass
        req - reconsider


**SOURCE**


    source is :ref:`here <source>`


**FILES**

    ::

        ~/.president 
        ~/.local/bin/president
        ~/.local/bin/presidentc
        ~/.local/bin/presidentd
        ~/.local/pipx/venvs/president/*


**AUTHOR**

    Bart Thate <bthate@dds.nl>


**COPYRIGHT**

    ``PRESIDENT`` is Public Domain.
