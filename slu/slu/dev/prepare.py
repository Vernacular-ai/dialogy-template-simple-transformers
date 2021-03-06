import json

import pandas as pd
from tqdm import tqdm

from dialogy.plugins.preprocess.text.normalize_utterance import normalize  # type: ignore

from slu import constants as const  # type: ignore
from slu.dev.io.reader.csv import read_multiclass_dataset_csv, map_labels_in_df, get_unique_labels  # type: ignore
from slu.dev.io.reader.sqlite import read_multiclass_dataset_sqlite  # type: ignore
from slu.dev.io.mp import parallel_proc  # type: ignore


def preprocess(df):
    texts = []
    labels = []
    data_id = []
    for _, row in tqdm(df.iterrows(), total=len(df)):
        label = row[const.LABELS]
        data = json.loads(row[const.DATA])
        try:
            alternatives = data[const.ALTERNATIVES]
            data = normalize(alternatives)
            texts.append(data)
            labels.append(label)
            data_id.append(row[const.DATA_ID])
        except KeyError:
            raise KeyError(
                "Your data doesn't match the expected format!"
                ' your data column should have {"alternatives": [[{"transcript": "..."}]]})'
                f" \ninstead looks like {data}"
            )
    return pd.DataFrame(
        {const.DATA_ID: data_id, const.TEXT: texts, const.LABELS: labels},
        columns=[const.DATA_ID, const.TEXT, const.LABELS],
    )


def read_multiclass_dataset(full_path, alias=None, file_format=const.CSV, **kwargs):
    if file_format == const.SQLITE:
        data_frame = read_multiclass_dataset_sqlite(full_path, **kwargs)
        return map_labels_in_df(data_frame, alias=alias)

    if file_format == const.CSV:
        return read_multiclass_dataset_csv(full_path, alias=alias, **kwargs)
    else:
        raise ValueError(
            "Expected format to be a string with"
            f" values in {const.V_SUPPORTED_DATA_FORMATS} but {file_format} was found."
        )


def prepare(data_file, alias, file_format=const.CSV, n_cores=const.N_DEFAULT_CORES):
    dataset = read_multiclass_dataset(
        data_file,
        alias,
        file_format=file_format,
        usecols=[const.DATA_ID, const.DATA, const.LABELS],
    )
    data_frame = parallel_proc(dataset, preprocess, return_df=True, n_cores=n_cores)
    labels = get_unique_labels(data_frame, const.LABELS)
    return data_frame, labels
