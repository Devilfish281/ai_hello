# Product Requirements Document (PRD)

## Product

AI Hello

## Version

v0.1 (Learning Project)

## Date

2026-05-06

## 1. Overview

AI Hello is a small Python learning project designed to teach modular design through a simple greeting workflow. The product demonstrates how to build software using clear interfaces, hidden implementations, and testable seams.

The current module in focus is `hello_world`, which exposes a minimal public interface for setting a name and producing a greeting.

## 2. Problem Statement

Beginner projects often mix calling code and implementation details, making it hard to learn abstraction, testing, and maintainability. This project solves that by requiring callers to use explicit interface functions and by keeping module internals local.

## 3. Goals

1. Teach interface-first module design in Python.
2. Demonstrate depth and leverage via a tiny but meaningful API.
3. Ensure behavior is verified through pytest.
4. Preserve naming consistency for interface functions.
5. Keep implementation simple and easy to refactor.

## 4. Non-Goals

1. Build a production chatbot or full AI assistant.
2. Add network services, database storage, or web UI.
3. Introduce advanced dependency injection frameworks.
4. Support multilingual greeting logic in v0.1.

## 5. Target Users

1. Learners studying Python modules and architecture basics.
2. Instructors using small examples to teach seams and adapters.
3. Contributors practicing TDD and incremental refactoring.

## 6. Product Scope

### In Scope (v0.1)

1. `hello_world` module with public interface:
   - `i_hello_world_name_set(name: str) -> None`
   - `i_hello_world_greet() -> None`
2. Deterministic greeting behavior:
   - If no name is set, output `Hello World`.
   - If a name is set, output `Hello <name>`.
3. Entry point that calls interface functions.
4. Pytest coverage for default and named greeting paths.

### Out of Scope (v0.1)

1. Persistence across process restarts.
2. Input validation beyond basic runtime behavior.
3. CLI argument parsing.
4. Integration with real AI model providers.

## 7. Functional Requirements

1. The module must expose interface functions using the pattern `i_<module>_<action>`.
2. Calling code must interact only through public interface functions.
3. `i_hello_world_name_set` must store a name used by subsequent greetings in the same process.
4. `i_hello_world_greet` must print exactly one line ending with a newline.
5. If no name is set, `i_hello_world_greet` must print `Hello World`.
6. If a name is set to `Mark`, `i_hello_world_greet` must print `Hello Mark`.

## 8. Non-Functional Requirements

1. Runtime environment: Python 3.12+.
2. Test framework: pytest.
3. Package/dependency management: Poetry.
4. Code organization must preserve locality (module concerns remain in module).
5. Public interface names must remain stable unless explicitly changed by requirement.

## 9. Architecture and Design Principles

1. Module: Any unit with interface and implementation.
2. Interface: What callers must know to use the module.
3. Implementation: Hidden internals behind the interface.
4. Seam: Boundary where callers cross into the module.
5. Adapter: Concrete implementation used at a seam.
6. Depth: Useful behavior hidden behind a small interface.
7. Leverage: Simpler caller code because of module depth.
8. Locality: Easier maintenance due to confined implementation details.

## 10. User Stories

1. As a learner, I want to call a clearly named interface function so I can understand where module boundaries are.
2. As a learner, I want default greeting behavior so I can see predictable output before setting state.
3. As a learner, I want to set a name and get personalized output so I can verify stateful behavior.
4. As a maintainer, I want tests for both paths so I can refactor internals safely.

## 11. Acceptance Criteria

1. Running tests passes for:
   - default greeting without name set
   - greeting after setting name to `Mark`
2. Main entry point executes without errors and outputs expected greeting text.
3. Public interface functions remain available with current names.
4. No caller relies on private module internals.

## 12. Success Metrics

1. 100% pass rate on defined module behavior tests.
2. New contributors can explain module interface and seam in under 5 minutes.
3. Changes to internal implementation require no caller changes when interface remains stable.

## 13. Risks and Mitigations

1. Risk: Global module state can leak between tests.
   - Mitigation: Reload module state in tests before each scenario.
2. Risk: Contributors bypass interface and use internals directly.
   - Mitigation: Document interface-only usage and enforce through review.
3. Risk: Scope creep into unrelated AI features.
   - Mitigation: Keep v0.1 scope small and explicit.

## 14. Milestones

1. Milestone 1: Establish stable `hello_world` interface and implementation.
2. Milestone 2: Add and pass baseline pytest coverage.
3. Milestone 3: Document architecture vocabulary and conventions.
4. Milestone 4: Prepare next tracer-bullet issue for an additional module seam.

## 15. Future Considerations (Post-v0.1)

1. Add a seam for configurable output adapter (stdout, logger, or collector).
2. Add input sanitization/validation behavior and tests.
3. Add CLI adapter while preserving module interface boundaries.
4. Introduce additional modules following the same naming and depth principles.
