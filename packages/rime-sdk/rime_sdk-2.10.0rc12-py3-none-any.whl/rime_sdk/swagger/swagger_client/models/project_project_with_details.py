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

class ProjectProjectWithDetails(object):
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
        'project': 'ProjectProject',
        'owner_details': 'ProjectOwnerDetails',
        'last_updated_time': 'datetime'
    }

    attribute_map = {
        'project': 'project',
        'owner_details': 'ownerDetails',
        'last_updated_time': 'lastUpdatedTime'
    }

    def __init__(self, project=None, owner_details=None, last_updated_time=None):  # noqa: E501
        """ProjectProjectWithDetails - a model defined in Swagger"""  # noqa: E501
        self._project = None
        self._owner_details = None
        self._last_updated_time = None
        self.discriminator = None
        if project is not None:
            self.project = project
        if owner_details is not None:
            self.owner_details = owner_details
        if last_updated_time is not None:
            self.last_updated_time = last_updated_time

    @property
    def project(self):
        """Gets the project of this ProjectProjectWithDetails.  # noqa: E501


        :return: The project of this ProjectProjectWithDetails.  # noqa: E501
        :rtype: ProjectProject
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this ProjectProjectWithDetails.


        :param project: The project of this ProjectProjectWithDetails.  # noqa: E501
        :type: ProjectProject
        """

        self._project = project

    @property
    def owner_details(self):
        """Gets the owner_details of this ProjectProjectWithDetails.  # noqa: E501


        :return: The owner_details of this ProjectProjectWithDetails.  # noqa: E501
        :rtype: ProjectOwnerDetails
        """
        return self._owner_details

    @owner_details.setter
    def owner_details(self, owner_details):
        """Sets the owner_details of this ProjectProjectWithDetails.


        :param owner_details: The owner_details of this ProjectProjectWithDetails.  # noqa: E501
        :type: ProjectOwnerDetails
        """

        self._owner_details = owner_details

    @property
    def last_updated_time(self):
        """Gets the last_updated_time of this ProjectProjectWithDetails.  # noqa: E501


        :return: The last_updated_time of this ProjectProjectWithDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, last_updated_time):
        """Sets the last_updated_time of this ProjectProjectWithDetails.


        :param last_updated_time: The last_updated_time of this ProjectProjectWithDetails.  # noqa: E501
        :type: datetime
        """

        self._last_updated_time = last_updated_time

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
        if issubclass(ProjectProjectWithDetails, dict):
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
        if not isinstance(other, ProjectProjectWithDetails):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
