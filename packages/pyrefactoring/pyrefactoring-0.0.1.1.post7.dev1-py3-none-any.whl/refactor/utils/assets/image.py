import rawpy
from PIL import Image
from io import BytesIO
from pillow_heif import register_heif_opener
from refactor.utils.assets import Asset

# support HEIC image format.
register_heif_opener()

class ImageAsset(Asset):
  """
  This class load image asset.
  """

  @property
  def image(self) -> Image.Image:
    return self._image

  def __init__(self, src: any, *args, **kwargs) -> None:
    """
    Deserializable class constructor.
    :param args:    addition arguments.
    :param kwargs:  addition keyword arguments.
    """
    super().__init__(src, *args, **kwargs)
    try:
      self._image = Image.open(self.data)
    except:
      pass
    try:
      with rawpy.imread(BytesIO(self.data)) as raw:
        thumb = raw.extract_thumb()
      if thumb.format == rawpy.ThumbFormat.JPEG:
        self._image = Image.open(BytesIO(thumb.data))
      elif thumb.format == rawpy.ThumbFormat.BITMAP:
        self._image = Image.fromarray(thumb.data)
    except:
      raise AssertionError(f'Cannot load image asset {src:20s}')
