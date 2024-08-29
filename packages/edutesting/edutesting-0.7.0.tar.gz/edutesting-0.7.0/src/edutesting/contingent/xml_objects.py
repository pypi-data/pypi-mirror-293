# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

from lxml import objectify
import six
from six.moves import map


class XmlElement(object):
    u"""
    Класс, содержащий значения атрибутов дочернего элемента
    в строковом типе
    """

    def __init__(self, xml_object):
        self._xml_object = xml_object
        self.type = self._xml_object.tag
        for k, v in six.iteritems(self._xml_object.__dict__):
            self.__dict__[k] = v.text

    def __repr__(self):
        return '<XmlElement tag:{type}; id:{id}>'.format(
            type=self.type,
            id=self.ID
        )

    def __getitem__(self, item):
        return self.__dict__[item]


class PersonXmlElement(XmlElement):
    u"""
    Класс для Person- и Delegate-элементов
    """
    def __init__(self, xml_object):
        super(PersonXmlElement, self).__init__(xml_object)
        self.fullname = ' '.join([
            self.LastName,
            self.FirstName,
            self.MiddleName if self.MiddleName else ''
        ])

    def __repr__(self):
        return '<PersonXmlElement tag:{type}; id:{id}>'.format(
            type=self.type,
            id=self.ID
        )


class XmlParsedObject(object):
    u"""
    Класс, содержащий в качестве атрибутов список дочерних элементов
    основных блоков xml документа.
    """
    def __init__(self, xml_file):
        self._source = xml_file
        self._document_tree = self.__get_document_tree()
        self.document = self._document_tree.getroot()
        self.persons = self._get_children('Persons')
        self.organizations = self._get_children('Organizations')
        self.accreditations = self._get_children('Accreditations')
        self.declarations = self._get_children('Declarations')
        self.declaration_org = self._get_children('DeclarationOrganizations')
        self.delegate_citizen_countries = self._get_children(
            'DelegateCitizenshipCountries'
        )
        self.delegate_docs = self._get_children('DelegateDocuments')
        self.delegate_persons = self._get_children('DelegatePersons')
        self.delegates = self._get_children('Delegates')
        self.edu_programms = self._get_children('EducationPrograms')
        self.licenses = self._get_children('Licenses')
        self.person_citizen_countries = self._get_children(
            'PersonCitizenshipCountries'
        )
        self.person_docs = self._get_children('PersonDocuments')

    def __repr__(self):
        return '<XmlParsedObject from {}>'.format(
            self._source.split('/')[-1]
        )

    def __getitem__(self, item):
        return self.__dict__[item]

    def __get_document_tree(self):
        with open(self._source, 'r') as source:
            doc_tree = objectify.parse(source)

        return doc_tree

    def _get_children(self, parent):
        parent_obj = self.document.Data.__dict__.get(parent, None)

        if parent == 'Persons' or parent == 'Delegates':
            obj = PersonXmlElement
        else:
            obj = XmlElement

        if parent_obj:
            result = list(map(
                obj,
                parent_obj.getchildren()
            ))
        else:
            result = None
        return result
