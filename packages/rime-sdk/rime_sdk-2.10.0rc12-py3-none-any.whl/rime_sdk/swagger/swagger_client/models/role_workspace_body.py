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

class RoleWorkspaceBody(object):
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
        'project_id': 'object',
        'role_pairs': 'list[RimeParentRoleSubjectRolePair]'
    }

    attribute_map = {
        'project_id': 'projectId',
        'role_pairs': 'rolePairs'
    }

    def __init__(self, project_id=None, role_pairs=None):  # noqa: E501
        """RoleWorkspaceBody - a model defined in Swagger"""  # noqa: E501
        self._project_id = None
        self._role_pairs = None
        self.discriminator = None
        if project_id is not None:
            self.project_id = project_id
        self.role_pairs = role_pairs

    @property
    def project_id(self):
        """Gets the project_id of this RoleWorkspaceBody.  # noqa: E501

        Uniquely specifies a Project.  # noqa: E501

        :return: The project_id of this RoleWorkspaceBody.  # noqa: E501
        :rtype: object
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this RoleWorkspaceBody.

        Uniquely specifies a Project.  # noqa: E501

        :param project_id: The project_id of this RoleWorkspaceBody.  # noqa: E501
        :type: object
        """

        self._project_id = project_id

    @property
    def role_pairs(self):
        """Gets the role_pairs of this RoleWorkspaceBody.  # noqa: E501

        The elements of role_pairs maps each Workspace role to a Project role. For example, you can specify that a user with admin rights on a Workspace will get viewer rights on Projects in that Workspace.  # noqa: E501

        :return: The role_pairs of this RoleWorkspaceBody.  # noqa: E501
        :rtype: list[RimeParentRoleSubjectRolePair]
        """
        return self._role_pairs

    @role_pairs.setter
    def role_pairs(self, role_pairs):
        """Sets the role_pairs of this RoleWorkspaceBody.

        The elements of role_pairs maps each Workspace role to a Project role. For example, you can specify that a user with admin rights on a Workspace will get viewer rights on Projects in that Workspace.  # noqa: E501

        :param role_pairs: The role_pairs of this RoleWorkspaceBody.  # noqa: E501
        :type: list[RimeParentRoleSubjectRolePair]
        """
        if role_pairs is None:
            raise ValueError("Invalid value for `role_pairs`, must not be `None`")  # noqa: E501

        self._role_pairs = role_pairs

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
        if issubclass(RoleWorkspaceBody, dict):
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
        if not isinstance(other, RoleWorkspaceBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
