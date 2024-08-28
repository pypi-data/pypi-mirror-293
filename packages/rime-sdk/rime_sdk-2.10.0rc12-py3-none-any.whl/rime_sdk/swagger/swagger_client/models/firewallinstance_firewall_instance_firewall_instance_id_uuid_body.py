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

class FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody(object):
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
        'firewall_instance_id': 'object',
        'config': 'GenerativefirewallFirewallRuleConfig',
        'deployment_status': 'GenerativefirewallFirewallInstanceStatus',
        'description': 'str',
        'agent_id': 'RimeUUID',
        'spec': 'GenerativefirewallFirewallInstanceDeploymentConfig',
        'last_heartbeat_time': 'datetime'
    }

    attribute_map = {
        'firewall_instance_id': 'firewallInstanceId',
        'config': 'config',
        'deployment_status': 'deploymentStatus',
        'description': 'description',
        'agent_id': 'agentId',
        'spec': 'spec',
        'last_heartbeat_time': 'lastHeartbeatTime'
    }

    def __init__(self, firewall_instance_id=None, config=None, deployment_status=None, description=None, agent_id=None, spec=None, last_heartbeat_time=None):  # noqa: E501
        """FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody - a model defined in Swagger"""  # noqa: E501
        self._firewall_instance_id = None
        self._config = None
        self._deployment_status = None
        self._description = None
        self._agent_id = None
        self._spec = None
        self._last_heartbeat_time = None
        self.discriminator = None
        if firewall_instance_id is not None:
            self.firewall_instance_id = firewall_instance_id
        if config is not None:
            self.config = config
        if deployment_status is not None:
            self.deployment_status = deployment_status
        if description is not None:
            self.description = description
        if agent_id is not None:
            self.agent_id = agent_id
        if spec is not None:
            self.spec = spec
        if last_heartbeat_time is not None:
            self.last_heartbeat_time = last_heartbeat_time

    @property
    def firewall_instance_id(self):
        """Gets the firewall_instance_id of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501

        Unique ID of an object in RIME.  # noqa: E501

        :return: The firewall_instance_id of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :rtype: object
        """
        return self._firewall_instance_id

    @firewall_instance_id.setter
    def firewall_instance_id(self, firewall_instance_id):
        """Sets the firewall_instance_id of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.

        Unique ID of an object in RIME.  # noqa: E501

        :param firewall_instance_id: The firewall_instance_id of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :type: object
        """

        self._firewall_instance_id = firewall_instance_id

    @property
    def config(self):
        """Gets the config of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501


        :return: The config of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :rtype: GenerativefirewallFirewallRuleConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.


        :param config: The config of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :type: GenerativefirewallFirewallRuleConfig
        """

        self._config = config

    @property
    def deployment_status(self):
        """Gets the deployment_status of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501


        :return: The deployment_status of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :rtype: GenerativefirewallFirewallInstanceStatus
        """
        return self._deployment_status

    @deployment_status.setter
    def deployment_status(self, deployment_status):
        """Sets the deployment_status of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.


        :param deployment_status: The deployment_status of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :type: GenerativefirewallFirewallInstanceStatus
        """

        self._deployment_status = deployment_status

    @property
    def description(self):
        """Gets the description of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501

        Optional human-readable description of the firewall instance.  # noqa: E501

        :return: The description of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.

        Optional human-readable description of the firewall instance.  # noqa: E501

        :param description: The description of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def agent_id(self):
        """Gets the agent_id of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501


        :return: The agent_id of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._agent_id

    @agent_id.setter
    def agent_id(self, agent_id):
        """Sets the agent_id of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.


        :param agent_id: The agent_id of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :type: RimeUUID
        """

        self._agent_id = agent_id

    @property
    def spec(self):
        """Gets the spec of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501


        :return: The spec of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :rtype: GenerativefirewallFirewallInstanceDeploymentConfig
        """
        return self._spec

    @spec.setter
    def spec(self, spec):
        """Sets the spec of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.


        :param spec: The spec of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :type: GenerativefirewallFirewallInstanceDeploymentConfig
        """

        self._spec = spec

    @property
    def last_heartbeat_time(self):
        """Gets the last_heartbeat_time of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501

        Last time the control plan received a heartbeat from the firewall instance.  # noqa: E501

        :return: The last_heartbeat_time of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :rtype: datetime
        """
        return self._last_heartbeat_time

    @last_heartbeat_time.setter
    def last_heartbeat_time(self, last_heartbeat_time):
        """Sets the last_heartbeat_time of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.

        Last time the control plan received a heartbeat from the firewall instance.  # noqa: E501

        :param last_heartbeat_time: The last_heartbeat_time of this FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody.  # noqa: E501
        :type: datetime
        """

        self._last_heartbeat_time = last_heartbeat_time

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
        if issubclass(FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody, dict):
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
        if not isinstance(other, FirewallinstanceFirewallInstanceFirewallInstanceIdUuidBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
