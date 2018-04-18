asciinema editor
================

Video editing tool for `asciinema <https://asciinema.org>`_ video files.

Usage
-----

Add an offset to the timestamp of all events::

    ./asciinema-editor.py add-offset <input file> <output file> <offset>

Limit idle time between events (similar to ``asciinema rec -i`` option, but
after the recording has been made)::

    ./asciinema-editor.py limit-idle-time <input file> <output file> <idle time limit>

License
-------

Apache License 2.0
