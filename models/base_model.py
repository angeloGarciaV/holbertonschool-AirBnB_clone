#!/usr/bin/python3
"""
Module containing the BaseModel class
"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """
    The BaseModel class defines common attributes/methods for other classes.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of BaseModel.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f"))
                elif key != '__class__':
                    setattr(self, key, value)
            self.id = kwargs.get('id', str(uuid.uuid4()))
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the object.
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute updated_at with the current datetime.
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Returns a dictionary containing all
        keys/values of __dict__ of the instance.
        Includes a key __class__ with the class name of the object.
        created_at and updated_at 
        are converted to string objects in ISO format using isoformat().
        This method is the first piece of the
        serialization/deserialization process.
        """
        model_dict = self.__dict__.copy()
        model_dict['__class__'] = self.__class__.__name__
        model_dict['created_at'] = self.created_at.isoformat()
        model_dict['updated_at'] = self.updated_at.isoformat()
        return model_dict
