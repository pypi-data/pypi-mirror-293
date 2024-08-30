import base64
import hashlib
from refactor.common import Object
from refactor.utils.assets import AssetLoaderManager


class Asset(Object):
  """
  Base class of all inherited assets.
  """

  @property
  def src(self) -> any:
    return self._src
  
  @property
  def data(self) -> bytes:
    return self._data
  
  @property
  def hash(self) -> str:
    return hashlib.md5(self.data).hexdigest()
  
  @property
  def base64(self) -> str:
    return str(base64.b64encode(self.data))

  def __init__(self, src: any, *args, **kwargs) -> None:
    """
    Deserializable class constructor.
    :param args:    addition arguments.
    :param kwargs:  addition keyword arguments.
    """
    self._src = src
    self._data = AssetLoaderManager().load(src, *args, **kwargs)
