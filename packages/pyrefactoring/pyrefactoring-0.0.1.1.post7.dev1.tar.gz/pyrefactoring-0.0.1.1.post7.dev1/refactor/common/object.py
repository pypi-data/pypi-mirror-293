from refactor.utils import logging


class Object:
  """
  Base object of almost entities in the library.
  """

  @property
  def classname(self) -> str:
    return self.__class__.__name__
  
  @property
  def modulename(self) -> str:
    return self.__module__

  @property
  def logger(self) -> logging.Logger:
    return self.__logger

  def __init__(self, *args, **kwargs) -> None:
    """
    Deserializable class constructor.
    :param args:    addition arguments.
    :param kwargs:  addition keyword arguments.
    """
    self.__logger = logging.getLogger(f'{__name__}.{self.classname}')

  def brief(self) -> dict:
    """
    Get object data as a dict.
    :return:  data dict.
    """
    return {'classname': self.classname, 'module': self.modulename}

  def checksum(self, hash: str) -> bool:
    """
    Checksum MD5.
    :param hash:  hash to be checked.
    :return:      true or false.
    """
    return self.hash == hash
