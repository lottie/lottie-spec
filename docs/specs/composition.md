# Composition

<h2 id="animation">Animation</h2>

{schema_string:composition/animation/description}

{schema_object:composition/animation}

### Versioning Guidelines

Tools implementing the Lottie specification should consider the following
guidelines:

* Major version updates may contain breaking changes that are not compatible
with previous versions of the specification.
* Minor version updates are typically adding new functionality and should not
contain breaking changes.
* Patch version updates are typically making minor changes to already existing
functionality.

#### Authoring Tools

Authoring tools should specify the latest version of the Lottie Specification.
They may want to allow the targeted major version to be configurable to
facilitate playback on a wide range of players. Changing the targeted major
version may also require changes to the animation for any breaking changes
between versions.

Authoring tools should always use the latest minor/patch version for the
targeted major version(s) as these are backwards compatible, even if the
authoring tool doesn't support any of the newer functionality.

#### Animation Players

Players should determine what major versions they support and also any
conditional logic to handle brekaing changes across major versions as needed.
Players should expect to handle animations that specify both newer and older
versions of the Lottie specification and should issue a warning if:

* The animation specifies a major version that is not supported.
* The animation specifies a newer minor version.
* No warning needed if the specified patch version is different.

<h2 id="composition">Composition</h2>

{schema_string:composition/composition/description}

{schema_object:composition/composition}
