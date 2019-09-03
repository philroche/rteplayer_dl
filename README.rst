===========================
RTE Player video downloader
===========================


.. image:: https://img.shields.io/pypi/v/rteplayer_dl.svg
        :target: https://pypi.python.org/pypi/rteplayer_dl

.. image:: https://img.shields.io/travis/philroche/rteplayer_dl.svg
        :target: https://travis-ci.org/philroche/rteplayer_dl

.. image:: https://readthedocs.org/projects/rteplayer-dl/badge/?version=latest
        :target: https://rteplayer-dl.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Helpful python project to download videos from RTE Player.

Uses a combination of a bookmarklet and a python script to download programmes
from RTE player for offline viewing.

* Free software: MIT license
* Documentation: https://rteplayer-dl.readthedocs.io.
* Usage: https://rteplayer-dl.readthedocs.io/en/latest/usage.html

Known issues
------------

* Programmes with run time greater than 1 hour are not watchable past the fist
  hour due to audio and video stream no longer being in sync. The reason for
  this is not yet known.
* Some downloaded videos contain multiple video tracks of different resolution.
  From my experimentation the last video track is the highest resolution.

Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
