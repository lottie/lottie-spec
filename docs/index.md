# Lottie Animation Format

Welcome to the official documentation for Lottie,
a JSON-based format for animated vector graphics.

This manual contains formal specification and documentation for the
Lottie file format, offering insights into its structure and features.

The main target audience for this manual are developers that want to
create tools within the Lottie ecosystem as it provides details about
the JSON internals.


## Status of this manual

The Lottie specification is still a work in progress, this document
contains a subset of features that have been approved by the
Lottie Animation Community. The documentation and specs will be expanded
as more of the Lottie format becomes standardized.

Once the draft is complete, there will be an announcement by the
Lottie Animation Community.


## Where to start

Lottie files use JSON to structure its data so basic JSON knowledge
is required to understand the specidification.

To understand Lottie data, it's useful to start learning about
[basic values](./specs/values.md) and [animated properties](./specs/properties.md).

The root object of any Lottie animation is the [Animation](./specs/composition.md#animation) object.

If you want a machine readable specification the [JSON Schema](./specs/schema.md) is also available.

<lottie src="static/logo.json" loop="false" buttons="false" background="none" />
