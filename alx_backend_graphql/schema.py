#!/usr/bin/ python3
import graphene

# class Query(CRMQuery, graphene.ObjectType)
class Query(graphene.ObjectType):
        hello = graphene.String()
        
        def resolve_hello(root, info):
              return "Hello, GraphQL!"
    
schema = graphene.Schema(query=Query)