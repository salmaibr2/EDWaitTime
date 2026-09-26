"""
Loads the analytics dataframe from Cloud Storage once per app instance.

Place this file at appengine/data_loader.py, alongside app4.py (not
inside pages/). Reads the same BUCKET_NAME and EDA_CSV_BLOB env
variables already defined in app.yaml.
"""

import os
import tempfile
import pandas as pd
from google.cloud import storage

_df_cache = None


def get_dataframe():
    """Return the cached dataframe, downloading it from GCS on first call."""
    global _df_cache

    if _df_cache is not None:
        return _df_cache

    bucket_name = os.environ["BUCKET_NAME"]
    blob_name = os.environ["EDA_CSV_BLOB"]

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # tempfile.gettempdir() resolves to /tmp on App Engine (Linux) and
    # to the correct temp folder on Windows, so this works in both places
    local_path = os.path.join(tempfile.gettempdir(), "eda_df.csv")
    blob.download_to_filename(local_path)

    _df_cache = pd.read_csv(local_path)
    return _df_cache