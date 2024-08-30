import base64
import urllib
from io import BytesIO
from pathlib import Path
from .base import AssetLoaderInterface
from .manager import AssetLoaderManager


class RawAssetLoader(AssetLoaderInterface):
  def _on_load(self, src: any, *args, **kwargs) -> bytes:
    kwargs['type'] = 'raw'
    return BytesIO(src)


class Base64AssetLoader(AssetLoaderInterface):
  def _on_load(self, src: any, *args, **kwargs) -> bytes:
    kwargs['type'] = 'base64'
    return base64.b64decode(src, validate=True)
  

class FileAssetLoader(AssetLoaderInterface):
  def _on_load(self, src: any, *args, **kwargs) -> bytes:
    kwargs['type'] = 'file'
    data = Path(src).expanduser().resolve().read_bytes()
    return data
  

class InternetAssetLoader(AssetLoaderInterface):
  def _on_load(self, src: any, *args, **kwargs) -> bytes:
    kwargs['type'] = 'internet resource'
    return urllib.request.urlopen(src).read()
  

AssetLoaderManager()\
.register(RawAssetLoader())\
.register(Base64AssetLoader())\
.register(FileAssetLoader())\
.register(InternetAssetLoader())