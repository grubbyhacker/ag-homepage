---
title: The Myth of REST
date: '2025-01-14'
draft: false
tags:
- programming
- distributed-systems
summary: Why your JSON API is just RPC over HTTP.
---

Nobody uses REST. Not really. 

Roy Fielding's dissertation described a highly decoupled, hypermedia-driven architecture where clients navigate state transitions via HATEOAS. What you built is RPC with HTTP verbs. And that is fine.

We need to stop pretending that using `POST /api/users/123/activate` is RESTful. It isn't. It's an RPC call telling the server to execute an action. 

Embrace RPC paradigms where they make sense. Use gRPC for internal service-to-service communication, and provide a GraphQL or JSON-RPC layer to the frontend. Stop twisting HTTP protocols into weird shapes.