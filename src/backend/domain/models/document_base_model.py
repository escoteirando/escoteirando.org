class DocumentBaseModel:

    def validate_dict(self, dict_value: dict, fields: list) -> bool:
        """
        Validate if a dict has the fields
        """
        if isinstance(dict_value, dict) and isinstance(fields, list):
            for field in fields:
                if field not in dict_value or not hasattr(self, field):
                    return False

            return True
        return False

    def from_dict(self, dict_value: dict, fields: list) -> DocumentBaseModel:
        for k, v in dict_value:
            setattr(self, k, v)
        self._after_from_dict()
        return self

    def _after_from_dict(self):
        pass
