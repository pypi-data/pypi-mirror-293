# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `X-Firewall-Auth-Token` for all the firewall methods and `rime-api-key` for all other methods.  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: dev@robustintelligence.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class RuntimeinfoCustomImageType(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'custom_image': 'RuntimeinfoCustomImage',
        'managed_image_name': 'str'
    }

    attribute_map = {
        'custom_image': 'customImage',
        'managed_image_name': 'managedImageName'
    }

    def __init__(self, custom_image=None, managed_image_name=None):  # noqa: E501
        """RuntimeinfoCustomImageType - a model defined in Swagger"""  # noqa: E501
        self._custom_image = None
        self._managed_image_name = None
        self.discriminator = None
        if custom_image is not None:
            self.custom_image = custom_image
        if managed_image_name is not None:
            self.managed_image_name = managed_image_name

    @property
    def custom_image(self):
        """Gets the custom_image of this RuntimeinfoCustomImageType.  # noqa: E501


        :return: The custom_image of this RuntimeinfoCustomImageType.  # noqa: E501
        :rtype: RuntimeinfoCustomImage
        """
        return self._custom_image

    @custom_image.setter
    def custom_image(self, custom_image):
        """Sets the custom_image of this RuntimeinfoCustomImageType.


        :param custom_image: The custom_image of this RuntimeinfoCustomImageType.  # noqa: E501
        :type: RuntimeinfoCustomImage
        """

        self._custom_image = custom_image

    @property
    def managed_image_name(self):
        """Gets the managed_image_name of this RuntimeinfoCustomImageType.  # noqa: E501

        Name of the RI managed image.  # noqa: E501

        :return: The managed_image_name of this RuntimeinfoCustomImageType.  # noqa: E501
        :rtype: str
        """
        return self._managed_image_name

    @managed_image_name.setter
    def managed_image_name(self, managed_image_name):
        """Sets the managed_image_name of this RuntimeinfoCustomImageType.

        Name of the RI managed image.  # noqa: E501

        :param managed_image_name: The managed_image_name of this RuntimeinfoCustomImageType.  # noqa: E501
        :type: str
        """

        self._managed_image_name = managed_image_name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(RuntimeinfoCustomImageType, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RuntimeinfoCustomImageType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
