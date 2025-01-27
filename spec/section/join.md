## Generating quoted triples from multiple sources {#join}

RML-star can create RDF-star triples from multiple [logical sources](https://rml.io/specs/rml/#logical-source).
When creating RDF-star triples from multiple [logical sources](https://rml.io/specs/rml/#logical-source), [join conditions](https://rml.io/specs/rml/#join-condition) are used, just like when using [referencing object maps](https://rml.io/specs/rml/#referencing-object-map) in RML.

If a [=star map=] has a [join condition](https://rml.io/specs/rml/#join-condition), it generates [=quoted triples=] as follows. Each combination of iterations, i.e., the [Cartesian product](https://en.wikipedia.org/wiki/Cartesian_product), from the *child source* and the *parent source* is looked at. Here, we consider as <dfn>child source</dfn> the [logical source](https://rml.io/specs/rml/#logical-source) of the [triples map](https://rml.io/specs/rml/#triples-map) in which the star map occurs, and as <dfn>parent source</dfn> the logical source of the star map's [=quoted triples map=]. A star map only generates quoted triples for combinations in which the join condition holds true. As is the case when [join conditions are used in in referencing object maps](https://rml.io/specs/rml/#logical-join), a join condition checks for equality of the [reference values](https://rml.io/specs/rml/#reference-value) of the [child](https://rml.io/specs/rml/#child-reference)/[parent reference](https://rml.io/specs/rml/#parent-reference) between iterations of the child/parent source.

<!--Following criterion is taken almost verbatim from the RML spec, mutatis mutandi: https://rml.io/specs/rml/#parent-query -->
If the [logical source](https://rml.io/specs/rml/#logical-source) of triples map in which a [=star map=] occurs and the logical source of star map's [=quoted triples map=] are not identical, then the star map must have at least one [join condition](https://rml.io/specs/rml/#join-condition).

<pre class="ex-input">
# contents of logical source ex:ClassesSource
entity,class
Alice,Person
Bobby,Dog
</pre>

<pre class="ex-input">
# contents of logical source ex:ConfidencesSource
entity,confidence
Alice,0.8
Bobby,0.6
</pre>

<pre class="ex-mapping nohighlight"><!-- nohighlight because otherwise the bolding is lost and we don't use highlighting anyway-->
# triples map that generates "type" triples
<#innerTriplesMap>
  a rml:NonAssertedTriplesMap ;
  rml:logicalSource ex:ClassesSource ;
  rml:subjectMap [
    rr:template "http://example.com/{entity}"
  ] ;
  rr:predicateObjectMap [
    rr:predicate rdf:type ;
    rml:objectMap [ rr:template "http://example.com/{class}" ]
  ] .

# triples map that generates "confidence" triples
<#outerTriplesMap> a rr:TriplesMap ;
  rml:logicalSource ex:ConfidencesSource ;
  rml:subjectMap [
    rml:quotedTriplesMap <#innerTriplesMap>
    <b>rr:joinCondition [
      rr:parent "entity" ;
      rr:child "entity" ;
    ]</b>
  ] ;
  rr:predicateObjectMap [
    rr:predicate ex:confidence ;
    rml:objectMap [ rml:reference "confidence" ]
  ] .
</pre>

<pre class="ex-output">
<< ex:Alice a ex:Person >> ex:confidence 0.8 .
<< ex:Bobby a ex:Dog >> ex:confidence 0.6 .
</pre>

### Using star map together with referencing object maps

It is also possible to generate [=quoted triples=] which themselves are built from multiple sources.
This is done by using a [=quoted triples map=] which contains a [referencing object map](https://rml.io/specs/rml/#referencing-object-map).

Note: this process for generating [=quoted triples=] with a [referencing object map](https://rml.io/specs/rml/#referencing-object-map) is not different from the general process to create quoted triples [described earlier](#quoted), but we include this section for clarity.

<pre class="ex-input">
# contents of logical source ex:ClassesSource
entity,class
Alice,Person
Bobby,Dog
</pre>

<pre class="ex-input">
# contents of logical source ex:ConfidencesSource
entity,confidence
Alice,0.8
Bobby,0.6
</pre>

<pre class="ex-mapping nohighlight"><!-- nohighlight because otherwise the bolding is lost and we don't use highlighting anyway-->
# triples map that generates objects of "type" triples
<#classTriplesMap>
  a rr:TriplesMap ;
  rml:logicalSource ex:ClassesSource ;
  rml:subjectMap [
    rr:template "http://example.com/{class}"
  ] .

# triples map that generates "type" triples using a join
<#innerTriplesMap>
  a rml:NonAssertedTriplesMap ;
  rml:logicalSource ex:ConfidencesSource ;
  rml:subjectMap [
    rr:template "http://example.com/{entity}"
  ] ;
  rr:predicateObjectMap [
    rr:predicate rdf:type ;
    rml:objectMap [
      <b>rr:parentTriplesMap <#classTriplesMap> ;
      rr:joinCondition [
        rr:parent "entity" ;
        rr:child "entity" ;
      ]</b>
    ]
  ] .

# triples map that generates "confidence" triples
<#outerTriplesMap>
  a rr:TriplesMap ;
  rml:logicalSource ex:ConfidencesSource ;
  rml:subjectMap [
    rml:quotedTriplesMap <#innerTriplesMap>
  ] ;
  rr:predicateObjectMap [
    rr:predicate ex:confidence ;
    rml:objectMap [ rml:reference "confidence" ]
  ] .
</pre>

<pre class="ex-output">
<< ex:Alice a ex:Person >> ex:confidence 0.8 .
<< ex:Bobby a ex:Dog >> ex:confidence 0.6 .
</pre>
