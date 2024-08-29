.. _manual:

.. raw:: html

    <br><br>

.. title:: Manual


.. raw:: html

    <center>

manual
======

.. raw:: html

    </center>
    <br>



**NAME**

    ``KAMER`` - Bejaarden, Gehandicapten, Criminelen, Psychiatrische Patienten `! <source.html>`_


**SYNOPSIS**

    ::

        kamer  <cmd> [key=val] [key==val]
        kamerc [-i] [-v]
        kamerd 


**DESCRIPTION**


    Op 20 Oktober 2012 heb ik na correspondentie met de Koningin een klacht tegen de Nederland ingedient (Thate tegen Nederland 69389/12). De klacht betrof het falen van de
    (F)ACT methodiek, de methode die GGZ Nederland gebruikt om vorm te geven aan de wetten die gedwongen behandeling in Nederland mogelijk maken. De uitspraak is niet-ontvankelijk.


**INSTALL**

    ::

        $ pipx install kamer
        $ pipx ensurepath

        <new terminal>

        $ kamer srv > president.service
        $ sudo mv *.service /etc/systemd/system/
        $ sudo systemctl enable kamer --now

        joins #kamer on localhost


**USAGE**

    without any argument the bot does nothing

    ::

        $ kamer
        $

    see list of commands

    ::

        $ kamer cmd
        cmd,req,skl,srv


    start a console

    ::

        $ kamerc
        >

    start daemon

    ::

        $ kamerd
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

        $ kamer cfg server=<server>
        $ kamer cfg channel=<channel>
        $ kamer cfg nick=<nick>

    sasl

    ::

        $ kamer pwd <nsvnick> <nspass>
        $ kamer cfg password=<frompwd>

    rss

    ::

        $ kamer rss <url>
        $ kamer dpl <url> <item1,item2>
        $ kamer rem <url>
        $ kamer nme <url> <name>


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

        ~/.kamer 
        ~/.local/bin/kamer
        ~/.local/bin/kamerc
        ~/.local/bin/kamerd
        ~/.local/pipx/venvs/kamer/*


**AUTHOR**

    Bart Thate <bthate@dds.nl>


**COPYRIGHT**

    ``KAMER`` is Public Domain.
