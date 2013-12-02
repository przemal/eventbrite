Eventbrite
==========
Simple Python command line script for creating, updating and displaying Eventbrite events.

Requirements
------------
`requests <https://pypi.python.org/pypi/requests>`_

Authentication tokens
---------------------
Script needs `application <https://www.eventbrite.com/api/key/>` and `user <https://www.eventbrite.com/userkeyapi/>`
tokens to work.

Before posting new events you need to set organizer name in your
`profile <http://www.eventbrite.com/myprofile>` if you haven't done that already.

For more details, please go to:
`<http://developer.eventbrite.com/doc/authentication>`

Command examples
----------------
*All examples assume you have already setup your authentication tokens in config.json!*

.. code-block:: bash

    $ ./eventbrite.py -h
    $ ./eventbrite.py create --title 'Event title' --desc 'Event description' --date '2013-11-11 16:16'
    $ ./eventbrite.py update --id 1234 --desc 'Event description update'
    $ ./eventbrite.py details --id 9509327655

