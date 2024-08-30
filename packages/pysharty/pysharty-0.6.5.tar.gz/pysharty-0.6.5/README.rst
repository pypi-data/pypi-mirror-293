soyjak.party Python Library
====================
pysharty is an absolutely spine chilling genre defining bone tingling
terrifying jumpscare 'jak driven atmosphere oozing a24 released
trope subverting dark and eerie gut wrenching aesthetically heavy
craft gradual escalation soul shaking dread inducing post horror
suspenseful build up a "say more with less" approach blood curdling
kino keyed nerve wracking nail biting jaw clenching free of cheap gore
kuz, soot, doll and froot approved snopes verified reuters verified
'zellig free coal killing cobson loving fauci approved pro science
truth uncovering jannie decimating glowie zapping vtuber chudding
schizophrenic 4cuck killing shitter crashing discoal erasing
'coinslot closing NAS free anti meds soylent free wholesome pupperino
west rising heavenly holy sharty saving IAS gemerald Python library that gives access to the soyjak.party API
and an object-oriented way to browse and get board and thread
information quickly and easily.

Uses requests, respects if-modified-since headers on updating threads.
Caches thread objects. Gemmy stuff.

An absolute must if you want to interface with or scrape from soyjak.party,
using a Python script.

`Hosted Documentation <https://py8chan.readthedocs.io/en/latest/index.html>`_

`Github Repository <http://github.com/SuperWaluigi64/pysharty>`_

You can install this library `straight from
PyPi <https://pypi.python.org/pypi/pysharty>`_ with::

    pip install pysharty


**Getting Help**

If you want help, or you have some trouble using this library, put a issue on our `Github
Issue Tracker <http://github.com/SuperWaluigi64/pysharty>`_ and go fuck yourself!

Usage
-----

.. code:: python

    import pysharty
    soy = pysharty.Board('soy')
    thread = soy.get_thread(423491034)

    print(thread)

    for file in thread.files():
        print(file)
        
    # In a while...
    print("I fetched", thread.update(), "new replies.")

Documentation is located `here <https://py8chan.readthedocs.io/en/latest/index.html>`_.

License
-------

.. code:: text

                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                        Version 2, December 2004

     Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

     Everyone is permitted to copy and distribute verbatim or modified
     copies of this license document, and changing it is allowed as long
     as the name is changed.

                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
       TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

      0. You just DO WHAT THE FUCK YOU WANT TO.
