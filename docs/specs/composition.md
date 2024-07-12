# Composition

<h2 id="animation">Animation</h2>

{schema_string:composition/animation/description}

{schema_object:composition/animation}

### Versioning Guidelines

Tools implementing the Lottie specification SHOULD consider the following
guidelines:

* Major version updates MAY contain breaking changes that are not compatible
with previous versions of the specification.
* Minor version updates are typically adding new functionality and SHOULD NOT
contain breaking changes.
* Patch version updates are typically making minor changes to already existing
functionality.

#### Authoring Tools

Authoring tools SHOULD specify the latest version of the Lottie Specification.
They MAY want to allow the targeted major version to be configurable to
facilitate playback on a wide range of players. Changing the targeted major
version MAY also require changes to the animation for any breaking changes
between versions.

Authoring tools SHOULD always use the latest minor/patch version for the
targeted major version(s) as these are backwards compatible, even if the
authoring tool doesn't support any of the newer functionality.

#### Animation Players

Players SHOULD determine what major versions they support and also any
conditional logic to handle brekaing changes across major versions as needed.
Players SHOULD expect to handle animations that specify both newer and older
versions of the Lottie specification and SHOULD issue a warning if:

* The animation specifies a major version that is not supported.
* The animation specifies a newer minor version.
* No warning needed if the specified patch version is different.

<h2 id="composition">Composition</h2>

{schema_string:composition/composition/description}

{schema_object:composition/composition}
