# Composition

<h2 id="animation">Animation</h2>

{schema_string:composition/animation/description}

{schema_object:composition/animation}

### Time and Duration

The animation's playable frame range is defined by `ip` (In Point, inclusive)
and `op` (Out Point, exclusive). The frame at `op` is NOT rendered; the
animation loops or stops at that boundary.

The total duration in frames is `op - ip`, and the duration in seconds is
`(op - ip) / fr`.

Implementations MUST treat `op` as an exclusive boundary. `op` MUST be
strictly greater than `ip`.

Example: `ip: 0`, `op: 30`, `fr: 30` defines a 30-frame, 1-second animation
playing frames `0..29`.

### Versioning Guidelines

The Lottie specification version number uses a semantic versioning system,
tools implementing the specification SHOULD consider the following
guidelines:

* Major version signal the possibility of breaking changes that are not compatible
with previous versions of the specification.
* Minor version updates typically add new functionality but do not
contain breaking changes for existing features.
* Patch version updates typically make minor changes or clarifications to
already existing functionality.

#### Authoring Tools

Authoring tools SHOULD specify the latest version of the Lottie Specification.
They MAY allow the major version to be configurable to facilitate playback on a
wider range of players. Changing the targeted major version MAY also require
changes to the produced animation in the case of any breaking changes between
major versions.

#### Animation Players

Players SHOULD determine what major versions they support and handle breaking
changes across supported major versions. Players SHOULD be able to handle
animations that specify both newer and older versions of the Lottie
specification and SHOULD issue a warning if:

* The animation specifies a major version that is not supported.
* The animation specifies a newer minor version.
* No warning needed if the specified patch version is different.

<h2 id="composition">Composition</h2>

{schema_string:composition/composition/description}

{schema_object:composition/composition}
