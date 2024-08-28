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

class RimeWorkspaceWriteMask(object):
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
        'name': 'bool',
        'agent_ids': 'bool',
        'default_agent_id': 'bool',
        'description': 'bool',
        'results_retention_in_days': 'bool'
    }

    attribute_map = {
        'name': 'name',
        'agent_ids': 'agentIds',
        'default_agent_id': 'defaultAgentId',
        'description': 'description',
        'results_retention_in_days': 'resultsRetentionInDays'
    }

    def __init__(self, name=None, agent_ids=None, default_agent_id=None, description=None, results_retention_in_days=None):  # noqa: E501
        """RimeWorkspaceWriteMask - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._agent_ids = None
        self._default_agent_id = None
        self._description = None
        self._results_retention_in_days = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if agent_ids is not None:
            self.agent_ids = agent_ids
        if default_agent_id is not None:
            self.default_agent_id = default_agent_id
        if description is not None:
            self.description = description
        if results_retention_in_days is not None:
            self.results_retention_in_days = results_retention_in_days

    @property
    def name(self):
        """Gets the name of this RimeWorkspaceWriteMask.  # noqa: E501

        Specifies whether to update name.  # noqa: E501

        :return: The name of this RimeWorkspaceWriteMask.  # noqa: E501
        :rtype: bool
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this RimeWorkspaceWriteMask.

        Specifies whether to update name.  # noqa: E501

        :param name: The name of this RimeWorkspaceWriteMask.  # noqa: E501
        :type: bool
        """

        self._name = name

    @property
    def agent_ids(self):
        """Gets the agent_ids of this RimeWorkspaceWriteMask.  # noqa: E501

        Specifies whether to update list of Agent IDs.  # noqa: E501

        :return: The agent_ids of this RimeWorkspaceWriteMask.  # noqa: E501
        :rtype: bool
        """
        return self._agent_ids

    @agent_ids.setter
    def agent_ids(self, agent_ids):
        """Sets the agent_ids of this RimeWorkspaceWriteMask.

        Specifies whether to update list of Agent IDs.  # noqa: E501

        :param agent_ids: The agent_ids of this RimeWorkspaceWriteMask.  # noqa: E501
        :type: bool
        """

        self._agent_ids = agent_ids

    @property
    def default_agent_id(self):
        """Gets the default_agent_id of this RimeWorkspaceWriteMask.  # noqa: E501

        Specifies whether to update default Agent ID.  # noqa: E501

        :return: The default_agent_id of this RimeWorkspaceWriteMask.  # noqa: E501
        :rtype: bool
        """
        return self._default_agent_id

    @default_agent_id.setter
    def default_agent_id(self, default_agent_id):
        """Sets the default_agent_id of this RimeWorkspaceWriteMask.

        Specifies whether to update default Agent ID.  # noqa: E501

        :param default_agent_id: The default_agent_id of this RimeWorkspaceWriteMask.  # noqa: E501
        :type: bool
        """

        self._default_agent_id = default_agent_id

    @property
    def description(self):
        """Gets the description of this RimeWorkspaceWriteMask.  # noqa: E501

        Specifies whether to update description.  # noqa: E501

        :return: The description of this RimeWorkspaceWriteMask.  # noqa: E501
        :rtype: bool
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this RimeWorkspaceWriteMask.

        Specifies whether to update description.  # noqa: E501

        :param description: The description of this RimeWorkspaceWriteMask.  # noqa: E501
        :type: bool
        """

        self._description = description

    @property
    def results_retention_in_days(self):
        """Gets the results_retention_in_days of this RimeWorkspaceWriteMask.  # noqa: E501

        Specifies whether to results retention in days.  # noqa: E501

        :return: The results_retention_in_days of this RimeWorkspaceWriteMask.  # noqa: E501
        :rtype: bool
        """
        return self._results_retention_in_days

    @results_retention_in_days.setter
    def results_retention_in_days(self, results_retention_in_days):
        """Sets the results_retention_in_days of this RimeWorkspaceWriteMask.

        Specifies whether to results retention in days.  # noqa: E501

        :param results_retention_in_days: The results_retention_in_days of this RimeWorkspaceWriteMask.  # noqa: E501
        :type: bool
        """

        self._results_retention_in_days = results_retention_in_days

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
        if issubclass(RimeWorkspaceWriteMask, dict):
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
        if not isinstance(other, RimeWorkspaceWriteMask):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
