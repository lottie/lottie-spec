# Lottie Format

A Lottie file is a JSON-encoded object, whose top-level structure is {link:composition/animation}.

See the [JSON schema](schema.md) for a full description of the JSON format.


## Media Type

This section registers a new MIME media type, `video/lottie+json` in conformance with BCP 13 [RFC4288].

Media type name:
: `video`

Media subtype name:
: `lottie+json`

Required parameters:
: None

Optional parameters:
: None

Encoding considerations:
: 8bit, UTF-8 encoded text

Security considerations:
: Security considerations relating to the generation and consumption of Lottie files are similar to application/json and are discussed in Section 12 of [RFC8259].<br/>
Documents may reference external image assets. Security considerations in the Media Type registrations for those formats shall apply.<br/>
A commonly used extension to the format outside of the spec is "expressions" which allow code execution. In itself, the Lottie format is a text based json document and relatively harmless. Support for expressions and security considerations for the same are dependent on the renderer used.<br/>

Interoperability considerations:
: Processors must expect that content received is well-formed JSON, but it cannot be guaranteed that the content is valid to a particular Schema version, or that the processor will recognize all of the elements and attributes in the document.

Published specification:
: The specification is published by Lottie Animation Community, and is publicly available at<br/>
Documentation: <https://lottie.github.io/lottie-spec/1.0/> <br/>
JSON Schema: <https://lottie.github.io/lottie-spec/1.0/specs/schema/> <br/>

Applications which use this media:
: Lottie is/will be used by systems and applications which require scalable static or interactive vector graphics animations.

Fragment identifier considerations:
: None

Restrictions on usage:
: None

Additional information:
: Deprecated alias names for this type:
    : N/A
: Magic number(s):
    : N/A
: File extension(s):
    : `.lot`
: Macintosh file type code:
    : N/A
: Object Identifiers:
    : N/A

Person to contact for further information:
: Lottie Animation Community lottie-dev AT googlegroups.com

Intended usage:
: COMMON

Author/Change controller:
: Lottie Animation Community (<https://lottie.github.io>) working group

