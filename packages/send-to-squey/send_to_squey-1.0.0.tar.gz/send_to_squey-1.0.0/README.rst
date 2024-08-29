Connect and send a dataset
--------------------------

.. code-block:: python

    from squeylab import send_to_squey
    import pandas as pd

    squey = send_to_squey.connect(
        endpoint="3.222.243.61.aws.squeylab.com",
        auth=("squey", "p@$$w0rd!")
    )

    df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})

    squey.import_data(df, dataset_name="my_dataset")

.. note::
    `import_data <https://send-to-squey.doc.squeylab.com/#send_to_squey.SqueyInstance.import_data>`_ `data` parameter can be any object compatible with `pyarrow.record_batch`_ data parameter, or a path toward a parquet file.

.. _pyarrow.record_batch: https://arrow.apache.org/docs/python/generated/pyarrow.record_batch.html#pyarrow-record-batch

Start the instance
------------------

.. code-block:: python

    from squeylab import send_to_squey

    send_to_squey.start_instance(instance_id="i-0eb3fbba537abfa95")

.. note::
    Only supporting AWS for the moment. Needs a properly configured `credential file`_.

.. _credential file: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#guide-credentials