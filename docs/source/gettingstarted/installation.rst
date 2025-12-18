Installation
============

Regular installation using PIP
------------------------------

This package can be installed using PIP. The recommended pocedure is running:

.. code-block::

    pip install -u factiva-analytics

This will install and/or update the package to the latest official release.

Alternatively it can be installed directly from GitHub by running:

.. code-block::

    pip install git+https://github.com/dowjones/factiva-analytics-python.git@main

package guidelines establish that the ``main`` branch is also the latest official release.
However, this method allows to install pre-release versions in any of the available branches
of the repository like ``dev``.


Optional Packages
-----------------

The package automatically installs all prerequisites automatically. However, some custom
handlers for ``Streams`` and other processing components in the ``integration`` module may
require the installation of additional packages like Elasticsearch or Google Cloud BigQuery.

This is the list of optional packages. Installing them is recommended as long as these
components will be used within the solution.

* **elasticsearch**: Used in a Streams custom handler and bulk data import.

    .. code-block::

        pip install factiva-analytics[elasticsearch]

* **bigquery**: Used in a Streams custom handler and bulk data import.

    .. code-block::

        pip install factiva-analytics[bigquery]

* **MongoDB**: Used in a Stream custom handler and bulk data import.

    .. code-block::
    
        pip install factiva-analytics[mongodb]


* **MongoDB**: Used in a Stream custom handler and bulk data import.

    .. code-block::
    
        pip install factiva-analytics[mongodb]


Dev Environment
---------------

These packages are not required for production use.

* **dev**: Includes packages for testing and development. This code sample assumes the git repository is cloned and the command is executed from the root directory. It installs the library in editable mode along with the development dependencies.

    .. code-block::

        pip install -e .[dev]
