.. _concepts_auth:

Authentication
==============

Depending on thte service intended to be used, an operation object will need either a
``UserKey`` or ``OAuthUser`` instance. As a best practice, it is recommended to use
ENV variables to store values to instantiate these objects (see Getting Started
> Environment Variables > :ref:`gettingstarted_envvariables_auth`).

However, most class constructors look automatically for relevant environment variables
and perform the authentication automatically.

If an explicit user creation is needed, the following classes can be used:

UserKey
-------

Used by all services except the Article Fetcher Service. Usually it's not required to
be instantiated independently as the creation of a `parent` object will get the value
from the environment.

If using this class explicitly, the following code snippet can be helpful:

.. code-block:: python

    from factiva.analytics import UserKey, SnapshotExplain
    u = UserKey('abcd1234abcd1234abcd1234abcd1234')
    se = SnapshotExplain(user_key=u)

When using ENV variables, the above snippet requires only the constructor call from the parent
class, in this case `SnapshotExplain()`.

.. code-block:: python

    from factiva.analytics import SnapshotExplain
    ar = SnapshotExplain()

OAuthUser
---------

Used by the Article Fetcher Service only. Like ``UserKey``, it is usually not required
to be instantiated independently. However, below code snippets can be helpful when using this
class explicitly:

.. code-block:: python

    from factiva.analytics import OAuthUser, ArticleRetrieval
    c_id = "0abcd1wxyz2abcd3wxyz4abcd5wxyz6o"
    uname = "9ZZZ000000-svcaccount@dowjones.com"
    pwd = "pa55WOrdpa55WOrd"
    ou = OAuthUser(client_id=c_id, username=uname, password=pwd)
    ar = ArticleFetcher(oauth_user=ou)
    ...

When using ENV variables, the above snippet requires only the constructor call from the parent
class, in this case `ArticleFetcher()`.

.. code-block:: python

    from factiva.analytics import ArticleFetcher
    ar = ArticleFetcher()
