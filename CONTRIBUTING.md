# Lottie Format Specification Contribution Guide

This repository contains the specification text as well as Pull Requests with suggested improvements and contributions.

When proposing or weighing-in on any issue or pull request, consider the [Code of Conduct](Code_of_Conduct.md) to better understand expected and unacceptable behavior.


## Workflow

1. The primary workflow is centered around the [main repository](https://github.com/lottie/lottie-spec/),
   utilizing the following features:
    * Pull Requests
    * Issues
    * Discussions

2. Regular, documented meetings of the LAC working group, to review and progress proposals
   through the various stages as outlined below.

Members of the community, who are interested in participating in discussions and other work
around the Lottie format, be it the format itself, documentation, libraries, tools or other services built around the format can do so around the repository.

In doing so, members can put forth _proposals_ for the format, which are well reasoned formal recommendations or suggestions put toward consideration by the community and working group, aimed at fixing or enhancing the Lottie format. Proposals can be initiated either via issues or pull requests (as detailed below). Any issue raised is considered an RFC, subject to review, comments and deliberation by both community and working group. An RFC may begin as an issue or PR, and may not initially be reasoned out enough to be considered a formal proposal (see below). However, it will eventually have to be detailed enough to be considered a proposal.

## Definitions

### Lottie Animation Community

Lottie Animation Community (or LAC) is a non-profit open source project hosted by The Linux Foundation, dedicated to establishing the Lottie File Format as an efficient, scalable and cross-platform animated vector graphics technology and open file format.

### Lottie Animation Working Group

A working group, put together by the LAC, is responsible for guiding the process, moderating discussions, and so forth. The working group will conduct regular meetings to review proposals, and either advance them through the process or put forward recommendations/suggestions for the same.

Relevant details of the working group, its members and tenure shall be published on the main repository.

### Sponsors

Individuals or organizations who are recognised by LAC are responsible for taking on proposals and guiding them through the process. Every proposal must have a sponsor attached to it, in order to progress through the process. A proposal may have multiple sponsors.

Sponsor organizations shall be transparently documented on the main repository.

### Editors

Either working group members or selected contributors responsible to repository maintenance.
to the main repository.


### Consensus

Consensus is defined as approval of two thirds of the Working Group. Proposals that require the introduction or changes of core features, will require unanimous approval of the entire
working group.

## Proposals

Proposals can come in the form of issues or pull requests. Discussions may be used for general discussion and brainstorming before it is put forth as a proposal and subsequently into the RFC process.

Submissions fall into one of two categories:

1. **Contributions that _do not_ change the specifications, or their interpretation**  
   These are issues and PRs largely aimed at improving legibility, fixing editorial errors,
   clearing up ambiguities, adding examples to existing specifications, or updating the tooling that generates the documentation.
   These may be progressed and merged without much process and typically only require one approval from a member of the LAC working group.

2. **Contributions that _do_ meaningfully change the specifications**  
   These must progress through the stages of RFC, guided by a sponsor until
   they are ultimately accepted or rejected.

Once a proposal is raised either via issues or pull request, it is considered to be an RFC.

RFCs are guided by a sponsor through a series of stages: **_explainer, proposal, draft, and accepted (or rejected)_**, each of which has suggested entrance criteria and next steps detailed below. RFCs typically advance one stage at a time but may advance multiple stages at a time. Stage advancements typically occur during Working Group meetings, but may also occur on GitHub.

In general, it's preferable to start with a pull request so that we can best evaluate the RFC in detail. However, starting with an issue is also permitted if the full details are not worked out.

All RFCs start as either an explainer or a proposal. They will be tagged with the appropriate tag on GitHub as it progresses.

### Explainer

An RFC in the Explainer stage captures a described problem or partially-considered solutions. 

An explainer does not need to meet any entrance criteria. An Explainer may be an issue or a pull request (though an illustrative pull request is preferable).

#### Entrance criteria

* A well defined problem or use case. 
* Identification of potential concerns, challenges, and drawbacks.

As implied by the name, the goal at the Explainer stage is to capture the issue, and from there, reject it by considering other possible solutions or that it is not aligned with the guiding principles, or to move forwards with the next stage.

Once determined that the explainer is compelling, it should seek the entrance criteria for proposal.

### Proposal

An RFC in the Proposal stage is a solution to a problem with enough detail to be discussed further. It must be backed by a willing Sponsor. A Proposal's goal is to make a compelling case for acceptance by describing the problem and formalizing the solution. A proposal should be a pull request.

#### Entrance criteria

* Identified sponsor
* Identified target  profile for the proposal
    * A proposal may not add features to the core profile immediately, but rather pick an extension or module (or be a
      module of its own). Core specifications may only change when an extension or module is migrated into core  via
      a separate proposal.
* Clear explanation of the problem and solution
* Illustrative examples
* .json Files for testing
* Initial draft of the specification changes

A Proposal is subject to the same discussion as an Explainer: ensuring that it is well aligned with the guiding principles,a problem worth solving, and the preferred solution to that problem. A Sponsor is not expected to have confidence in every detail at this stage and should instead focus on identifying and resolving issues and edge-cases. To better understand the technical ramifications of the proposal, a sponsor is encouraged to implement it in a Lottie
library.

Most Proposals are expected to evolve or change and may be rejected. Therefore, it is unwise to rely on a Proposal in a production Lottie Library. Lottie libraries may implement proposals, though are encouraged to not enable the proposed feature without explicit opt-in.

### Draft

An RFC in the Draft stage is a fully formed solution. There is Consensus that the RFC is a good candidate for inclusion in the official specifications. A Draft's goal is to formally describe the solution and resolve any potential concerns. **A Draft must be submitted as a pull request.**

#### Entrance criteria

* Consensus within the Working Group
* Resolution of identified concerns and challenges
* Relevant changes to the specifications, including the JSON schema when applicable
* Relevant tests and test .json files
* Compliant implementation in an established library or tool of their choosing

A Proposal becomes a Draft when the set of problems or drawbacks have been fully considered and accepted or resolved, and the solution is deemed desirable. A Draft's goal is to complete final specification edits that are ready to be merged and implement the draft in Lottie libraries along with tests to gain confidence that the description is sufficient.

Drafts may continue to evolve and change, occasionally dramatically, and are not guaranteed to be accepted. Therefore, it is unwise to rely on a draft in a production Lottie Service. Lottie libraries should implement drafts to provide valuable feedback, though are encouraged not to enable the draft feature without explicit opt-in when possible.

### Accepted

An RFC at the accepted stage is a completed solution. According to an Editor it is ready to be merged into the main repository. The RFC is ready to be implemented by Lottie libraries.

#### Entrance criteria

* Consensus that the solution is complete
* 3 Approvals given by members of the LAC on the merge request
* Complete specification edits, including schema, examples, and/or prose
* Compliant implementation in a lottie library (fully tested and merged or ready to merge)

A Draft is accepted when the working group or editor (in the case of non-invasive edits as outlined before) has been convinced via implementations and tests that it appropriately handles all edge cases; that the specification changes not only precisely describe the new syntax and semantics but include sufficient documentation and examples; and that the RFC includes edits to any other affected areas of the specifications.

An accepted RFC is merged into the Lottie specification's main repository by an Editor and will be included in the next released revision.

### Blocked

At any stage of the process, any member of the Working Group may raise an objection, sending the RFC to the Blocked stage. The submitter can amend the RFC to resolve the issue raised in the objection. If the objecting Working Group member is satisfied with the amendment, the RFC can go back to its previous stage.
 
If the proposal can be progressed after amendments, this avenue should be explored first. Should the submitter be unwilling or unable to make amendments, the proposal may be Rejected.


### Rejected

An RFC may be rejected at any point. The reason for rejection should be clearly specified. 

Most rejections occur when an Explainer is proven to be unnecessary or fails to meet the entrance criteria to become a Proposal. A Proposal may become rejected for similar reasons, if it fails to reach Consensus, or loses the confidence of its Sponsor. Likewise, a Draft may encounter unforeseen issues during the process which cause it to lose Consensus or the confidence of its Sponsor.

RFCs which have lost a Sponsor will not be rejected immediately, but may become rejected if they fail to attract a new Sponsor.


### Contributing to Lottie Libraries

Should a new addition be made to the Lottie specifications or a Lottie library first?

Libraries seek to be compliant, which means they might discourage changes that cause them to behave differently from the specifications. However, they also encourage pull requests for changes that accompany an RFC _Proposal_ or _Draft_. Proposals won't be _Accepted_ until it has experience being implemented in a Lottie library.

To allow a library to remain compliant to the specifications while also implementing _Proposals_ and _Drafts_, the library's maintainers may request that these new features are disabled by default with opt-in options, or they may simply wait to merge a well-tested pull request until the Proposal is _Accepted_.


## Specification Release Process

The file format specifications are published using a semantic versioning system.

Each published version of the specifications is identified by a unique sequence of major, minor, and patch numbers, following these guidelines:

* Increasing the major version number signals the possibility of breaking changes and significant incompatibilities.
* Increasing the minor version number happens when new features are introduced, but existing features should not be changed in an incompatible way.
* The patch version is used to publish minor changes that improve the clarity of the specifications without introducing new functionality.

Each version through a release process consisting of multiple stages to ensure all stakeholders have a say before a new version of the specification is published.

Different versions of the specification might be in different release stages at any given time.

### Active Development

This is the initial stage, new features and proposals are welcome.

Whether or not backwards-incompatible changes are accepted depends on the target version as described above.


### Requesting Comments

Once the LAC working group has reached a consensus that the specification is ready to start the publishing process,
it will request comments on the draft specification from stakeholders.

New features and changed can be introduced based on the feedback but most new contributions should target a following version.

When the target version is an increase in the major version, LAC guarantees that this stage will last a minimum of 3 weeks before moving forward to the next stage.


### Feature freeze

After all the comments have been addressed and accepted into the specifications, the draft version goes into feature freeze
where no new features should be introduced. The LAC working group will still accept fixes that clarify ambiguities, correct mistakes, or otherwise
don't change compliance requirements.

When the target version is an increase in the major version, LAC guarantees that this stage will last a minimum of one week before publishing the specifications.

### Published

When the LAC working group is confident no more work is needed to release a version of the specifications, a final vote is performed to approve
the specifications for publishing.

If consensus is reached, then the version is published and can no longer be changed in any way.
Any further work should target a higher version number. Errata should be published as a new version of the specifications with increased patch number.

If consensus is not reached, the version goes back to the *Active Development* stage.
