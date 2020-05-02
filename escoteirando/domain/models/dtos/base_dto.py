from datetime import date, datetime
from dateutil.parser import parse

from escoteirando.ext.logging import get_logger


class BaseDTO:

    LOG = get_logger()

    def __init__(self, from_dict: dict):
        if not isinstance(from_dict, dict):
            raise BaseDTOException(
                '{0}: ERROR - from_dict is invalid: {1}'.format(self.__class__,
                                                                from_dict))
        self.origin = from_dict

    def get(self, field_name: str, field_type):
        if field_name in self.origin:
            if field_type == date:
                return self._get_date(self.origin[field_name])
            elif field_type == datetime:
                return self._get_datetime(self.origin[field_name])
            else:
                try:
                    return field_type(self.origin[field_name])
                except Exception as exc:
                    self.LOG.exception('%s: ERROR - invalid parsing %s as %s: %s',
                                       self.__class__,
                                       self.origin[field_name],
                                       field_type,
                                       exc)

        else:
            self.LOG.error('%s: ERROR - field %s inexistent in %s',
                           self.__class__,
                           field_name,
                           self.origin)

        return None

    @classmethod
    def _get_date(cls, value) -> datetime:
        return cls._get_datetime(value).date

    @classmethod
    def _get_datetime(cls, value) -> datetime:
        try:
            return parse(value)
        except Exception as exc:
            cls.LOG.exception('%s: ERROR - DateTime parsing: %s',
                              cls,
                              exc)
        return datetime.min

    # "dataNascimento": "Tue Sep 13 2011 00: 00: 00 GMT+0000 (UTC)",
    # "dataValidade": "2020-01-01T00: 00: 00.000Z",


class BaseDTOException(Exception):
    pass
