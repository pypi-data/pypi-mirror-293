import copy
import datetime
from enum import StrEnum, auto
import json
import time

import pyarrow as pa
import pyarrow.flight as fl
import pyarrow.parquet as pq

from pip._vendor.rich.progress import Progress

import sys
if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

instance_started = False

class CloudProvider(StrEnum):
    AWS = auto()

class CloudInstance:
    cloud_provider = None
    instance_id = None
    profile_name = None
    region_name = None

    def __init__(self, cloud_provider, instance_id, profile_name, region_name):
        self.cloud_provider = cloud_provider
        self.instance_id = instance_id
        self.profile_name = profile_name
        self.region_name = region_name

class SqueyInstance:
    """
    """
    endpoint = None
    auth = None
    instance_id = None

    client = None
    options = None

    def __init__(self, endpoint, auth, disable_server_verification, compression_codec):
        self.endpoint = endpoint
        self.auth = auth
        self.client = None
        self.compression_codec = compression_codec
        self.version = metadata.version('send-to-squey')

        connect = lambda e, v : fl.connect(f"grpc+tls://{e}:5005", disable_server_verification=v)

        # Wait for Apache Arrow Flight service to be up and running
        if instance_started:
            bar = Progress()
            id = bar.add_task(description=f"Waiting for Squey service  to start", total=None)
            bar.start()

            while True:
                try:
                    self.client = connect(endpoint, disable_server_verification)
                    try:
                        list(self.client.list_flights())
                    except fl.FlightUnauthenticatedError as e:
                        break
                except fl.FlightUnavailableError as e:
                    time.sleep(10)
            
            bar.stop()
        else:
            self.client = connect(endpoint, disable_server_verification)

        # Authenticate against Apache Arrow Flight server
        token_pair = self.client.authenticate_basic_token(auth[0], auth[1])
        self.options = pa.flight.FlightCallOptions(
            headers=[token_pair],
            write_options=pa.ipc.IpcWriteOptions(compression=compression_codec)
        )

    def import_data(self, data, dataset_name=None):
        """
        Uploads a dataset to the cloud Squey instance and imports it.

        :param data: any object compatible with pyarrow.record_batch data parameter \
        (see https://arrow.apache.org/docs/python/generated/pyarrow.record_batch.html#pyarrow-record-batch) \
        or the path toward a parquet file.
        :param dataset_name: the name of the dataset that will be displayed in Squey.
        :type dataset_name: string
        """
        if dataset_name == None:
            dataset_name=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if isinstance(data, str):
            data = pq.ParquetFile(data)
            num_rows = data.metadata.num_rows
        else:
            num_rows = len(data)

        batch_size = max(int(num_rows / 100), 100)

        if isinstance(data, pq.ParquetFile):
            progress_total = num_rows
            record_batches = self._ParquetBatchReader(data, batch_size)
        elif hasattr(data, "iloc"):
            progress_total = num_rows
            split_func = lambda data, start, end : data.iloc[start:end]
            record_batches = self._IndexBasedBatchReader(data, batch_size, split_func)
        else:
            progress_total = None
            split_func = lambda data, start, end : data
            record_batches = self._IndexBasedBatchReader(data, num_rows, split_func)

        bar = Progress()
        description=f"Uploading '{dataset_name}' to Squey remote instance ({self.endpoint})"
        id = bar.add_task(description, total=progress_total)
        bar.start()

        descriptor_info = {
            "path": f"{dataset_name}.parquet",
            "compression": self.compression_codec,
            "version": self.version
        }
        descriptor = fl.FlightDescriptor.for_command(json.dumps(descriptor_info))
        
        writer = None
        init = False
        for record_batch in record_batches:
            if not init:
                writer, _ = self.client.do_put(
                    descriptor,
                    record_batch.schema,
                    options=self.options
                )
                init = True
            writer.write_batch(record_batch)
            bar.advance(id, record_batch.num_rows)

        bar.stop()

    class _DataBatchReader:
        def __init__(self, data_source, batch_size):
            self.data_source = data_source
            self.batch_size = batch_size

        def __iter__(self):
            return self

        def __next__(self):
            raise NotImplementedError("__next__ method not implemented.")

    class _IndexBasedBatchReader(_DataBatchReader):
        def __init__(self, data_source, batch_size, split_func):
            super().__init__(data_source, batch_size)
            self.num_rows = len(data_source)
            self.split_func = split_func
            self.current_index = 0

        def __next__(self):
            if self.current_index >= self.num_rows:
                raise StopIteration
            start = self.current_index
            self.current_index = end = min(start + self.batch_size, self.num_rows)
            batch = self.split_func(self.data_source, start, end)
            return pa.record_batch(batch)

    class _ParquetBatchReader(_DataBatchReader):
        def __init__(self, data_source, batch_size):
            super().__init__(data_source, batch_size)
            self.parquet_file = data_source
            self.batch_iterator = self.parquet_file.iter_batches(batch_size=batch_size)

        def __next__(self):
            batch = next(self.batch_iterator)
            return batch

def start_instance(
    instance_id,
    cloud_provider=CloudProvider.AWS,
    profile_name=None,
    region_name=None
    ):
    """
    Start a cloud instance.

    :param instance_id: the id of the instance
    :type instance_id: string
    :param cloud_provider: a value of the CloudProvider enum
    :type profile_name: enum
    :param profile_name: the profile name
    :type profile_name: string
    :param region_name: the region code
    :type region_name: string
    """
    provider_module = importlib.import_module("squeylab.cloud_providers." + cloud_provider)

    if not provider_module.is_instance_running(instance_id, profile_name, region_name):
        bar = Progress()
        id = bar.add_task(description=f"Waiting for Squey instance to start", total=None)
        bar.start()

        global instance_started
        instance_started = True
        provider_module.start_instance(instance_id, profile_name, region_name)

        bar.stop()

def connect(endpoint, auth, disable_server_verification=False, compression_codec="lz4"):
    """
    Connect to Squey server and returns a :class:`SqueyInstance` object.

    :param endpoint: the connection endpoint.
    :type endpoint: string
    :param auth: a tuple composed of username and password.
    :type auth: (string, string)
    :param port: the apache arrow flight server port.
    :type port: int
    :param disable_server_verification: disable SSL server verification.
    :type disable_server_verification: bool
    :param compression_codec: compression codec used ("lz4", "zstd" or None; defaults to "lz4")
    :type compression_codec: string
    :return: a :class:`SqueyInstance` object
    """
    return SqueyInstance(endpoint, auth, disable_server_verification, compression_codec)
