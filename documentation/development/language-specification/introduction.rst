Introduction
============

Scope
-----

This specification defines the Harpy programming language and the normative requirements governing conforming Harpy implementations.

The specification defines the language itself, including its lexical structure, syntax, semantic rules, type system, expressions, operators, memory and representation semantics, contracts, error semantics, compile-time execution, fragments, metadata, calling conventions, assembly integration, and foreign and external interfaces.

The specification also defines the compiler-visible and compiler-controlled mechanisms required for the language to operate as specified. In particular, the Harpy Compiler interface exposed through ``_harpyc`` is normative where defined by this specification. Properties exposed through ``_harpyc`` are part of the observable behavior of a conforming implementation and shall conform to their specified semantics.

The specification further defines the relevant object, binary, linking, loading, and execution behavior of Harpy programs. This includes the object representation, ``.metapkginfo`` metadata, PLDC integration, the linker requirements, and the loader requirements necessary to implement the Harpy execution model.

The specification does not prescribe the internal architecture or algorithms of a compiler. A conforming implementation may use any internal organization, representation, optimization strategy, or compilation algorithm, provided that the resulting observable behavior conforms to this specification.

The specification is intended to permit multiple independent implementations. A conforming Harpy implementation shall therefore not depend on undocumented behavior of the original Harpy implementation.

The Harpy standard library, where provided, is not defined by this specification. A library may be linked by default by a particular environment, but such a library does not acquire special language status merely by being provided by that environment.

This specification does not generally define auxiliary development tools. Its normative toolchain requirements are limited to the Harpy language and the Harpy Compiler, together with the compilation, object, linking, loading, and execution mechanisms explicitly defined by this specification.

Diagnostic wording is not generally standardized. This specification defines the conditions under which diagnostics are required and, where applicable, the structure and semantics imposed by mechanisms such as ``@error`` and ``@warning``; it does not require a particular textual diagnostic message.

Terminology
-----------

**Harpy**
   The programming language defined by this specification.

**Harpy Compiler**
   A compiler implementing the compilation requirements of this specification. An implementation may provide the compiler under any product name, but references to the language implementation in this specification use the generic term *Harpy Compiler*.

**Source file**
   A file containing Harpy source text processed by the Harpy Compiler.

**Package**
   A Harpy source file. Each package is compiled individually.

**Module**
   A conceptual grouping of packages used to describe program organization. A module is not a syntactic construct and is not an independent semantic compilation entity.

**Program**
   An executable binary produced through the compilation and linking of Harpy packages and their required external components.

**Translation unit**
   The unit of source processing corresponding to a package during compilation. The compilation model described by this specification is expressed in terms of translation units.

**Target**
   The combination of a kernel, CPU, microarchitecture, and binary format for which a program is compiled.

**Implementation**
   A complete implementation of the requirements of this specification.

**Conforming implementation**
   An implementation that satisfies all requirements of this specification.

**Language version**
   The version of the Harpy language for which a program is intended to be interpreted and compiled.

**Specification version**
   The version of this specification defining the language and implementation requirements.

The terms defined above are normative. Other technical terms are used according to their ordinary meaning unless explicitly defined elsewhere in this specification.

Design Principles
-----------------

Harpy is designed around explicit semantics, predictable compilation, and direct control over the target system.

The principal design priorities of the language are, in order:

1. hardware control;
2. predictability;
3. expressiveness;
4. metaprogramming; and
5. interoperability.

These priorities do not constitute separate language modes. They describe the design constraints under which the language is defined.

Semantic Explicitness
~~~~~~~~~~~~~~~~~~~~~

Harpy does not permit semantic ambiguity.

Where a construct admits more than one interpretation under the rules of this specification, and the applicable context does not uniquely determine the interpretation, the program is ill-formed and the implementation shall diagnose the condition.

A conforming implementation shall not select an arbitrary interpretation to resolve such ambiguity. In particular, the implementation shall not use heuristics to assign semantics that are not established by the language rules.

Contextual resolution and constraint-based resolution are permitted where explicitly defined by the language. Such mechanisms shall resolve according to the applicable rules and constraints; they shall not constitute unrestricted type inference or heuristic deduction.

Harpy has no general type inference mechanism. Types and other semantic properties shall be established according to the explicit rules of the language.

Explicit Conversion and Representation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Harpy does not perform implicit conversions, promotions, coercions, casts, initialization conversions, or automatic type extensions unless a specific language rule explicitly defines such behavior.

Representation is a fundamental part of the Harpy semantic model. The language permits explicit control over representation, layout, alignment, byte order, bit order, memory access, sections, registers, calling conventions, and assembly.

A conforming implementation shall preserve the representation and semantic requirements established by the program and by this specification.

Compile-Time Correctness
~~~~~~~~~~~~~~~~~~~~~~~~

Harpy favors compile-time determination of semantic correctness.

Compile-time analysis shall establish all properties that are required by the language rules and can be established from compile-time information. Constructs for which the required semantic conditions cannot be established shall be rejected when the language requires those conditions to be known at compile time.

Runtime behavior shall not be used to give meaning to a construct whose required compile-time semantics have not been established.

This principle does not imply that every property of a program must be known at compile time. Runtime checks exist where explicitly required by the language, including constructs such as runtime-deferred contracts and other operations whose semantics require runtime validation.

No Implicit Policy
~~~~~~~~~~~~~~~~~~

Harpy provides mechanisms for explicitly defining policies concerning memory, representation, resources, permissions, and related properties. It does not impose a universal runtime safety policy.

Where a policy is expressed through language-defined mechanisms, the compiler shall enforce the requirements that follow from that policy.

Consequently, Harpy does not intrinsically guarantee a particular memory-safety model, allocation model, garbage-collection model, or runtime environment. A program may define or provide such mechanisms explicitly when required.

There is no mandatory Harpy runtime, garbage collector, or allocator.

Direct System Control
~~~~~~~~~~~~~~~~~~~~~

Harpy permits programs to directly control low-level aspects of execution when the corresponding language mechanisms are used correctly.

Direct memory access, custom representations, custom calling conventions, assembly, foreign symbols, and target-specific code are valid language facilities. Their use may make a program dependent on a particular target and therefore reduce portability, but does not by itself make the program non-conforming.

Low-level facilities do not provide a means of bypassing the semantic rules of the language. Compile-time contracts, type rules, representation requirements, metadata constraints, and other applicable requirements remain in force.

Deterministic Semantics
~~~~~~~~~~~~~~~~~~~~~~~

A conforming implementation shall not introduce implementation-defined language semantics.

Where this specification defines a semantic result, conforming implementations shall produce behavior consistent with that definition. Implementation freedom concerns the means by which that result is obtained, not the meaning of the program.

Compiler optimizations may change the generated implementation of a program only to the extent permitted by this specification and without changing specified observable behavior.

Compilation Model
-----------------

The compilation model describes the conceptual processing of a Harpy translation unit. It specifies the semantic stages that a conforming implementation shall account for; it does not prescribe a particular internal compiler architecture.

A conceptual processing model is:

.. mermaid::

    flowchart TD
        A[Translation Unit] --> B[Lexical Analysis]
        B --> C[Parsing]
        C --> D[Semantic Analysis]

        D --> E[Code Generation]
        D --> X[Compile-time Execution]

        E --> F[Object Generation]
        X --> D

        F --> G[Linking]
        G --> H[Loading]
        H --> I[Execution]

An implementation may combine, reorder, repeat, or otherwise organize internal processing stages when doing so does not alter any behavior or information required by this specification.

Lexical Analysis
~~~~~~~~~~~~~~~~

Lexical analysis processes source text into tokens.

The lexical structure of Harpy, including the token categories and the information exposed through ``_harpyc``, is normative.

Malformed lexical input is represented according to the lexical error rules of this specification. Lexical processing does not itself terminate source processing merely because malformed input has been encountered; the subsequent parsing and semantic mechanisms determine the resulting diagnostic behavior.

Parsing
~~~~~~~

Parsing determines whether the token sequence conforms to the Harpy grammar.

The grammar defined in this specification is normative. Syntactic validity does not imply semantic validity.

A syntactically valid construct may subsequently be rejected during semantic analysis when its use violates a semantic rule.

Semantic Analysis
~~~~~~~~~~~~~~~~~

Semantic analysis determines the meaning and validity of the program according to the language rules.

Semantic analysis includes, as applicable, type and entity resolution, constraints, contracts, metadata, representation requirements, calling conventions, compile-time execution, fragment processing, and other compile-time semantic mechanisms defined by this specification.

Compile-time execution occurs as part of the compilation process and shall be subject to the semantic and resource restrictions defined by this specification.

The implementation may perform semantic analysis in multiple internal passes or in another organization, provided that the specified semantic result is preserved.

Code Generation
~~~~~~~~~~~~~~~

Code generation produces the target-specific representation required to implement the semantics established during compilation.

Target-specific properties may affect representation, type sizes, alignment, calling conventions, instruction selection, and assembly generation. Such properties do not alter the semantics of the Harpy language itself.

Assembly integration spans semantic processing and code generation. Assembly constructs are subject to the language rules governing their declarations, references, constraints, and target compatibility.

Object Generation
~~~~~~~~~~~~~~~~~

Object generation produces the object representation required for subsequent integration.

A conforming implementation shall generate the object information required by this specification, including the ``.metapkginfo`` information associated with packages where required.

The object and binary representations defined by this specification are normative.

Linking
~~~~~~~

Linking resolves and combines the object-level components required to construct an executable program.

Linking is a normative part of the Harpy execution model. A conforming environment shall implement the linking requirements defined by this specification, including the requirements imposed by PLDC and by external symbol resolution.

Link-time failures are part of the defined compilation process and shall not be treated as successful compilation.

Loading and Execution
~~~~~~~~~~~~~~~~~~~~~

Loading prepares the linked program for execution according to the target and binary format.

The loader and the execution behavior required by PLDC are part of the normative Harpy environment defined by this specification.

The execution model does not require a mandatory Harpy runtime. Runtime facilities may instead be provided by ordinary Harpy code, assembly, foreign code, or other components permitted by this specification.

Conformance
-----------

A conforming implementation shall implement the complete Harpy language and all implementation requirements defined by this specification.

There are no language profiles or conforming subsets. An implementation that omits a language feature or implementation requirement is not conforming.

There are no implementation-defined language semantics. Where this specification defines the meaning of a construct, all conforming implementations shall implement that meaning.

An implementation may differ internally in algorithms, data structures, optimization strategies, compilation order, resource usage, and other implementation details for which this specification does not prescribe a particular method. Such freedom shall not change any specified observable behavior.

Where this specification exposes compiler properties or operations through ``_harpyc``, those properties and operations are part of the conformance requirements of the implementation.

Program Conformance
~~~~~~~~~~~~~~~~~~~

A Harpy program is conforming when:

* its source text satisfies the lexical requirements;
* its structure satisfies the grammatical requirements;
* its semantics satisfy all applicable language rules;
* all required compile-time constraints are satisfied;
* all applicable preconditions and postconditions are satisfied; and
* all applicable target, representation, ABI, linking, and external-interface requirements are satisfied.

The use of assembly, custom calling conventions, foreign interfaces, or ``_harpyc`` does not by itself make a program non-conforming.

A program may be inherently dependent on a particular target. Such a program remains a valid Harpy program when all of its requirements are satisfied by the target for which it is compiled. Attempting to compile or execute it for an incompatible target is a failure to satisfy the applicable requirements; it does not change the language validity of the source in the abstract.

A program is not required to be portable to be conforming.

Extensions
~~~~~~~~~~

The Harpy language is closed with respect to its normative syntax and semantics.

A compiler shall not extend the Harpy language with additional keywords, metadata, operators, types, implicit conversions, calling conventions, compiler APIs, or other language constructs while claiming conformance to this specification.

An implementation may provide non-Harpy facilities outside the language, but source code relying on such facilities is not thereby part of the Harpy language and cannot be treated as conforming Harpy syntax or semantics unless the facility is defined by this specification.

Diagnostics
~~~~~~~~~~~

This specification defines diagnostic conditions and required diagnostic mechanisms but does not generally standardize diagnostic wording.

A conforming implementation shall diagnose every condition for which this specification requires a diagnostic. Implementations may differ in the wording, formatting, ordering, and presentation of diagnostics unless a specific requirement states otherwise.

A compiler option may permit a compilation process to terminate after a diagnostic when such behavior is explicitly supported. Such an option does not change the underlying semantic validity of the program.

Specification Completeness
--------------------------

This specification is a closed-world definition of Harpy.

Every language construct, semantic behavior, compiler facility, representation rule, runtime behavior, and other normative property of Harpy shall be established by this specification.

Harpy has no undefined behavior, unspecified behavior, implementation-defined language behavior, or equivalent hidden category of behavior.

If a behavior is not defined or permitted by this specification, it is not part of the Harpy language.

This rule applies to, among other things:

* syntax;
* metadata;
* operators;
* types;
* conversions;
* implicit behavior;
* compiler-visible properties;
* compile-time execution;
* object generation;
* linking;
* loading; and
* runtime behavior.

An implementation shall not assign semantics to a construct merely because it can technically implement such behavior. If an implementation accepts a construct or behavior that is outside the language defined by this specification, that construct or behavior is not conforming Harpy.

Normative Authority
~~~~~~~~~~~~~~~~~~~

Normative requirements are authoritative throughout this specification.

No chapter, section, annex, example, or table has implicit authority to override another normative requirement. The specification shall be interpreted as a logically consistent whole.

Where two normative statements appear to contradict one another, the specification is defective and shall be corrected. Such a contradiction shall not be resolved by assigning general precedence to one chapter over another.

The grammar is normative, but grammatical validity does not override semantic restrictions. A construct may therefore be grammatically valid and semantically invalid.

Examples and tables included as part of the normative specification are normative representations of the rules they express. Annexes are part of the specification and are normative unless explicitly designated otherwise.

Informative Material
~~~~~~~~~~~~~~~~~~~~

The specification may contain explanatory material intended to improve understanding.

Informative material shall be explicitly identified as informative and shall not introduce, modify, restrict, or contradict the semantics defined by normative material.

Informative material may explain the motivation, interpretation, or practical consequences of a rule, but a conforming implementation shall derive language requirements only from the normative specification.

Normative Language
~~~~~~~~~~~~~~~~~~

The following terms have the indicated normative meanings:

**shall**
   Establishes a mandatory requirement.

**shall not**
   Establishes a mandatory prohibition.

**may**
   Permits an implementation or program to perform or use the specified behavior without requiring it.

**should**
   Is reserved for informative guidance and does not establish a language requirement.

Unless explicitly stated otherwise, normative requirements apply to all conforming implementations.

Absence of Permission
~~~~~~~~~~~~~~~~~~~~~

The absence of a rule permitting a construct or behavior means that the construct or behavior is not part of Harpy.

An implementation may not infer additional language semantics from analogy with another programming language, from common compiler practice, from hardware capabilities, or from behavior of another Harpy implementation.

Implementation freedom exists only where this specification permits it. Such freedom concerns implementation technique and does not create implementation-defined language behavior.

Versioning
~~~~~~~~~~

Harpy defines both a language version and a specification version.

Breaking language changes may be introduced only through the versioning and deprecation mechanisms defined by this specification. A feature subject to deprecation remains valid during its specified deprecation period and may subsequently be removed according to the applicable versioning rules.

A conforming compiler may support multiple Harpy language versions simultaneously.

A program written for an earlier language version is not required to compile unchanged under a later language version unless compatibility is explicitly specified. The language version targeted by a compilation is observable through the compiler facilities defined by this specification.

The absence of a language-version declaration in source code does not remove the versioning requirements imposed on the compilation environment.

Completeness Requirement
~~~~~~~~~~~~~~~~~~~~~~~~

The requirements of this specification are intended to be sufficient for an independent implementation.

A conforming implementation shall not require knowledge of undocumented behavior of another implementation to determine the meaning of a conforming Harpy program.

Where the specification intentionally leaves an implementation detail unconstrained, that freedom is an implementation choice rather than an additional language semantic category.

The specification therefore defines the semantics of Harpy without relying on undefined, unspecified, or implementation-defined behavior.
