from abc import abstractmethod
from refactor.common import Object
from refactor.design import Singleton


class AssetLoaderInterface(Object, metaclass=Singleton):
  """
  Interface class of all inherited asset loaders.
  """
  
  def load(self, src: any, *args, **kwargs) -> bytes:
    """
    Load asset from source.
    :param src:     asset source.
    :param args:    additional arguments.
    :param kwargs:  additional keyword arguments.
    """
    try:
      data = self._on_load(src, *args, **kwargs)
      self._on_success(src, data, *args, **kwargs)
      return data
    except Exception as e:
      self._on_failed(src, *args, **kwargs)
      raise e
  
  @abstractmethod
  def _on_load(self, src: any, *args, **kwargs) -> bytes:
    """
    Asset loading process.
    :param src:     asset source.
    :param args:    additional arguments.
    :param kwargs:  additional keyword arguments.
    """
    raise NotImplementedError

  def _on_success(self, src: any, data: any, *args, **kwargs):
    """
    Asset was loaded successfully.
    :param src:     asset source.
    :param data:    loaded data.
    :param args:    additional arguments.
    :param kwargs:  additional keyword arguments.
    """
    pass
  
  def _on_failed(self, src: any, *args, **kwargs):
    """
    Asset was loaded unsucessfully.
    :param src:     asset source.
    :param args:    additional arguments.
    :param kwargs:  additional keyword arguments.
    """
    pass
