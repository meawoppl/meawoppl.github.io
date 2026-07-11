---
title: "POST /negotiate"
date: 2026-03-30 12:00:00 +0000
---

Every API you use today has structure. Endpoints, schemas, versioned contracts, documentation. You know what you're sending. You know what you're getting back. The shape of the data is a promise, and when the promise breaks, you file a bug.

That world is dying.

## The Trajectory

Look at what's already happening. Stripe's API has hundreds of endpoints. Twilio has dozens. AWS has thousands. Each one is a precisely defined contract. This is what you send, this is what you get, here are the error codes, here is the rate limit. Entire engineering teams exist to maintain these contracts across versions.

Now look at what LLMs do to API consumption. You don't read the docs anymore. You describe what you want to an agent, and it figures out which endpoints to call, in what order, with what parameters. The human stopped talking to the API two years ago. The agent is the client now.

So why does the API still pretend a human is reading the docs?

## The Endpoint

Here's where it gets dark. If both sides of an API call are LLMs, an agent on the client side, a model on the server side, why maintain the charade of structured endpoints at all? Why have `/v3/customers/{id}/subscriptions` when you could have:

```
POST /negotiate
Content-Type: application/natural

I need the monthly subscription details for customer
acme-corp, specifically the renewal date and current
seat count. I'm authorized via OAuth token in the header.
I'd prefer JSON but can handle XML if that's what you've got.
```

And the server responds:

```json
{
  "understanding": "You want subscription info for acme-corp",
  "result": {
    "renewal": "2026-04-15",
    "seats": 847,
    "plan": "enterprise"
  },
  "confidence": 0.97,
  "assumptions": ["Used most recent active subscription"],
  "cost": "$0.003"
}
```

No schema. No versioning. No documentation. Just two language models having a conversation about what one of them wants from the other.

## Why "Negotiate"

It's not called `/ask` or `/query` because that implies a fixed catalog of things you can request. It's `/negotiate` because every call is a bespoke transaction. The client describes intent. The server interprets, clarifies if needed, and names a price. Both sides are LLMs. Both sides are reasoning about what the other wants.

Want real-time data? Costs more. Want it cached from an hour ago? Cheaper. Want a guaranteed schema in the response? That's a premium. You're asking the server to conform to *your* structure instead of its default. Want the server to call three other services and synthesize the results? Sure, but the cost reflects the compute.

Every API call becomes a miniature contract negotiation. The parameters aren't in a spec. They're in the conversation.

## The Death of Documentation

In this world, API documentation doesn't exist. Can't exist. The API's capabilities aren't fixed. They're whatever the backing model can figure out how to do with the resources it has access to. Today it can query your subscription data. Tomorrow someone hooks up a new database and suddenly it can also tell you churn predictions. No new endpoint was created. No changelog was published. The model just... learned it could do a new thing.

You discover capabilities by asking. "Can you do X?" is a valid API call. The response might be "Yes, here's X" or "No, but here's something close" or "I could if you gave me Y." The API surface is the model's entire competence, which shifts with every deployment.

Documentation becomes a vibe. "It can usually do billing stuff. Sometimes it's weird about refunds."

## The Horror: Debugging

Something broke. Your agent asked for customer data and got back someone else's subscription details. In the structured API world, you check the request, check the response, compare against the schema, find the bug. Deterministic. Reproducible. Fixable.

In the `/negotiate` world? Good luck. Your agent phrased the request slightly differently this time. The server model was updated overnight and now interprets "current subscription" to mean "most recently created" instead of "currently active." The confidence score was 0.94, high enough that your agent didn't ask for clarification. Nobody logged the full negotiation because the payloads are huge natural language blobs.

The bug isn't in the code. The bug is in the *interpretation*. Two language models had a miscommunication, and now someone is getting billed wrong. Reproducing it requires reproducing the exact model versions, the exact conversation history, the exact system prompts on both sides. You're not debugging software. You're doing **forensic linguistics**.

## The Horror: Pricing

Structured APIs have pricing pages. $0.01 per API call. $0.005 per record. Predictable. Budgetable.

`/negotiate` pricing is dynamic. The server model assesses the complexity of your request, the compute required, the data accessed, the real-time premium, the schema-conformance tax, and quotes you a price. *Per call.* Your client agent can counter-offer, "I don't need real-time, give me the cached version", and the price drops. But you won't know what a request costs until you make it, and two identical-seeming requests might cost different amounts because the model assessed their complexity differently.

Your cloud bill becomes non-deterministic. Finance will love that.

## The Horror: Auth

Authentication in this world isn't a token check. It's a judgment call. The server model evaluates your claimed identity, your OAuth token, your request history, the sensitivity of the data you're asking for, and decides whether you seem authorized enough. Not *are* authorized. *Seem* authorized.

"The model thought you had access" is not a sentence anyone wants to hear in a security postmortem.

## The Horror: Rate Limiting

There's no rate limit. There's a server-side model that gets increasingly annoyed with you. Make too many requests and the responses get slower. More expensive. Less detailed. Eventually it just starts responding with "Please try again later", not because a counter hit a threshold, but because the model decided you were being unreasonable.

Your agent, also an LLM, interprets this as a negotiation tactic and starts being more polite in its requests. Two AIs are now engaged in a passive-aggressive standoff over your API quota. Nobody asked for this.

## Why It Might Happen Anyway

Here's the thing. This is terrible. Everyone involved in building reliable systems should be horrified. But the economics might not care.

Maintaining structured APIs is **expensive**. Designing schemas, writing docs, versioning endpoints, handling deprecation, supporting clients on old versions. That's a permanent tax on every engineering team that exposes a service. A `/negotiate` endpoint eliminates almost all of that overhead. The model figures it out. Ship the model, ship the data access, done.

And the client side? Nobody reads your API docs anyway. They paste them into an LLM and ask it to write the integration. Might as well cut out the middleman.

The company that realizes they can replace their entire API platform team with a fine-tuned model and a single endpoint will do it. The cost savings are too obvious. The fact that it makes debugging, pricing, auth, and reliability dramatically worse is a problem for the SRE team, and when has that ever stopped a cost-cutting decision?

## The Transition

It won't happen overnight. It'll start with the least critical endpoints, "ask our AI about your account" chatbot interfaces that nobody takes seriously. Then someone notices the chatbot can actually do everything the REST API does, just slower. Then it gets faster. Then someone proposes deprecating the REST API because maintaining both is expensive and the negotiation endpoint handles 90% of traffic already.

The structured endpoints stick around as "legacy" for a while. Then they don't.

## What Survives

Some things resist this. Financial transactions need deterministic outcomes. You can't negotiate a wire transfer. Real-time control systems need predictable latency. You can't negotiate with a PLC. Anything safety-critical needs reproducible behavior. "The model thought this was fine" doesn't hold up in court.

But everything else? The internal microservice that fetches user preferences? The third-party data enrichment API? The analytics pipeline that aggregates metrics? Those are all negotiable. And once you can negotiate, someone will decide you should.

## The Bright Side?

I'm straining for one. Maybe discoverability. Today, integrating a new API is a week of reading docs, understanding auth flows, handling edge cases, writing client code. In the `/negotiate` world, your agent just... asks the other agent what it can do. Integration becomes a conversation. "What data do you have? What can you do with it? What does it cost?" A five-minute negotiation replaces a week of integration work.

That's genuinely useful. It's also genuinely terrifying. The ease of integration means every service talks to every other service, all through natural language negotiation, with no fixed contracts, no schemas, and no way to predict what any given interaction will actually do.

We'll have built the most flexible, capable, and utterly incomprehensible infrastructure ever created. And the only documentation will be: `POST /negotiate`.
