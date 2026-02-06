from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """ 
    Базовая модель, содержащая в себе настройки, которые
    я хочу переиспользовать в других схемах:

    - from_attributes = True - позволяет мапить данные из объектов Beanie
    - populate_by_name = True - позволяет создавать модель, используя как 'id' так и '_id'
    """
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
