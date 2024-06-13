"""
Hover over variables to see how well the LSP handles the type hints
"""

from sqlalchemy import select

from environment import Session
from model import Person, Address


def session_query():
    people = Session.query(Person).join(Person.addresses).all()
    person = people[0]
    name = people[0].name
    person_address = list(people[0].addresses)[0]
    person_street = list(people[0].addresses)[0].street

    addresses = Session.query(Address).join(Address.postal_code).join(Address.postal_code.city).all()
    address = addresses[0]
    address_street = address.street
    address_postcode = address.postal_code.code


def typed_param(person: Person) -> Address:
    address = list(person.addresses)[0]
    street = address.street
    city = address.postal_code.city
    city_name = city.name
    return address


# def select():
#     person = Session.execute(select(Person)).first()
