# Lottie Format Specification Contribution Guide

This repository contains the specification text as well as Pull Requests
with suggested improvements and contributions.

The outline of this document closely follows contribution guidelines
set out in the [GraphQL](https://github.com/graphql/graphql-spec) specification's process

Contributions that do not change the interpretation of the spec but instead
improve legibility, fix editorial errors, clear up ambiguity and improve
examples are encouraged and are often merged by a spec editor with little
process.

However, contributions that _do_ meaningfully change the interpretation of the
spec must follow an RFC (Request For Comments) process led by a _sponsor_
through a series of _stages_ intended to improve _visibility_, allow for
_discussion_ to reach the best solution, and arrive at _consensus_. This process
becomes ever more important as Lottie Animation Community Broadens.

When proposing or weighing-in on any issue or pull request, consider the
[Code of Conduct](https://github.com/lottie/lottie-spec/blob/main/8._Code_of_Conduct.md)
to better understand expected and unacceptable behavior.


## Contributing to Lottie Libraries

A common point of confusion for those who wish to contribute to the Lottie Format is where
to start. In fact, you may have found yourself here after attempting to make an
improvement to a Lottie library. Should a new addition be made to the Lottie
spec first or a Lottie library first? Admittedly, this can become a bit of a
[chicken-or-egg](https://en.wikipedia.org/wiki/Chicken_or_the_egg) dilemma.

Libraries seek to be "spec compliant", which means they discourage
changes that cause them to behave differently from the spec as written. However,
they also encourage pull requests for changes that accompany an RFC _proposal_
or RFC _draft_. In fact, a spec contribution RFC won't be _accepted_ until it
has experience being implemented in a Lottie library.

To allow a library to remain spec compliant while also implementing _proposals_
and _drafts_, the library's maintainers may request that these new features are
disabled by default with opt-in option flags or they may simply wait to merge a
well-tested pull request until the spec proposal is _accepted_.

## Workflow

1. The primary workflow is centered around _this_ repository,
   utilizing the following features.
    * Pull Requests
    * Issues
    * Discussions

2. Regular, documented meetings of the LAC working group, to review and progress proposals 
   through the various stages as outlined below.

Members of the community, who are interested in participating in discussions and other work 
around the Lottie Format, be it the format itself, documentation, libraries, tools or 
other services built around the format can do so around the repository.

In doing so, members can put forth _proposals_ for the format, which are 
well reasoned formal recommendations or suggestions put toward consideration by 
the community and working-group, aimed at fixing, improving or enhancing the
Lottie Animation Format. Proposals can be initiated either via issues or pull requests 
(as detailed below). Any issue raised is considered an RFC, subject to review, 
comments and deliberation by both community and working-group. An RFC may begin as an 
issue or PR, and may not initially be reasoned out enough to be considered a formal 
proposal (see below). However, it will eventually have to be detailed enough to be 
considered a proposal.

## Key stakeholders

**Lottie Animation Working Group**

A working group, put together by the LAC, is responsible for guiding the process, 
moderating discussions, and so forth. The working group will conduct regular meetings to 
review proposals, and either advance them through the process or put
forward recommendations/suggestions for the same.

Relevant details of the working-group, its members and tenure shall be published on 
the main repository.

**Lottie Sponsors**

Individuals or organizations who are recognised by LAC are responsible for taking on proposals and guiding them through
the process. Every proposal must have a sponsor attached to it, in order to progress through the process. A proposal may
have multiple sponsors.

Sponsor organizations shall be transparently documented on the main repository.

**Editors**

Either working-group members or selected contributors responsible to repository maintenance: i.e have write/edit access
to the main repository.


## Classifying Contributions

Contributions can come in the form of issues or pull requests. Contributions through github discussions are not
recognized. Discussions may be used for general discussion and brainstorming before it is put forth as a proposal and
subsequently into the RFC process.

Of contributions, they may be classified as follows:

1. **Contributions that _do not_ change the spec, or interpretation of the spec**  
   These are issues and PRs largely aimed at improving legibility, fixing editorial errors, 
   clearing up ambiguities, or adding examples to existing specifications. 
   These may be progressed and merged without much process.

2. **Contributions that _do_ meaningfully change the interpretation of the spec**  
   These must progress through the stages of RFC, guided by a sponsor until 
   they are ultimately accepted or rejected.

### Contribution Stages

Once a proposal is raised either via issues or pull request, it is considered to be an RFC.

RFCs are guided by a sponsor through a series of stages: **_explainer, proposal, draft, and accepted (or rejected)_**,
each of which has suggested entrance criteria and next steps detailed below. RFCs typically advance one stage at a time
but may advance multiple stages at a time. Stage advancements typically occur during Working Group meetings, but may
also occur on GitHub.

In general, it's preferable to start with a pull request so that we can best evaluate the RFC in detail. However,
starting with an issue is also permitted if the full details are not worked out.

All RFCs start as either an explainer or a proposal. They will be tagged with the appropriate issue/pr tag on GitHub as
it progresses.

### Stage 0: Explainer

An RFC at the explainer stage captures a described problem or partially-considered solutions. An explainer does not need
to meet any entrance criteria. An explainer’s goal is to prove or disprove a problem and guide discussion towards either
rejection or a preferred solution. An explainer may be an issue or a pull request (though an illustrative pull request
is preferrable).

There are no entrance criteria for an explainer. It can simply be an issue, grievance or query.

As implied by the name explainer, the goal at this stage is to capture the issue, and from there, knock it down (reject)
by considering other possible related solutions, showing that the motivating problem can be solved with no change to the
specification, or that it is not aligned with the guiding principles.

Once determined that the explainer is compelling, it should seek the entrance criteria for proposal.

### Stage 1: Proposal

An RFC at the proposal stage is a solution to a problem with enough fidelity to be discussed in detail. It must be
backed by a willing sponsor. A proposal's goal is to make a compelling case for acceptance by describing both the
problem and the solution via examples and spec edits. A proposal should be a pull request.

**Entrance criteria:**

* Identified sponsor
* Identified target spec profile for the proposal
    * A proposal may not add features to the core profile immediately, but rather pick an extension or module (or be a
      module of its own). Core specifications may only change when an extension or module is migrated into core-spec via
      a separate proposal.
* Clear explanation of the problem and solution
* Illustrative examples
* .json Files for testing
* Incomplete spec edits
* Identification of potential concerns, challenges, and drawbacks

A proposal is subject to the same discussion as an explainer: ensuring that it is well aligned with the guiding
principles, is a problem worth solving, and is the preferred solution to that problem. A sponsor is not expected to have
confidence in every detail at this stage and should instead focus on identifying and resolving issues and edge-cases. To
better understand the technical ramifications of the proposal, a sponsor is encouraged to implement it in a Lottie
library.

Most proposals are expected to evolve or change and may be rejected. Therefore, it is unwise to rely on a proposal in a
production Lottie Library. Lottie libraries may implement proposals, though are encouraged to not enable the proposed
feature without explicit opt-in.

### Stage 2: Draft

An RFC at the draft stage is a fully formed solution. There is working-group consensus that the problem identified
should be solved, and this particular solution is preferred. A draft's goal is to precisely and completely describe the
solution and resolve any concerns through library implementations. **A draft must be a pull request.**

**Entrance criteria:**

* Consensus the solution is preferred (typically via Working Group)
* Resolution of identified concerns and challenges
* Precisely described with spec edits
* Relevant tests and test .json files
* Compliant implementations:
    * A library or tool of their choosing
    * Machine readable Lottie-schema as hosted in this repository

A proposal becomes a draft when the set of problems or drawbacks have been fully considered and accepted or resolved,
and the solution is deemed desirable. A draft's goal is to complete final spec edits that are ready to be merged and
implement the draft in Lottie libraries along with tests to gain confidence that the spec text is sufficient.

Drafts may continue to evolve and change, occasionally dramatically, and are not guaranteed to be accepted. Therefore,
it is unwise to rely on a draft in a production Lottie Service. Lottie libraries should implement drafts to provide
valuable feedback, though are encouraged not to enable the draft feature without explicit opt-in when possible.

### Stage 3: Accepted

An RFC at the accepted stage is a completed solution. According to a spec editor it is ready to be merged as-is into the
spec document. The RFC is ready to be deployed in Lottie libraries.

Entrance criteria:

* Consensus the solution is complete (via editor or working group)
* Complete spec edits, including examples and prose
* Compliant implementation in a lottie library (fully tested and merged or ready to merge)

A draft is accepted when the working group or editor (in the case of non invasive edits as outlined before) has been
convinced via implementations and tests that it appropriately handles all edge cases; that the spec changes not only
precisely describe the new syntax and semantics but include sufficient motivating prose and examples; and that the RFC
includes edits to any other affected areas of the spec. Once accepted, its sponsor should encourage adoption of the RFC
by opening issues or pull requests on other popular Lottie libraries.

“Consensus” is defined as approval of two thirds of working-group. Proposals that call for or necessitate the movement
of a feature previously regarded as an extension, into core-features, will require unanimous approval of the entire
working-group.

An accepted RFC is merged into the Lottie spec's main branch by an editor and will be included in the next released
revision.

### Stage X: Rejected

An RFC may be rejected at any point. The reason for rejection should be clearly specified. If the proposal can be
progressed after amendments, this avenue should be explored first.

Most rejections occur when an explainer is proven to be unnecessary, is misaligned with the guiding principles, or fails
to meet the entrance criteria to become a proposal. A proposal may become rejected for similar reasons as well as if it
fails to reach consensus or loses the confidence of its sponsor. Likewise a draft may encounter unforeseen issues during
implementations which cause it to lose consensus or the confidence of its sponsor.

RFCs which have lost a sponsor will not be rejected immediately, but may become rejected if they fail to attract a new
sponsor.

Once rejected, an RFC will typically not be reconsidered. Reconsideration is possible if a sponsor believes the original
reason for rejection no longer applies due to new circumstances or new evidence.
