# Mackerel Architecture

## Introduction

- Minimize third party dependencies
- Strongly typed
    - Dataclasses instead of tuples / dicts
    - Algebraic data types with union types
    - Encoding invariants using types
    - Pattern matching
    - New types even for primitives
    - Protocols

## Components

## Plugins

## Workflows

### Development

### Release


## Resources

- https://kobzol.github.io/rust/python/2023/05/20/writing-python-like-its-rust.html
- https://github.com/kbilsted/Functional-core-imperative-shell
- https://github.com/kenneth-lange/ts-functional-core-imperative-shell

Protocol naming conventions generally use nouns, adjectives ending in "-ing", or nouns with "-able" or "-ible" suffixes, depending on the protocol's purpose. For protocols describing what something is, nouns are used (e.g., Collection). If the protocol describes a capability, it should use "-ing" (e.g., Loading) or "-able"/"-ible" (e.g., Equatable). When a protocol is used in a delegate or data source pattern, the class name of the conforming object is appended (e.g., DataSource, Delegate).
Elaboration:

Here's a more detailed breakdown of naming conventions for protocols:
1. Protocols Describing "What Something Is":

    Use nouns to represent the concept the protocol embodies.
    Examples: Collection, Sequence, View, Repository.

2. Protocols Describing Capabilities or Actions:

    "Something is doing something":
    Use adjectives ending in "-ing".
        Examples: Loading, Generating, Coordinating.
    "Something is done to something":
    Use adjectives ending in "-able" or "-ible".
        Examples: Equatable, Codable, Cacheable, Comparable.

3. Protocols used in Delegate or Data Source Patterns:

    Append Delegate or DataSource to the class name of the conforming object.
    Example: UITextFieldDelegate, UITableViewDataSource.

4. General Tips:

    Avoid names that are too generic or only describe a function signature or property type.

The name should add value that isn't already implied by other code elements.
Consider using meaningful prefixes or suffixes if they improve clarity, but avoid unnecessary prefixes.
Be consistent with your naming conventions within a project.
Use clear and descriptive names that are easy to understand.
