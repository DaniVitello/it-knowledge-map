---
title: "Internet & Web"
area: "Frontend"
numero: 1
aliases: ["Internet & Web"]
tags: [concepto, it/frontend]
---
# Internet & Web

> **Área:** [[02 - Frontend/00 - Índice Frontend|Índice Frontend]] · **Concepto 1 de 25**

## Qué abarca
- HTTP
- HTTPS
- URLs
- request/response
- cliente-servidor

## Mis notas
<!-- ai:start -->
# Comprehensive Study Guide: Architectural Dynamics of the Modern Web (HTTP, TLS, and URIs)
<!-- ai:end -->

## Overview & Core Architectural Pillars

Modern distributed web architectures depend on three standardized pillars to facilitate reliable, secure, and scalable client-server interactions:
1. **Uniform Resource Identifiers (URIs)** for resource identification across namespaces.
2. **Hypertext Transfer Protocol (HTTP)** for application-layer semantics, state management, and transport mappings.
3. **Transport Layer Security (TLS)** for confidentiality, message integrity, server authentication, and operational trust.

Over three decades of standardization by the Internet Engineering Task Force (IETF) have decoupled abstract application semantics from underlying wire formats, minimized connection setup latency, and replaced outdated cryptographic heuristics with zero-trust primitives.

---

## Section 1: Resource Identification & URI Governance

### Generic URI Structure
Normatively defined under **STD 66 / RFC 3986**, a Uniform Resource Identifier (URI) is a compact, structured sequence of characters identifying an abstract or physical resource without dictating its retrieval mechanism. 

A complete URI conforms to the formal syntax:
$$\text{URI} = \text{scheme} \text{ ":" } [ \text{ "//" } \text{authority} ] \text{ path } [ \text{ "?" } \text{query} ] [ \text{ "#" } \text{fragment} ]$$

| URI Component | Structural Delimiter | Processing Domain | Architectural Function |
| :--- | :--- | :--- | :--- |
| **Scheme** | Terminates with `:` | Generic Parser / Runtime Engine | Specifies the protocol scheme context (`http`, `https`, `ftp`, `urn`) [cite: 1, 2]. |
| **Authority** | Prefixed by `//` | Domain Name System (DNS) / Network Layer | Designates administrative governance over the identifier namespace; includes host, optional port, and user info [cite: 2]. |
| **Path** | Prefixed by `/` | Origin Server Application | Supplies hierarchical context to locate a resource within the authority scope [cite: 2]. |
| **Query** | Prefixed by `?` | Origin Server Application / Script | Delivers non-hierarchical key-value parameters (`key=value&...`) for dynamic computing/filtering [cite: 2]. |
| **Fragment** | Prefixed by `#` | Client User Agent | Targets a secondary sub-element payload; **never** transmitted in HTTP request messages [cite: 2]. |

### Character Sets, Percent-Encoding, and Substructure Ownership
* **Character Partitioning**: RFC 3986 divides ASCII into *reserved* delimiters (`/`, `?`, `#`, `:`, `@`, `&`, `=`, etc.) and *unreserved* characters [cite: 2].
* **Percent-Encoding**: When a reserved delimiter is used as literal data rather than a structural boundary, it must be percent-encoded as `%` followed by two hexadecimal digits (e.g., an ASCII space `0x20` encodes as `%20`) [cite: 2].
* **Path Governance (RFC 8820)**: RFC 8820 (which obsoleted RFC 7320) establishes that internal path structures belong strictly to the URI authority (origin server) [cite: 7, 9]. External standards are explicitly forbidden from mandating rigid path hierarchies on applications [cite: 9].

---

## Section 2: Evolution of HTTP Semantics and Wire Protocols

### Separation of Core Semantics from Wire Formats (STD 97 / RFC 9110)
Historically, HTTP specifications bundled abstract semantics directly with wire-level formatting rules [cite: 11, 12]. In June 2022, the IETF HTTP Working Group (HTTPBIS) published **STD 97**, permanently separating core application semantics from wire transports [cite: 4, 5, 13]:
* **Core Semantics**: Standardized in **RFC 9110** (Semantics) and **RFC 9111** (Caching) [cite: 4, 5]. Defines methods (GET, POST, PUT, DELETE, PATCH, etc.), status codes ($1xx$ through $5xx$), header field registries, and caching behavior [cite: 4, 5].
* **Wire Transport Mappings**:
  * **HTTP/1.1 (RFC 9112)**: ASCII text-based messages over persistent TCP connections [cite: 4, 5, 12].
  * **HTTP/2 (RFC 9113)**: Binary framing layer supporting stream multiplexing over a single TCP connection; uses **HPACK (RFC 7541)** for header compression [cite: 4, 5, 12].
  * **HTTP/3 (RFC 9114)**: Binary framing over **QUIC** (UDP-based transport), removing transport-level head-of-line blocking; uses **QPACK (RFC 9204)** for field compression [cite: 4, 5].

```
┌────────────────────────────────────────────────────────────────────────┐
│                      HTTP Semantics (RFC 9110)                         │
│                     HTTP Caching   (RFC 9111)                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Maps Onto
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
  HTTP/1.1 (RFC 9112)         HTTP/2 (RFC 9113)         HTTP/3 (RFC 9114)
   Text over TCP             Binary over TCP            Binary over QUIC
                            (HPACK: RFC 7541)          (QPACK: RFC 9204)
```

### Historical Timeline of HTTP Standards

```
1996          1997        1999              2014                 2015        2018        2022
 │             │           │                 │                    │           │           │
 ├─ RFC 1945   ├─ RFC 2068 ├─ RFC 2616       ├─ RFC 7230-7235     ├─ RFC 7540 ├─ RFC 8446 ├─ RFC 9110-9114
 │  (HTTP/1.0) │  (HTTP/1.1)│  (Ref Spec for  │  (Clarified        │  (HTTP/2  │  (TLS 1.3)│  (STD 97 Semantics &
 │             │           │   15 years)     │   Semantics / 7231)│   SPDY)   │           │   Updated Wire Formats)
```

* **HTTP/1.0 (RFC 1945, May 1996)**: Short-lived connections per request; basic ASCII request/response [cite: 12].
* **HTTP/1.1 (RFC 2068, Jan 1997 / RFC 2616, June 1999)**: Introduced persistent TCP connections and pipelining [cite: 12]. Clarified in 2014 by RFCs 7230–7235 (notably RFC 7231 for semantics) [cite: 12].
* **HTTP/2 (RFC 7540, May 2015)**: Derived from SPDY; introduced binary framing, multiplexing on a single TCP connection, and HPACK [cite: 4, 5, 12].
* **HTTP/3 (RFC 9114, June 2022)**: Built on QUIC/UDP; resolves transport head-of-line blocking [cite: 4, 5, 12].

### GET Request Payload Processing Evolution & Operational Risks
The guidance surrounding message bodies in GET requests has progressively tightened across specification iterations:
1. **RFC 2616 (1999)**: Bodies implicitly disallowed; servers instructed to ignore payloads on methods lacking defined body semantics [cite: 15].
2. **RFC 7231 (2014)**: Bodies noted as carrying "no defined semantics", warning that implementations might reject or drop payloads [cite: 15].
3. **RFC 9110 (2022)**: Explicitly rules that content in a GET request **cannot alter the meaning or target of the request** [cite: 15]. Clients **SHOULD NOT** transmit a request body with GET unless prior knowledge exists that the origin server processes it [cite: 15].

#### Operational Risks of Transmission:
* **Cache Poisoning**: Caching proxies omit payloads when computing cache keys, serving stale/unintended data to subsequent requests [cite: 15].
* **Proxy Rejection**: Intermediaries and WAFs strip payloads or drop connections with a `400 Bad Request` [cite: 15].
* **HTTP Request Smuggling**: Inconsistent framing handling between edge proxies and backend origin servers creates desynchronization vulnerabilities [cite: 15].

---

## Section 3: Transport Security (TLS 1.2 vs. TLS 1.3) & PKI

### Architectural Comparison
HTTPS executes standard HTTP semantics over an encrypted TLS channel [cite: 3]. Operating between transport layer protocols (TCP/UDP) and application semantics, TLS delivers privacy (symmetric ciphers), authentication (X.509 digital certificates), and integrity (AEAD) [cite: 3, 16]. Standardized as **RFC 8446**, TLS 1.3 reformed the protocol compared to TLS 1.2 (RFC 5246) [cite: 3, 6, 16].

| Feature / Primitive | TLS 1.2 (RFC 5246) | TLS 1.3 (RFC 8446) |
| :--- | :--- | :--- |
| **Standard Handshake Latency** | 2-RTT (Two full round trips) [cite: 16, 17, 18] | 1-RTT (Single round trip) [cite: 3, 16, 17, 18] |
| **Resumption Latency** | 1-RTT [cite: 16] | 0-RTT (Pre-Shared Key early data) [cite: 3, 16, 18] |
| **Key Exchange** | Static RSA, Static DH, DHE, or ECDHE [cite: 6, 16, 18] | Ephemeral Diffie-Hellman ONLY (ECDHE / DHE) [cite: 16, 18] |
| **Forward Secrecy** | Optional (lost if static RSA is used) [cite: 16, 18] | **Mandatory** across all connections [cite: 3, 16, 18] |
| **Ciphers Supported** | Menu of >100 combinations (CBC, RC4, 3DES) [cite: 3, 17] | Restricted to 5 **AEAD-only** ciphers [cite: 3, 18] |
| **Handshake Security** | Plaintext (Certificates visible in transit) [cite: 16] | Encrypted immediately following `ServerHello` [cite: 3, 16, 18] |
| **Signature Schemes** | Vulnerable PKCS#1 v1.5 allowed [cite: 6, 18] | Replaced by **RSA-PSS**; entire transcript signed [cite: 6, 18] |

### Vulnerabilities Removed in TLS 1.3
TLS 1.3 eliminated legacy features responsible for historic attacks against TLS 1.2:
* **Million-Message / Bleichenbacher Attack & ROBOT**: Exploit flaws in RSA encryption padding (PKCS#1 v1.5) [cite: 6].
* **POODLE, BEAST, Lucky 13**: Vulnerabilities targeting Cipher Block Chaining (CBC) mode padding and MAC-then-Encrypt constructions [cite: 6, 16].
* **LogJam, FREAK, WeakDH, CurveSwap**: Downgrade attacks where middle-man adversaries manipulate unsigned portions of the handshake to force weak export-grade DH parameters [cite: 6].

### Detailed TLS 1.3 1-RTT Handshake Sequence

```
Client                                                  Server
  │                                                       │
  │─── ClientHello ──────────────────────────────────────►│ (Flight 1)
  │      + Supported Versions (1.3)                       │
  │      + Cipher Suites & Client Random                  │
  │      + key_share (Speculative ECDHE Public Value)     │
  │      + Server Name Indication (SNI)                   │
  │                                                       │
  │◄── ServerHello ───────────────────────────────────────│ (Flight 2)
  │      + Selected Cipher Suite                          │
  │      + key_share (Server ECDHE Public Value)          │
  │                                                       │
  │   [Endpoints derive Master Secret locally;]           │
  │   [Handshake traffic is encrypted from this point]    │
  │                                                       │
  │◄── EncryptedExtensions ───────────────────────────────│ (Flight 2 cont.)
  │◄── Certificate (Server X.509 Chain) ──────────────────│
  │◄── CertificateVerify (Signature over Transcript) ─────│
  │◄── Finished (Server MAC) ─────────────────────────────│
  │                                                       │
  │─── Finished (Client MAC) ────────────────────────────►│ (Flight 3)
  │─── Encrypted Application Data (HTTP Payload) ────────►│
  ▼                                                       ▼
```

### 0-RTT PSK Resumption & Replay Attack Vulnerabilities
Clients holding a Pre-Shared Key (PSK) session ticket from a previous handshake can send encrypted application data in their initial `ClientHello` flight (0-RTT) [cite: 3, 16, 18].
* **Security Risk**: Because 0-RTT data is transmitted before an interactive handshake completes, an attacker can capture and replay the packet stream to the server [cite: 6, 16, 18].
* **Mitigation Protocol**:
  1. Origin servers/gateways must enforce **Idempotent Method Restrictions**, allowing 0-RTT data processing **only** for safe HTTP methods (GET, HEAD) [cite: 3, 18].
  2. Non-idempotent, state-changing requests (POST, PUT, DELETE, PATCH) must **never** be accepted via 0-RTT [cite: 6, 16, 18].
  3. Server ticket validation incorporates time-elapsed checks to reject replayed ticket windows [cite: 6].

### Public Key Infrastructure (PKI) & Revocation
* **Certificate Chain of Trust**: Consists of a Root CA (self-signed, pre-installed in trust store) $\rightarrow$ Intermediate CA(s) $\rightarrow$ End-Entity Certificate [cite: 16].
  * *Operational Pitfall*: Omitting intermediate certificates during server configuration causes connection failures on clients lacking Automated Information Access (AIA) fetching [cite: 16].
* **OCSP Stapling**: Rather than forcing clients to perform out-of-band queries to a CA's Online Certificate Status Protocol (OCSP) responder (which adds latency and reveals browsing history), the origin server periodically fetches a signed OCSP response from the CA and "staples" it directly inside the TLS handshake [cite: 16].

---

## Section 4: Short-Answer Practice Questions

### Question 1
**According to STD 66 / RFC 3986, what is the processing domain of a URI fragment identifier, and how is it handled during HTTP request generation?**

**Answer:**
A URI fragment identifier (prefixed by `#`) is processed exclusively by the client user agent to target a sub-structure or secondary element within the retrieved resource payload [cite: 2]. It is never transmitted in HTTP request messages sent to origin servers [cite: 2].

---

### Question 2
**Explain the core architectural re-alignment established by STD 97 / RFC 9110 in 2022.**

**Answer:**
STD 97 / RFC 9110 permanently separated abstract HTTP semantics (request methods, status codes, header registries, caching) from transport-specific wire formats [cite: 4, 5, 13]. Abstract semantics defined in RFC 9110 now map cleanly onto multiple wire protocols: HTTP/1.1 text framing (RFC 9112), HTTP/2 binary streams (RFC 9113), and HTTP/3 QUIC streams (RFC 9114) [cite: 4, 5].

---

### Question 3
**How does HTTP/3 eliminate transport-level head-of-line blocking compared to HTTP/2?**

**Answer:**
HTTP/2 multiplexes multiple streams over a single TCP connection; a single lost TCP packet stalls all multiplexed streams while TCP retransmits the missing segment [cite: 4, 5, 12]. HTTP/3 replaces TCP with QUIC (a UDP-based transport), allowing independent binary streams to be transmitted without blocking unrelated streams when packet loss occurs [cite: 4, 5].

---

### Question 4
**Why was static RSA key exchange removed in TLS 1.3?**

**Answer:**
Static RSA key exchange lacks forward secrecy; if a server's private key is compromised in the future, an attacker can decrypt all historical recorded traffic [cite: 6, 16]. Furthermore, RSA key exchange was vulnerable to million-message/Bleichenbacher padding oracle attacks (e.g., ROBOT) [cite: 6]. TLS 1.3 mandates ephemeral Diffie-Hellman (ECDHE/DHE) key exchange to guarantee forward secrecy across all sessions [cite: 3, 16, 18].

---

### Question 5
**Describe the primary security vulnerability associated with TLS 1.3 0-RTT session resumption and how servers mitigate it.**

**Answer:**
0-RTT early data is sent before an interactive handshake completes, making it vulnerable to replay attacks if an adversary captures and retransmits the flight [cite: 6, 16, 18]. Servers mitigate this by restricting 0-RTT data processing exclusively to safe, idempotent HTTP methods (GET, HEAD) and rejecting non-idempotent methods (POST, PUT, DELETE) transmitted in 0-RTT [cite: 3, 6, 18].

---

### Question 6
**What is the purpose of OCSP Stapling, and what two problems inherent to traditional OCSP does it resolve?**

**Answer:**
OCSP Stapling allows an origin server to periodically fetch a signed certificate revocation status from the CA and staple it directly to the TLS handshake [cite: 16]. It resolves:
1. **Performance Latency**: Clients do not need to make a separate HTTP network call to the CA responder before completing the handshake [cite: 16].
2. **Privacy Concerns**: CAs no longer track individual user browsing history via real-time OCSP lookup requests [cite: 16].

---

### Question 7
**According to RFC 9110, what are the restrictions and risks regarding bodies in HTTP GET requests?**

**Answer:**
RFC 9110 states that content in a GET request cannot alter the target or meaning of the request, and clients SHOULD NOT send a body with GET without explicit prior knowledge of server support [cite: 15]. Operational risks include cache poisoning by proxies that ignore bodies when generating cache keys, request stripping/dropping by intermediaries, and HTTP request smuggling [cite: 15].

---

### Question 8
**How does TLS 1.3 prevent protocol downgrade attacks like LogJam and FREAK?**

**Answer:**
In TLS 1.2, parts of the handshake negotiating the cipher suites were not digitally signed, allowing middle-man attackers to alter the advertised cipher list [cite: 6]. In TLS 1.3, the server signs the *entire* handshake transcript using its private key (via `CertificateVerify`), ensuring any modification to negotiated parameters causes handshake verification to fail [cite: 6, 18].

---

## Section 5: Essay Prompts for Deeper Exploration

### Essay Prompt 1
**Analyze the architectural evolution of transport efficiency across HTTP/1.1, HTTP/2, and HTTP/3.**  
*In your essay, address how each protocol version handles connection management, head-of-line blocking, and header compression (contrasting HPACK and QPACK). Explain how the introduction of QUIC shifts traditional network boundaries and how abstract HTTP semantics (RFC 9110) remain invariant across these wire format transformations.*

---

### Essay Prompt 2
**Critique the cryptographic design changes between TLS 1.2 and TLS 1.3.**  
*Evaluate the removal of static RSA key transport, CBC-mode ciphers, and user-defined Diffie-Hellman parameters. Discuss how TLS 1.3 achieves 1-RTT handshake latency, the security trade-offs introduced by 0-RTT early data, and how application-layer gateway practices must align with transport-layer guarantees to prevent vulnerabilities such as replay attacks.*

---

### Essay Prompt 3
**Synthesize the interactions between Resource Identification (RFC 3986 / RFC 8820), Application Caching (RFC 9111), and Transport Encapsulation in modern distributed systems.**  
*Detail the end-to-end processing of a URI from generic client parsing to server execution. Discuss the operational hazards of improper URI path design, query string misuse, non-standard request payload usage in safe methods, and how edge caching proxies can be compromised when application behaviors diverge from IETF normative standards.*

---

## Section 6: Glossary of Important Terms

* **AEAD (Authenticated Encryption with Associated Data)**: A form of symmetric encryption that simultaneously assures both confidentiality and authenticity/integrity of data payloads [cite: 3, 16]. Mandatory in TLS 1.3 [cite: 3, 18].
* **AIA (Authority Information Access)**: A certificate extension enabling user agents to dynamically fetch missing intermediate CA certificates [cite: 16].
* **ALPN (Application-Layer Protocol Negotiation)**: A TLS extension used during the handshake to negotiate application protocols (e.g., `h2` or `h3`) without adding extra network round trips [cite: 16].
* **Bleichenbacher Attack**: An adaptive chosen-ciphertext attack leveraging error feedback from PKCS#1 v1.5 RSA encryption padding to perform private key operations [cite: 6].
* **Ephemeral Diffie-Hellman (ECDHE / DHE)**: A key agreement mechanism where a temporary, unique public/private key pair is generated for every session, providing Perfect Forward Secrecy [cite: 6, 16, 18].
* **HPACK**: A header compression algorithm defined in RFC 7541 for HTTP/2 that uses static/dynamic tables and Huffman coding over a stateful TCP connection [cite: 4, 5, 12].
* **Idempotent Method**: An HTTP method where multiple identical requests produce the same intended effect on the server state as a single request (e.g., GET, PUT, DELETE) [cite: 3, 18].
* **Middlebox Ossification**: The phenomenon where network middleboxes (firewalls, proxies) hardcode assumptions about protocol wire formats, breaking connections when new protocol versions are deployed [cite: 6].
* **OCSP Stapling**: An optimization where origin servers query the CA's OCSP responder, cache the signed revocation response, and include ("staple") it in the TLS handshake [cite: 16].
* **Percent-Encoding**: A mechanism defined in RFC 3986 to encode reserved or non-ASCII characters as a `%` followed by two hexadecimal digits [cite: 2].
* **Perfect Forward Secrecy (PFS)**: A property guaranteeing that the compromise of long-term server private keys does not expose past recorded session traffic [cite: 3, 6, 16, 18].
* **QPACK**: A field compression specification defined in RFC 9204 for HTTP/3 designed to operate over out-of-order QUIC streams without HOL blocking [cite: 4, 5].
* **QUIC**: An encrypted, UDP-based transport protocol providing multiplexed stream transport, integrated TLS 1.3 encryption, and fast connection establishment [cite: 4, 5, 12].
* **SNI (Server Name Indication)**: A TLS extension where the client specifies the hostname it is attempting to connect to during the `ClientHello`, enabling virtual hosting on shared IP addresses [cite: 18].
* **STD 97**: The IETF standard series encompassing RFC 9110, establishing core HTTP semantics independently of underlying wire transports [cite: 4, 13].

## Relacionados
- [[03 - Backend/01 - Cliente-Servidor|Cliente-Servidor]] · *Backend*
- [[03 - Backend/02 - HTTP|HTTP]] · *Backend*
- [[05 - Networking & Internet/01 - Internet|Internet]] · *Networking / Internet*
- [[05 - Networking & Internet/16 - HTTP|HTTP]] · *Networking / Internet*
- [[05 - Networking & Internet/18 - Request - Response|Request / Response]] · *Networking / Internet*
- [[05 - Networking & Internet/19 - HTTP Methods|HTTP Methods]] · *Networking / Internet*
- [[05 - Networking & Internet/20 - HTTP Status Codes|HTTP Status Codes]] · *Networking / Internet*
- [[05 - Networking & Internet/21 - Headers - Cookies|Headers / Cookies]] · *Networking / Internet*

---
[[02 - Frontend/00 - Índice Frontend|Índice Frontend]] · [[02 - Frontend/02 - HTML|HTML]] →
