from .base import AssetLoaderInterface


class AssetLoaderManager(AssetLoaderInterface):
  """
  This class manage all asset loaders.
  """

  def __init__(self, *args, **kwargs) -> None:
    """
    Deserializable class constructor.
    :param args:    addition arguments.
    :param kwargs:  addition keyword arguments.
    """
    super().__init__(*args, **kwargs)
    self._loaders = list()

  def register(self, loader: AssetLoaderInterface):
    """
    Register a new loader.
    :param loader:  loader to be registered.
    :return:        asset loader manager.
    """
    if loader not in self._loaders:
      self._loaders.append(loader)
    return self
  
  def unregister(self, loader: AssetLoaderInterface):
    """
    Unregister a new loader.
    :param loader:  loader to be unregistered.
    :return:        asset loader manager.
    """
    if loader in self._loaders:
      self._loaders.remove(loader)
    return self
  
  def _on_load(self, src: any, *args, **kwargs) -> bytes:
    """
    Asset loading process.
    :param src:     asset source.
    :param args:    additional arguments.
    :param kwargs:  additional keyword arguments.
    """
    for loader in self._loaders:
      try:
        data = loader.load(src, *args, **kwargs)
        return data
      except:
        continue
    raise AssertionError(f'Asset load error {src:20s}')
