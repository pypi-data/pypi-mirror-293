import base64
import urllib
from io import BytesIO
from pathlib import Path
from .base import AssetLoaderInterface
from .manager import AssetLoaderManager


class RawAssetLoader(AssetLoaderInterface):
  def _on_load(self, src: any, *args, **kwargs) -> bytes:
    return BytesIO(src).read()


class Base64AssetLoader(AssetLoaderInterface):
  def _on_load(self, src: any, *args, **kwargs) -> bytes:
    return base64.b64decode(src, validate=True)
  

class FileAssetLoader(AssetLoaderInterface):
  def _on_load(self, src: any, *args, **kwargs) -> bytes:
    data = Path(src).expanduser().resolve().read_bytes()
    return data
  

class InternetAssetLoader(AssetLoaderInterface):
  def _on_load(self, src: any, *args, **kwargs) -> bytes:
    return urllib.request.urlopen(src).read()
  

AssetLoaderManager()\
.register(RawAssetLoader())\
.register(Base64AssetLoader())\
.register(FileAssetLoader())\
.register(InternetAssetLoader())