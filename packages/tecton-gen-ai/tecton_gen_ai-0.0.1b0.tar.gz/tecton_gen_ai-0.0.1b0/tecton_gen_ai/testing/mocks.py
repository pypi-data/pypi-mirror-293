from datetime import timedelta
from typing import Any, Dict, List, Optional, Union

import pandas as pd
import pyarrow as pa
from tecton import (
    BatchFeatureView,
    BatchSource,
    Entity,
    RealtimeFeatureView,
    RequestSource,
    batch_feature_view,
    pandas_batch_config,
    realtime_feature_view,
)
from tecton.types import Field

from ..core_utils import get_df_schema

_MAX_ROWS = 100


def mock_source(name: str, df: pd.DataFrame, **source_kwargs: Any) -> BatchSource:

    if len(df) > _MAX_ROWS:
        raise ValueError(f"Dataframe has more than {_MAX_ROWS} rows")

    data = df.to_dict("records")
    pa.Table.from_pandas(df).schema

    @pandas_batch_config()
    def api_df():
        return pd.DataFrame(data)

    return BatchSource(name=name, batch_config=api_df, **source_kwargs)


def mock_batch_feature_view(
    name: str,
    data: Union[pd.DataFrame, Dict[str, Any]],
    entity_keys: List[str],
    timestamp_field: Optional[str] = None,
    **fv_kwargs: Any,
) -> BatchFeatureView:
    df = data if isinstance(data, pd.DataFrame) else pd.DataFrame([data])
    if timestamp_field is None:
        timestamp_field = "_tecton_auto_ts"
        df = df.assign(**{timestamp_field: "2024-01-01"})
    df = df.assign(**{timestamp_field: pd.to_datetime(df[timestamp_field])})

    source = mock_source(name + "_source", df)
    schema = get_df_schema(df, as_attributes=True)
    join_keys = [Field(x.name, x.dtype) for x in schema if x.name in entity_keys]
    if len(join_keys) != len(entity_keys):
        raise ValueError(f"Entity keys {entity_keys} not all found in schema {schema}")
    entity = Entity(name=name + "_entity", join_keys=join_keys)
    features = [
        x for x in schema if x.name not in entity_keys and x.name != timestamp_field
    ]

    base_args = dict(
        name=name,
        sources=[source],
        entities=[entity],
        mode="pandas",
        online=True,
        offline=True,
        features=features,
        feature_start_time=df[timestamp_field].min().to_pydatetime(),
        batch_schedule=timedelta(days=1),
        timestamp_field=timestamp_field,
        environment="tecton-rift-core-0.9.0",
    )
    base_args.update(fv_kwargs)

    @batch_feature_view(**base_args)
    def dummy(_df):
        return _df

    return dummy


def mock_realtime_feature_view(
    name: str,
    data: Union[pd.DataFrame, Dict[str, Any]],
    keys: List[str],
    **fv_kwargs: Any,
) -> RealtimeFeatureView:
    df = data if isinstance(data, pd.DataFrame) else pd.DataFrame([data])
    request_source = RequestSource(schema=get_df_schema(df[keys]))
    features = get_df_schema(df, as_attributes=True)

    base_args = dict(
        name=name, sources=[request_source], mode="pandas", features=features
    )
    base_args.update(fv_kwargs)

    @realtime_feature_view(**base_args)
    def dummy(request):
        return pd.merge(request, df, on=keys, how="inner").head(1)

    return dummy
