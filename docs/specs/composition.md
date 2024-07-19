# Composition

<h2 id="animation">Animation</h2>

{schema_string:composition/animation/description}

{schema_object:composition/animation}

### Versioning Guidelines

Tools implementing the Lottie specification SHOULD consider the following
guidelines:

* Major version updates MAY contain breaking changes that are not compatible
with previous versions of the specification.
* Minor version updates typically add new functionality and SHOULD NOT
contain breaking changes.
* Patch version updates typically make minor changes to already existing
functionality.

#### Authoring Tools

Authoring tools SHOULD specify the latest version of the Lottie Specification.
They MAY allow the major version to be configurable to facilitate playback on a
wider range of players. Changing the targeted major version MAY also require
changes to the produced animation in the case of any breaking changes between
major versions.

#### Animation Players

Players SHOULD determine what major versions they support and handle brekaing
changes across supported major versions. Players SHOULD expect to handle
animations that specify both newer and older versions of the Lottie
specification and SHOULD issue a warning if:

* The animation specifies a major version that is not supported.
* The animation specifies a newer minor version.
* No warning needed if the specified patch version is different.

<h2 id="composition">Composition</h2>

{schema_string:composition/composition/description}

{schema_object:composition/composition}
