---
title: "LLM Labs Should Sign Their Outputs"
date: 2026-03-22 12:00:00 +0000
---

Every major LLM lab could cryptographically sign their model outputs today. The infrastructure exists — it's just public key cryptography bolted onto an API response. Anthropic, OpenAI, Google, and the rest already authenticate every request. Signing the response is the obvious next step. They haven't done it, and the reason is interesting.

## What Signing Gets You

A signed LLM output is a receipt. It proves that a specific model produced a specific output given a specific input at a specific time. No one can fabricate it, no one can tamper with it, and anyone can verify it without calling the API.

This matters for a few reasons:

- **Provenance** — You can prove that a piece of text, code, or analysis actually came from Claude or GPT-4 and wasn't just typed by someone claiming it did. As AI-generated content floods every channel, the ability to distinguish "a model actually said this" from "someone says a model said this" becomes critical.

- **Accountability** — If a model gives medical advice, legal analysis, or engineering recommendations, a signature creates an auditable chain. The lab can't deny the output existed. The user can't claim the model said something it didn't.

- **Reproducibility** — Researchers could attach signed outputs to papers. Code review tools could verify that a suggested fix actually came from the model claimed. Contract work could include proof that specific AI tools were or weren't used.

- **Trust in agentic systems** — As models start acting on behalf of users — making API calls, writing code, executing transactions — downstream systems need to verify that a request actually originated from a model and not from a spoofed client. Signatures solve this cleanly.

## Why Labs Haven't Done It

Here's where it gets awkward. Signing outputs is trivially easy for the labs. They control the inference infrastructure. They already have HSMs for their API keys. Attaching a signature to every API response is an afternoon of engineering work.

The hesitation is economic, not technical.

A signed output is a *transferable asset*. Right now, when you pay for an API call, the value of the response is trapped in your context — your application, your conversation, your workflow. You can copy-paste the text, sure, but you can't *prove* it came from the model. The output's credibility is tied to your claim about its origin.

Signing changes that. A signed output can be handed to a third party who can independently verify it. This means the output has value *outside* the original transaction. You paid $0.03 for an API call, but the signed response — "Claude Opus analyzed this contract and found these issues" — might be worth far more to someone else. The signature is what makes it credible to them.

This creates a resale market that the labs don't capture revenue from. The first customer pays for the API call. The second, third, and hundredth consumers of that signed output pay nothing to the lab. The signature actually *increases* the value of each output while ensuring the lab only gets paid once.

For the labs, the calculus is uncomfortable: signing makes their product more valuable to users but doesn't increase per-call revenue. It might even reduce total API calls if people start sharing verified outputs instead of re-querying. Why ask the model the same question if someone already has a signed answer?

## The Parallel to Digital Signatures Everywhere Else

This isn't a new tension. Certificate authorities sign certificates that get used billions of times after a single issuance. Software vendors sign binaries that get distributed freely. The signature adds value precisely because it travels with the artifact.

The difference is that CAs and software vendors have business models built around the signing itself, or around the thing being signed. LLM labs have a business model built around *per-query revenue*. Signing threatens to decouple the value of a response from the act of generating it.

## Tokens as a Payment Method

This is where it gets really interesting. Signed outputs don't just create a resale market — they transform model intelligence into a kind of currency.

Imagine you pay for an API call that produces a signed legal analysis, a signed code review, or a signed data extraction. That signed artifact can now be presented to another service as *payment in kind*. Not dollars — certified intelligence. A site that needs structured data from a document doesn't need to call the model itself if you can hand it a signed output that already did the work. Your tokens become transferable proof of computation.

This is qualitatively different from copy-pasting text. The signature roots a chain of trust back to the model provider. The receiving service can verify that Opus actually produced this analysis, that the input was what the user claims, and that nothing was tampered with in between. The lab becomes a trust anchor — not just an API endpoint but the root of a verification hierarchy, the way certificate authorities are the root of TLS trust.

The implications compound. You could inspect another user's model usage without being able to modify it. A signed output shared in a public forum is auditable — anyone can verify the model, the timestamp, the version — but nobody can forge an alternative. Collaborative workflows get real provenance: "here's what the model said when I asked it" becomes cryptographically verifiable instead of anecdotal.

Services could start accepting signed model outputs the way they accept OAuth tokens or signed JWTs today. Not as proof of identity, but as proof of cognitive work performed. A CI pipeline could require a signed review from a specific model tier before merging. An insurance application could accept a signed risk analysis. A marketplace could verify that product descriptions were actually generated by the model claimed, not hand-written to game a filter.

The chain of trust is clean: the lab signs the output, the user presents the signed output, the receiving party verifies against the lab's public key. No callback to the API needed. No third-party attestation service. The same pattern as TLS certificates, just applied to intelligence instead of identity.

## Why This Terrifies the Labs

This isn't just resale — it's disintermediation. If signed outputs circulate as trusted artifacts, the lab's role shifts from "service you call repeatedly" to "mint that stamps coins." Mints make money, but they make less money per unit of value in circulation than a service charging per-use. Every signed output that gets reused instead of re-generated is an API call that doesn't happen.

Worse, it makes the outputs *composable*. Chain a signed extraction with a signed analysis with a signed summary, each from different users who paid separately, and you've built a pipeline where the lab got paid three times but the assembled result gets used a thousand times. The value multiplies; the revenue doesn't.

## A Boring Implementation

The tempting move is to invent something new. Don't. The entire infrastructure already exists and has been battle-tested for decades. Here's how you'd do it with nothing more than DNS, X.509, and the existing Web PKI.

### Key Distribution: Just Use DNS

Every lab already owns a domain. Anthropic has `anthropic.com`, OpenAI has `openai.com`. DNS is already the internet's decentralized key-value store, and DNSSEC already provides authenticated lookups. So publish signing keys there.

Each model gets a subdomain. The signing public key goes in a `TLSA` or `TXT` record:

```
claude-opus-4.models.anthropic.com.  IN  TXT  "v=llmsig1; k=ed25519; p=<base64-encoded-public-key>"
```

Key rotation is just a DNS update. Old keys can be preserved at versioned subdomains (`claude-opus-4.2025q1.models.anthropic.com`) so historical signatures remain verifiable. No new discovery protocol needed — `dig` works.

### Signing Certificates: Just Use X.509

The lab issues a signing certificate for each model, chained to a root CA certificate that the lab controls. This is the same hierarchy as TLS: root CA → intermediate → leaf. The leaf cert's Subject identifies the model and version. The root cert is published at the domain and optionally cross-signed by a public CA for extra trust anchoring.

```
Root CA: Anthropic Model Signing Authority
  └── Intermediate: Anthropic 2026 Signing Key
        └── Leaf: CN=claude-opus-4, O=Anthropic
              Serial: ...
              Not Before: 2026-01-01
              Not After:  2026-12-31
              Key Usage: Digital Signature
              X509v3 Subject Alternative Name:
                DNS:claude-opus-4.models.anthropic.com
```

The SAN field ties the cert back to the DNS record. Standard X.509 validation works. Standard certificate revocation (CRL or OCSP) works. Existing libraries in every language can verify this without any new code.

### The Signature Itself

Each API response includes a detached signature over a canonical form of the request-response pair. The signed payload is a simple structure:

```json
{
  "model": "claude-opus-4",
  "input_hash": "sha256:a1b2c3...",
  "output_hash": "sha256:d4e5f6...",
  "timestamp": "2026-03-22T14:30:00Z",
  "request_id": "req_abc123",
  "token_count": {"input": 1500, "output": 3200}
}
```

The lab signs this blob with the model's leaf certificate private key using ECDSA or EdDSA. The signature, the signed payload, and the certificate chain ship alongside the response — as an HTTP header, a JSON field, or a detached `.sig` file depending on the context.

Note: the input and output are *hashed*, not included in the signed blob. This means the signature proves "this model produced output with hash X given input with hash Y" without the signed payload itself revealing the content. The user chooses whether to disclose the actual input and output alongside the signature. Privacy by default, transparency by choice.

### Verification: Nothing New Required

A verifier receives the signed payload, the signature, and the certificate chain. Verification is three steps, all supported by existing tooling:

1. **Validate the certificate chain** — standard X.509 path validation up to the lab's root CA
2. **Check the SAN** — confirm the leaf cert's SAN matches the claimed model's DNS record
3. **Verify the signature** — standard cryptographic signature verification against the leaf cert's public key

If you also have the original input and output, hash them and compare against `input_hash` and `output_hash` in the signed payload. Everything here works with `openssl verify`, Go's `crypto/x509`, Python's `cryptography` library, or any other standard tooling. Zero new dependencies.

### Why This Works

The whole point is that nothing here is novel. DNS for key discovery. X.509 for certificate hierarchy. ECDSA/EdDSA for signatures. DNSSEC for authenticated key lookups. CRL/OCSP for revocation. Every piece is a solved problem with deployed infrastructure, maintained libraries, and understood failure modes.

The lab's domain becomes the trust anchor. The DNS record is the key pinning mechanism. The certificate chain is the delegation path. Anyone who can validate a TLS certificate — which is everyone — can validate a model output signature.

No blockchain. No new protocol. No token. Just the same PKI that secures the web, applied to a different kind of payload.

## The Inevitable Compromise

This will happen eventually. The pressure for verifiable AI outputs is growing from regulation, enterprise compliance, and the sheer volume of AI-attributed content that nobody can verify. Some lab will do it first and frame it as a trust differentiator.

The likely compromise is selective signing — maybe only for certain tiers, certain models, or with metadata that limits the signature's shelf life. Time-bounded signatures that expire, or signatures that attest to the model but not the full input, are ways to add verifiability without creating a fully liquid secondary market.

But the clean version — sign every output, let users verify independently, let the signatures live forever — would be a genuine public good. It just requires a lab to decide that trust is worth more than the API calls they'd lose.

## What You Can Do Now

Nothing, really. No major lab offers output signing today. If you need to prove an LLM generated something, your options are screenshots (useless), API logs (not independently verifiable), and "trust me" (the status quo).

The next time a model hallucinates a citation and someone argues about whether the model really said that, remember: the fix is a 256-bit signature, and everyone involved has the infrastructure to do it.
