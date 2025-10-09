Dow Jones Factiva Analytics Python Library
##########################################
.. image:: https://github.com/dowjones/factiva-analytics-python/actions/workflows/main_test_publish.yml/badge.svg
.. image:: https://readthedocs.org/projects/factiva-analytics-python/badge/?version=latest&style=plastic

This library simplifies the integration to Factiva Analytics API services that delivers premium news content.

The following services are currently implemented.

* **auth**: Contains tools to handle UserKey authentication and account statistics.
* **Snapshots**: Allows to run each snapshot creation, monitoring, download and local exploration, in an individual manner. Also allows to run the whole process within a single method.
* **Streams**: In addition to creating and getting stream details, contains the methods to easily implement a stream listener and push the content to other locations appropriate for high-available setups.
* **Taxonomy**: Operations that return taxonomies applied to classify news content.
* **ArticleFetcher**: Gets article's content by unique identifiers (AN), for display purposes only.

Installation
============
To install this library, run the following commands.

.. code-block::

    $ pip install --upgrade factiva-analytics

Using Library services
======================
Most Factiva Analytics services are implemented in this library. There may be a delay (commonly weeks) when new features are released and their operations are implemented in this package.

Getting Account Information
---------------------------
Create an `AccountInfo` instance that contains a summary of the account's basic information and usage statistics.

.. code-block:: python

    from factiva.analytics import AccountInfo
    u = AccountInfo(
        user_key='abcd1234abcd1234abcd1234abcd1234'  # Not needed if the ENV variable FACTIVA_USERKEY is set
    )
    print(u)

.. code-block::

    <'factiva.analytics.AccountInfo'>
    ├─user_key: <'factiva.analytics.UserKey'>
    │  ├─key: ****************************1234
    │  └─cloud_token: **********************YKB12sJrkHXX
    ├─account_name: AccName1234
    ├─account_type: account_with_contract_limits
    ├─active_product: DNA
    ├─max_allowed_extracted_documents: 8,000,000
    ├─max_allowed_extractions: 20
    ├─currently_running_extractions: 0
    ├─total_extracted_documents: 5,493,078
    ├─total_extractions: 4
    ├─total_stream_instances: 0
    ├─total_stream_subscriptions: 0
    ├─extractions_list: <NotLoaded>
    ├─streams_list: <NotLoaded>
    ├─enabled_company_identifiers:
    │  ├─[1]: sedol
    │  ├─[3]: cusip
    │  ├─[4]: isin
    │  └─[5]: ticker_exchange
    ├─remaining_documents: 2,506,922
    └─remaining_extractions: 16


Snapshot Explain
----------------
Creates an API request that tests the query and returns the number of matching items in the archive.

.. code-block:: python

    from factiva.analytics import SnapshotExplain
    my_query = "publication_datetime >= '2023-01-01 00:00:00' AND UPPER(source_code) = 'DJDN'"
    my_explain = SnapshotExplain(
        user_key='abcd1234abcd1234abcd1234abcd1234',  # Not needed if the ENV variable FACTIVA_USERKEY is set
        query=my_query)
    my_explain.process_job()  # This operation can take several seconds to complete
    print(my_explain)

.. code-block::

    <'factiva.analytics.SnapshotExplain'>
    ├─user_key: <'factiva.analytics.UserKey'>
    │  ├─key: ****************************1234
    │  └─cloud_token: **********************YKB12sJrkHXX
    ├─query: <'factiva.analytics.SnapshotExplainQuery'>
    │  ├─where: publication_datetime >= '2023-01-01 00:00:00' AND UPPER(source_code) = 'DJDN'
    │  ├─includes: <NotSet>
    │  ├─excludes: <NotSet>
    │  ├─include_lists: <NotSet>
    │  └─exclude_lists: <NotSet>
    ├─job_response: <'factiva.analytics.SnapshotExplainJobResponse'>
    │  ├─job_id: 3ee35a80-0406-4f2b-a999-3e4eb5aa94d8
    │  ├─job_link: https://api.dowjones...8/_explain
    │  ├─job_state: JOB_STATE_DONE
    │  ├─volume_estimate: 2,482,057
    │  └─errors: <NoErrors>
    └─samples: <NotRetrieved>


Snapshot Extraction
-------------------
Create a new snapshot and download to a local repository just require a few lines of code.

.. code-block:: python

    from factiva.analytics import SnapshotExtraction
    my_query = "publication_datetime >= '2023-01-01 00:00:00' AND UPPER(source_code) = 'DJDN'"
    my_snapshot = SnapshotExtraction(
        user_key='abcd1234abcd1234abcd1234abcd1234',  # Can be ommited if exist as env variable
        query=my_query)
    my_snapshot.process_job()  # This operation can take several minutes to complete

After the process completes, the output files are stored in a subfolder named as the Extraction Job ID.

In the previous code a new snapshot is created using my_query as selection criteria and user_key for user authentication. After the job is being validated internally, a Snapshot Id is obtained along with the list of files to download. Files are automatically downloaded to a folder named equal to the snapshot ID, and contents are loaded as a Pandas DataFrame to the variable news_articles. This process may take several minutes, but automates the extraction process significantly.


