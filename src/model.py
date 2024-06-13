"""The datamodel, which represents Person that has multiple
Address objects, each with PostalCode, City, Country.

Person --(1..n)--> Address
Address --(has a)--> PostalCode
PostalCode --(has a)--> City
City --(has a)--> Country

"""

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped
from .environment import Base


class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __init__(self, name):
        self.name = name


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)
    country = relationship(Country)

    def __init__(self, name, country):
        self.name = name
        self.country = country

    def example_no_mapped_hint(self):
        country = self.country  # hints as Any


class PostalCode(Base):
    __tablename__ = "postal_code"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    city: Mapped[City] = relationship(City)

    @property
    def country(self):
        return self.city.country

    def __init__(self, code, city):
        self.code = code
        self.city = city


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    street = Column(String(200), nullable=False)
    postal_code_id = Column(Integer, ForeignKey("postal_code.id"))
    postal_code: Mapped[PostalCode] = relationship(PostalCode)

    @property
    def city(self):
        return self.postal_code.city

    @property
    def country(self):
        return self.postal_code.country

    def __str__(self):
        return "%s\t%s, %s\t%s" % (
            self.street,
            self.city.name,
            self.postal_code.code,
            self.country.name,
        )
    
    def example_type_hints(self):
        street = self.street
        postal_code = self.postal_code.code
        # hints as Any due to no Mapped type hint
        country = self.postal_code.city.country
        country_name = self.postal_code.city.country.name


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    addresses: Mapped[set[Address]] = relationship(Address, collection_class=set)

    def __init__(self, name, *addresses):
        self.name = name
        self.addresses = set(addresses)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Person(name=%r)" % self.name

    def format_full(self):
        return "\t".join([str(x) for x in [self] + list(self.addresses)])
