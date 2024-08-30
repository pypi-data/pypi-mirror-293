from io import BytesIO
import pandas as pd
from refactor.utils.assets import Asset


READERS = (
  pd.read_csv,
  pd.read_excel,
  pd.read_json,
  pd.read_xml,
  pd.read_sql,
  pd.read_stata,
  pd.read_sql_query,
  pd.read_sql_table,
  pd.read_spss,
  pd.read_html,
  pd.read_parquet,
  pd.read_hdf,
  pd.read_pickle,
  pd.read_gbq,
  pd.read_fwf,
  pd.read_orc,
  pd.read_feather,
  pd.read_sas,
  pd.read_table
)


class DataframeAsset(Asset):
  """
  This class load dataframe.
  """

  @property
  def dataframe(self) -> pd.DataFrame:
    return self._dataframe

  def __init__(self, src: any, *args, **kwargs) -> None:
    """
    Deserializable class constructor.
    :param args:    addition arguments.
    :param kwargs:  addition keyword arguments.
    """
    super().__init__(src, *args, **kwargs)
    bytes = BytesIO(self.data)
    for reader in READERS:
      try:
        self._dataframe = reader(bytes)
        break
      except:
        continue
    if self._dataframe is None:
      raise AssertionError('Cannot load dataframe: {src:20s}')
