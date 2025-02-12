Volume Estimates
================

Accurate volume estimates are based on the Snapshot Explain operation. This
operation returns the exact number of matching articles in the archive.

.. code-block:: python

    from factiva.analytics import SnapshotExplain
    where_str = "publication_datetime >= '2020-01-01' AND language_code = 'en' AND REGEXP_CONTAINS(industry_codes, r'(?i)(^|,)(i1|i25121|i2567)($|,)')"
    se = SnapshotExplain(query=where_str)
    se.process_job()
    print(f"The query matches {se.job_results.volume_estimate} articles")


.. code-block::

    The query matches 123456 articles

Using the same Snapshot Explain object, you can also get metadata samples.

.. code-block:: python

    se.get_samples()
    print(se.samples.data[['word_count', 'title', 'source_code']])

The object ``se.samples.data`` is a pandas DataFrame.

.. code-block:: 

        word_count                                              title source_code
    0          110   Maire Tecnimont shares gain after India contract    SOLRADIN
    1          147  Poste Italiane begins offering electricity, ga...    SOLRADIN
    2          219  Constellation Energy inks PPA with Microsoft f...    SOLRADIN
    3           25  EDF now sees Hinkley Point C IRR 7.1-7.2% vs 7...    SOLRADIN
    4          131        Derivatives stock options: summary by title    SOLRADIN
    ..         ...                                                ...         ...
    95         775  Atlantic Power and Infrastructure Installs Tre...      ACWIRE
    96         249  Quebec Precious Metals Corporation Announces R...      ACWIRE
    97         503  Shareholders that lost money on Plug Power Inc...      ACWIRE
    98        1572  Tenth Avenue Petroleum Announces Third Quarter...      ACWIRE
    99         187  Challenging Ourselves To Lead in Sustainable E...      ACWIRE

When volume estimates are in line with your expectations, you can proceed to analyze
the data using the Snapshot TimeSeries operation, or directly extract the content via
the Snapshot Extract operation.