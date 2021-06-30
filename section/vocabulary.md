## The RML-star vocabulary {#vocabulary}

RML-star extends the RML vocabulary by introducing five new terms: 

- `rml:embeddedTriplesMap` is a new property that connects a term map with a triples map. It indicates the term map will generate [=embedded triples=] generated by the triples map.
- `rml:StarMap` is a class that represents functions that generate [=embedded triples=] from [logical references](https://rml.io/specs/rml/#reference). Conforming to the RDF-star specification, it can be used to generate subjects and objects. This class is the domain of `rml:embeddedTriplesMap`.
- `rml:NonAssertedTriplesMap` is a new kind of triples map that indicates triples maps of this subclass do not create [=asserted triples=], as is the default for triples maps. A triples map of this subclass *does* create [=embedded triples=] if it is used together with `rml:embeddedTriplesMap` and `rml:StarMap`.
- `rml:objectMap` and `rml:subjectMap` are new properties which can be used like `rr:objectMap` and `rr:subjectMap`, but with `rml:StarMap` added to their range.

### Overview of RML-star terms
The new terms are summarized in the following tables.

Property | Domain | Range
-|-|-
`rml:embeddedTriplesMap` | `rr:StarMap` |  `rml:TriplesMap`
`rr:subjectMap` | `rr:TriplesMap` | Union of `rr:SubjectMap`, `rml:StarMap`
`rr:objectMap` | `rr:TriplesMap` | Union of `rr:ObjectMap`, `rr:RefObjMap`, `rml:StarMap`

Class | Superclass 
- | -
`rml:StarMap` | `rr:TermMap`
`rml:NonAssertedTriplesMap` | `rr:TriplesMap`

In certain cases, a join is needed to generate [=embedded triples=]. To achieve this, the range of the property `rr:joinCondition` is changed. We summarize the change in the following table.

Property | Old domain | New domain
-|-|-
`rr:joinCondition` | `rr:RefObjMap` | Union of `rr:RefObjMap`, `rml:StarMap`