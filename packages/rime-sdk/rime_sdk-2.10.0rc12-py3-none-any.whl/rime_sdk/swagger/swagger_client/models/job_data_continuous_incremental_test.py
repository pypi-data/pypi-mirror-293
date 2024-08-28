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

class JobDataContinuousIncrementalTest(object):
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
        'firewall_id': 'str',
        'ct_test_run_ids': 'list[str]',
        'progress': 'RimeContinuousTestJobProgress'
    }

    attribute_map = {
        'firewall_id': 'firewallId',
        'ct_test_run_ids': 'ctTestRunIds',
        'progress': 'progress'
    }

    def __init__(self, firewall_id=None, ct_test_run_ids=None, progress=None):  # noqa: E501
        """JobDataContinuousIncrementalTest - a model defined in Swagger"""  # noqa: E501
        self._firewall_id = None
        self._ct_test_run_ids = None
        self._progress = None
        self.discriminator = None
        if firewall_id is not None:
            self.firewall_id = firewall_id
        if ct_test_run_ids is not None:
            self.ct_test_run_ids = ct_test_run_ids
        if progress is not None:
            self.progress = progress

    @property
    def firewall_id(self):
        """Gets the firewall_id of this JobDataContinuousIncrementalTest.  # noqa: E501


        :return: The firewall_id of this JobDataContinuousIncrementalTest.  # noqa: E501
        :rtype: str
        """
        return self._firewall_id

    @firewall_id.setter
    def firewall_id(self, firewall_id):
        """Sets the firewall_id of this JobDataContinuousIncrementalTest.


        :param firewall_id: The firewall_id of this JobDataContinuousIncrementalTest.  # noqa: E501
        :type: str
        """

        self._firewall_id = firewall_id

    @property
    def ct_test_run_ids(self):
        """Gets the ct_test_run_ids of this JobDataContinuousIncrementalTest.  # noqa: E501


        :return: The ct_test_run_ids of this JobDataContinuousIncrementalTest.  # noqa: E501
        :rtype: list[str]
        """
        return self._ct_test_run_ids

    @ct_test_run_ids.setter
    def ct_test_run_ids(self, ct_test_run_ids):
        """Sets the ct_test_run_ids of this JobDataContinuousIncrementalTest.


        :param ct_test_run_ids: The ct_test_run_ids of this JobDataContinuousIncrementalTest.  # noqa: E501
        :type: list[str]
        """

        self._ct_test_run_ids = ct_test_run_ids

    @property
    def progress(self):
        """Gets the progress of this JobDataContinuousIncrementalTest.  # noqa: E501


        :return: The progress of this JobDataContinuousIncrementalTest.  # noqa: E501
        :rtype: RimeContinuousTestJobProgress
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """Sets the progress of this JobDataContinuousIncrementalTest.


        :param progress: The progress of this JobDataContinuousIncrementalTest.  # noqa: E501
        :type: RimeContinuousTestJobProgress
        """

        self._progress = progress

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
        if issubclass(JobDataContinuousIncrementalTest, dict):
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
        if not isinstance(other, JobDataContinuousIncrementalTest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
