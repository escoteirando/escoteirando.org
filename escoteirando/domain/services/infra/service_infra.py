from flask_sqlalchemy import SQLAlchemy

from escoteirando.domain.models.infra.params import Param
from datetime import datetime
from escoteirando.ext.logging import get_logger


class ServiceInfra:

    LOG = get_logger()

    def __init__(self, db: SQLAlchemy):
        self.DB: SQLAlchemy = db

    def get_param(self,
                  param_name: str,
                  user_id: int = 0,
                  default_value: str = None) -> str:
        user_id = max(0, user_id)
        param = Param()
        param = param.query.filter(Param.param_name ==
                                   param_name and Param.user_id == user_id).first()
        return default_value if param is None else param.param_value

    def set_param(self,
                  param_name: str,
                  value: str,
                  user_id: int = 0) -> bool:
        user_id = max(0, user_id)
        param = Param().query.filter(
            Param.param_name ==
            param_name and Param.user_id == user_id).first()
        if not param:
            param = Param()
            param.param_name = param_name
            param.user_id = user_id
            self.DB.session.add(param)

        param.param_value = value
        param.last_update = datetime.utcnow()
        self.LOG.info('set_param("%s","%s",%s)', param_name, value, user_id)
        return True
