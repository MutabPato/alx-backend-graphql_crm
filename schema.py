#!/usr/bin/ python3
from graphene_django import graphene


class Query(graphene.ObjectType):
    def __init__(self):
        self.name = "hello"
        self.type = str

    def __str__(self):
        return f"Hello, GraphQL!"