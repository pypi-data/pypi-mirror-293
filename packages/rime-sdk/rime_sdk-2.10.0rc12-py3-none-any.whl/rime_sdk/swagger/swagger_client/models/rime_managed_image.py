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

class RimeManagedImage(object):
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
        'name': 'str',
        'base_image': 'RimeImageReference',
        'role_type': 'ManagedImageRoleType',
        'child_images': 'list[RimeImageReference]',
        'rime_tag': 'str',
        'repo_uri': 'str',
        'status': 'RimeManagedImageStatus',
        'package_requirements': 'list[ManagedImagePackageRequirement]',
        'pip_requirements': 'list[ManagedImagePipRequirement]',
        'pip_libraries': 'list[ManagedImagePipLibrary]',
        'python_version': 'str'
    }

    attribute_map = {
        'name': 'name',
        'base_image': 'baseImage',
        'role_type': 'roleType',
        'child_images': 'childImages',
        'rime_tag': 'rimeTag',
        'repo_uri': 'repoUri',
        'status': 'status',
        'package_requirements': 'packageRequirements',
        'pip_requirements': 'pipRequirements',
        'pip_libraries': 'pipLibraries',
        'python_version': 'pythonVersion'
    }

    def __init__(self, name=None, base_image=None, role_type=None, child_images=None, rime_tag=None, repo_uri=None, status=None, package_requirements=None, pip_requirements=None, pip_libraries=None, python_version=None):  # noqa: E501
        """RimeManagedImage - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._base_image = None
        self._role_type = None
        self._child_images = None
        self._rime_tag = None
        self._repo_uri = None
        self._status = None
        self._package_requirements = None
        self._pip_requirements = None
        self._pip_libraries = None
        self._python_version = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if base_image is not None:
            self.base_image = base_image
        if role_type is not None:
            self.role_type = role_type
        if child_images is not None:
            self.child_images = child_images
        if rime_tag is not None:
            self.rime_tag = rime_tag
        if repo_uri is not None:
            self.repo_uri = repo_uri
        if status is not None:
            self.status = status
        if package_requirements is not None:
            self.package_requirements = package_requirements
        if pip_requirements is not None:
            self.pip_requirements = pip_requirements
        if pip_libraries is not None:
            self.pip_libraries = pip_libraries
        if python_version is not None:
            self.python_version = python_version

    @property
    def name(self):
        """Gets the name of this RimeManagedImage.  # noqa: E501

        The external name of the image. This name must match the /^[a-z][a-z0-9]*(?:[_-][a-z0-9]+)*$/ regular expression. See the naming rules in https://docs.docker.com/engine/reference/commandline/tag/#extended-description https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html from which the naming convention derives. The above names are valid ECR or Docker image names.  # noqa: E501

        :return: The name of this RimeManagedImage.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this RimeManagedImage.

        The external name of the image. This name must match the /^[a-z][a-z0-9]*(?:[_-][a-z0-9]+)*$/ regular expression. See the naming rules in https://docs.docker.com/engine/reference/commandline/tag/#extended-description https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html from which the naming convention derives. The above names are valid ECR or Docker image names.  # noqa: E501

        :param name: The name of this RimeManagedImage.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def base_image(self):
        """Gets the base_image of this RimeManagedImage.  # noqa: E501


        :return: The base_image of this RimeManagedImage.  # noqa: E501
        :rtype: RimeImageReference
        """
        return self._base_image

    @base_image.setter
    def base_image(self, base_image):
        """Sets the base_image of this RimeManagedImage.


        :param base_image: The base_image of this RimeManagedImage.  # noqa: E501
        :type: RimeImageReference
        """

        self._base_image = base_image

    @property
    def role_type(self):
        """Gets the role_type of this RimeManagedImage.  # noqa: E501


        :return: The role_type of this RimeManagedImage.  # noqa: E501
        :rtype: ManagedImageRoleType
        """
        return self._role_type

    @role_type.setter
    def role_type(self, role_type):
        """Sets the role_type of this RimeManagedImage.


        :param role_type: The role_type of this RimeManagedImage.  # noqa: E501
        :type: ManagedImageRoleType
        """

        self._role_type = role_type

    @property
    def child_images(self):
        """Gets the child_images of this RimeManagedImage.  # noqa: E501

        The set of images that use this image as a source.  # noqa: E501

        :return: The child_images of this RimeManagedImage.  # noqa: E501
        :rtype: list[RimeImageReference]
        """
        return self._child_images

    @child_images.setter
    def child_images(self, child_images):
        """Sets the child_images of this RimeManagedImage.

        The set of images that use this image as a source.  # noqa: E501

        :param child_images: The child_images of this RimeManagedImage.  # noqa: E501
        :type: list[RimeImageReference]
        """

        self._child_images = child_images

    @property
    def rime_tag(self):
        """Gets the rime_tag of this RimeManagedImage.  # noqa: E501

        The tag of the RIME wheel used to build the managed image.  # noqa: E501

        :return: The rime_tag of this RimeManagedImage.  # noqa: E501
        :rtype: str
        """
        return self._rime_tag

    @rime_tag.setter
    def rime_tag(self, rime_tag):
        """Sets the rime_tag of this RimeManagedImage.

        The tag of the RIME wheel used to build the managed image.  # noqa: E501

        :param rime_tag: The rime_tag of this RimeManagedImage.  # noqa: E501
        :type: str
        """

        self._rime_tag = rime_tag

    @property
    def repo_uri(self):
        """Gets the repo_uri of this RimeManagedImage.  # noqa: E501

        The URI of the repository.  # noqa: E501

        :return: The repo_uri of this RimeManagedImage.  # noqa: E501
        :rtype: str
        """
        return self._repo_uri

    @repo_uri.setter
    def repo_uri(self, repo_uri):
        """Sets the repo_uri of this RimeManagedImage.

        The URI of the repository.  # noqa: E501

        :param repo_uri: The repo_uri of this RimeManagedImage.  # noqa: E501
        :type: str
        """

        self._repo_uri = repo_uri

    @property
    def status(self):
        """Gets the status of this RimeManagedImage.  # noqa: E501


        :return: The status of this RimeManagedImage.  # noqa: E501
        :rtype: RimeManagedImageStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this RimeManagedImage.


        :param status: The status of this RimeManagedImage.  # noqa: E501
        :type: RimeManagedImageStatus
        """

        self._status = status

    @property
    def package_requirements(self):
        """Gets the package_requirements of this RimeManagedImage.  # noqa: E501

        A list of all system package requirements used to build this image.  # noqa: E501

        :return: The package_requirements of this RimeManagedImage.  # noqa: E501
        :rtype: list[ManagedImagePackageRequirement]
        """
        return self._package_requirements

    @package_requirements.setter
    def package_requirements(self, package_requirements):
        """Sets the package_requirements of this RimeManagedImage.

        A list of all system package requirements used to build this image.  # noqa: E501

        :param package_requirements: The package_requirements of this RimeManagedImage.  # noqa: E501
        :type: list[ManagedImagePackageRequirement]
        """

        self._package_requirements = package_requirements

    @property
    def pip_requirements(self):
        """Gets the pip_requirements of this RimeManagedImage.  # noqa: E501

        A list of all pip requirements used to build this image.  # noqa: E501

        :return: The pip_requirements of this RimeManagedImage.  # noqa: E501
        :rtype: list[ManagedImagePipRequirement]
        """
        return self._pip_requirements

    @pip_requirements.setter
    def pip_requirements(self, pip_requirements):
        """Sets the pip_requirements of this RimeManagedImage.

        A list of all pip requirements used to build this image.  # noqa: E501

        :param pip_requirements: The pip_requirements of this RimeManagedImage.  # noqa: E501
        :type: list[ManagedImagePipRequirement]
        """

        self._pip_requirements = pip_requirements

    @property
    def pip_libraries(self):
        """Gets the pip_libraries of this RimeManagedImage.  # noqa: E501

        A list of all pip libraries installed on this image as obtained by running `pip list`.  # noqa: E501

        :return: The pip_libraries of this RimeManagedImage.  # noqa: E501
        :rtype: list[ManagedImagePipLibrary]
        """
        return self._pip_libraries

    @pip_libraries.setter
    def pip_libraries(self, pip_libraries):
        """Sets the pip_libraries of this RimeManagedImage.

        A list of all pip libraries installed on this image as obtained by running `pip list`.  # noqa: E501

        :param pip_libraries: The pip_libraries of this RimeManagedImage.  # noqa: E501
        :type: list[ManagedImagePipLibrary]
        """

        self._pip_libraries = pip_libraries

    @property
    def python_version(self):
        """Gets the python_version of this RimeManagedImage.  # noqa: E501

        The version of Python used to build the Robust Intelligence image.  # noqa: E501

        :return: The python_version of this RimeManagedImage.  # noqa: E501
        :rtype: str
        """
        return self._python_version

    @python_version.setter
    def python_version(self, python_version):
        """Sets the python_version of this RimeManagedImage.

        The version of Python used to build the Robust Intelligence image.  # noqa: E501

        :param python_version: The python_version of this RimeManagedImage.  # noqa: E501
        :type: str
        """

        self._python_version = python_version

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
        if issubclass(RimeManagedImage, dict):
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
        if not isinstance(other, RimeManagedImage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
