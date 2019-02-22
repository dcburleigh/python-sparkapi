"""Spark People Classes."""

from .spark_class import SparkDataClass, SparkAPI


class Person(SparkDataClass):
    create_attrs = ['firstName', 'lastName',
                     'displayName', 'emails', 'avatar',
                     'orgId', 'roles', 'licenses']

    def __init__(self, data, whitelist=(), blacklist=()):
        self.id = data.pop('id')
        self.firstName = data.pop('firstName', '')
        self.lastName = data.pop('lastName', '')
        self.displayName = data.pop('displayName', '')
        self.emails = data.pop('emails')
        self.roles = self.decode_list(data.pop('roles', []))
        self.licenses = self.decode_list(data.pop('licenses', []))
        self.status = data.pop('status', '')
        self.avatar = data.pop('avatar', '')
        self.orgId = data.pop('orgId')
        self.created = self.set_datetime(data.pop('created'))
        self.lastActivity = self.set_datetime(data.pop('lastActivity', None))
        self.invitePending = self.set_bool(data.pop('invitePending', False))
        self.loginEnabled = self.set_bool(data.pop('loginEnabled', False))
        super().__init__(data, whitelist, blacklist)

    @property
    def email(self):
        return self.emails[0]

    @property
    def update_params(self) -> dict:
        return {k: self.get(k, None) for k in self.create_attrs}

    def __str__(self):
        return 'Spark Person ({})'.format(self.emails[0])


# noinspection PyShadowingBuiltins
class People(SparkAPI):

    DataClass = Person

    def get_by_email(self, email, max=None):
        return self.list(email=email, max=max)

    def get_by_displayname(self, displayName, max=None):
        return self.list(displayName=displayName, max=max)

    def get_person(self, id):
        return self.get_by_id(id)

    def me(self):
        return self.get_by_id('me')

    def update(self, person=None, id=None, **params):
        if isinstance(person, Person):
            id = person.id
            payload = person.update_params
        elif id:
            payload = params
        else:
            raise ValueError('Must provide either a Person object or id and param dict')
        # payload = {name: value for name, value in params.items()}
        resp = self.session.put(self.url, id=id, payload=payload)
        return self.DataClass(resp.json())
