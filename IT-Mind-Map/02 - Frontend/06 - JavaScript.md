---
title: "JavaScript"
area: "Frontend"
numero: 6
aliases: ["JavaScript"]
tags: [concepto, it/frontend]
---
# JavaScript

> **Área:** [[02 - Frontend/00 - Índice Frontend|Índice Frontend]] · **Concepto 6 de 25**

## Qué abarca
- Sintaxis
- tipos
- funciones
- objetos
- arrays

## Mis notas
<!-- ai:start -->
# Modern JavaScript Fundamentals & Architecture: Comprehensive Study Guide

This study guide provides a detailed synthesis of core JavaScript mechanisms, memory models, execution contexts, variable lifecycles, object-oriented semantics, and collection operations based on the ECMAScript specifications and standard developer reference materials.
<!-- ai:end -->

---

## 1. Key Concepts Review

### 1.1 Execution Contexts, Lexical Environments, and Closures

The execution of JavaScript code is managed through **Execution Contexts**, which abstract the internal environment in which code evaluation and execution take place. An execution context consists of three core components:
1. **Variable Environment:** Stores local variable bindings and hoisted declarations.
2. **Lexical Environment:** Tracks identifier-to-value associations based on the physical position of code in the source file.
3. **This Binding (`this`):** Determines the context object bound to the current execution frame.

#### Lexical Environments and Scope Chains
A **Lexical Environment** contains:
* An **Environment Record**, which stores local identifier bindings.
* A reference to an **Outer Lexical Environment** (outer scope).

This nested structure creates the **Scope Chain**. When resolving a variable identifier, the engine conducts a linear search starting from the local Environment Record and moving upward through the chain of outer environments until it reaches the Global Environment.

#### Execution Context vs. Closure
While related, execution contexts and closures serve distinct runtime roles:
* **Closure:** A function paired with a reference to the Lexical Environment in which it was declared. Closures preserve access to outer variables even after the outer function's execution context has finished executing and has been popped off the Call Stack.
* **Execution Context:** The dynamic environment created *when* a function is invoked to manage its execution.

```
+-------------------------------------------------------------------+
| Closures  ==> Functions that retain their lexical creation context |
| Execution ==> Environment created at runtime during invocation    |
+-------------------------------------------------------------------+
```

Because a closure holds a direct reference to its outer lexical environment record, the **Garbage Collector** cannot free the variables within that outer scope as long as an active reference to the closure exists in the application.

---

### 1.2 Variable Lifecycles, Scope, and Global Resolution

JavaScript enforces strict rules regarding how variables are declared, hoisted, and scoped across block and function boundaries.

#### Variable Declaration Comparison

| Feature / Criterion | `var` | `let` | `const` |
| :--- | :--- | :--- | :--- |
| **Scope Type** | Function or Global | Block (`{ ... }`) | Block (`{ ... }`) |
| **Hoisting Behavior** | Hoisted and initialized to `undefined` | Hoisted into Temporal Dead Zone (TDZ) | Hoisted into Temporal Dead Zone (TDZ) |
| **Reassignment** | Allowed | Allowed | Prohibited (`TypeError`) |
| **Redeclaration in Same Scope** | Allowed | Prohibited (`SyntaxError`) | Prohibited (`SyntaxError`) |
| **Global Object Property Creation** | Yes (in non-strict global scope) | No | No |

#### The Temporal Dead Zone (TDZ)
Variables declared with `let` and `const` are hoisted during the compilation phase, but they remain uninitialized in the **Temporal Dead Zone (TDZ)**. Accessing a `let` or `const` variable before its explicit declaration line results in a `ReferenceError`.

#### Unified Global Resolution via `globalThis`
Historically, accessing the global object required platform-specific code (`window` or `self` in browsers, `self` in Web Workers, `global` in Node.js). 

The `globalThis` standard provides a unified global reference across all execution environments:
* In web browsers, `globalThis` returns a security proxy called **`WindowProxy`** rather than pointing directly to the underlying global window object to protect cross-iframe contexts.

---

### 1.3 Primitive Types, Precision Limits, and Equality Algorithms

JavaScript separates data types into **Primitives** (immutable values) and **Reference Types** (objects, arrays, functions, collections stored in the heap).

#### Primitives vs. Reference Types
* **Primitives:** `Number`, `BigInt`, `String`, `Boolean`, `Symbol`, `Undefined`, and `Null`. Operations on primitives produce new primitive values rather than mutating existing ones.
* **Reference Types:** Stored in heap memory and accessed via memory addresses.

#### Number vs. BigInt Operations
* **`Number` Limits:** Uses IEEE 754 double-precision floating-point format. Safe integer operations are restricted to the range $-(2^{53} - 1)$ through $2^{53} - 1$ (`Number.MAX_SAFE_INTEGER`). Arithmetic outside this range causes precision loss.
* **`BigInt`:** Represents arbitrary-precision integers. Created by appending `n` to an integer literal or invoking `BigInt()`.

##### Operating Rules for `BigInt`:
1. **No Implicit Mixing:** Direct arithmetic mixing of `Number` and `BigInt` operands throws a `TypeError`. Explicit type conversion is required.
2. **Truncating Division:** Division involving `BigInt` truncates fractional components toward zero (e.g., `5n / 2n === 2n`).
3. **Math Object Compatibility:** Built-in methods under the `Math` object do not accept `BigInt` instances.
4. **JSON Serialization:** `JSON.stringify()` throws a `TypeError` when encountering a `BigInt` unless a custom `toJSON()` method or custom replacer function is supplied.

#### Equality Comparison Algorithms

| Operation / Input Pair | Loose Equality (`==`) | Strict Equality (`===`) | Algorithm `Object.is()` |
| :--- | :--- | :--- | :--- |
| `42 == "42"` | `true` (coerced to number) | `false` | `false` |
| `null == undefined` | `true` | `false` | `false` |
| `NaN` vs. `NaN` | `false` | `false` | `true` |
| `0` vs. `-0` | `true` | `true` | `false` |
| `{a:1}` vs. `{a:1}` | `false` (different references) | `false` (different references) | `false` (different references) |

---

### 1.4 Object Mechanics, Prototype Delegation, and Deep Cloning

#### Prototype Chain Delegation
JavaScript uses prototype-based inheritance. Every object contains an internal, hidden property named `[[Prototype]]` referencing another object or `null`. If a property is requested that does not exist directly on the instance, the engine traverses up the **Prototype Chain** until the property is found or `null` is reached (`Object.prototype.[[Prototype]] === null`).

#### Native Private Class Fields (`#`)
Modern ECMAScript classes support native private members using the `#` prefix on fields, methods, getters, and setters.
* **Hard Encapsulation:** Private fields are enforced by the virtual machine and cannot be accessed or inspected via external reflection utilities (`Object.keys()`, `for...in`, `Object.getOwnPropertyNames()`).
* **Immutability Protection:** Metaprogramming methods like `Object.freeze()` or `Object.seal()` do not alter the mutability of `#` private fields.

#### Object Grouping Utilities

| Feature | `Object.groupBy()` | `Map.groupBy()` |
| :--- | :--- | :--- |
| **Returned Key Types** | Strings or Symbols (implicit coercion) | Any data type (objects, primitives) |
| **Output Data Structure** | Null-prototype plain object (`Object.create(null)`) | A standard `Map` instance |
| **Primary Use Case** | Strings/text-based categorizations | Complex or object-reference grouping keys |

#### Deep Cloning via `structuredClone()`
While shallow copying (`...` spread operator or `Object.assign()`) copies top-level references, `structuredClone()` utilizes the Structured Clone Algorithm to recursively copy complex objects, correctly handling circular references and Transferable Objects.

##### Limitations of `structuredClone()`:
* Throws `DataCloneError` or `TypeError` if tasked with cloning **functions**, **DOM nodes**, or property descriptors with accessors (`getters`/`setters`).
* Strips the object's prototype chain, converting instances to plain objects or standard built-in types.
* Does not copy class private `#` fields.

---

### 1.5 Array Architecture, Inmutability, and Sets

JavaScript arrays are resizable, zero-indexed collections indexed by non-negative integers.

#### Sparse Arrays and Empty Slots
Arrays can contain "empty slots" (sparse arrays), created when setting indices beyond current bounds or increasing the `length` property directly.
* **Legacy Methods (`forEach`, `map`, `filter`, `concat`):** Skip empty slots during iteration or preserve empty slots in output copies.
* **Modern Methods (`keys`, `values`, `entries`, `find`, `includes`, `toSorted`, `toReversed`, `toSpliced`, `with`):** Treat empty slots as if they contain `undefined`.

#### ES2023 Non-Destructive Array Methods

| Mutating (Destructive) Method | Non-Mutating Copy Alternative | Description |
| :--- | :--- | :--- |
| `Array.prototype.reverse()` | `Array.prototype.toReversed()` | Returns a reversed copy of the array. |
| `Array.prototype.sort()` | `Array.prototype.toSorted()` | Returns a sorted copy of the array. |
| `Array.prototype.splice()` | `Array.prototype.toSpliced()` | Returns a copy with elements removed/replaced. |
| Direct assignment (`arr[i] = v`) | `Array.prototype.with(i, v)` | Returns a copy with index `i` set to value `v`. |

#### ES2024 Native Set Operations
ES2024 introduced native methods to `Set.prototype` for set theory operations, including `intersection()`, `union()`, `difference()`, and `symmetricDifference()`.

* **Performance Optimization:** In `setA.intersection(setB)`, if `setA` is larger than `setB`, the engine optimizes performance by iterating internally over the smaller set (`setB`) and performing sublinear $O(1)$ lookup checks (`.has()`) against the larger set (`setA`).

---

## 2. Short-Answer Practice Questions

**Question 1: Explain the difference between variable hoisting with `var` and variable hoisting with `let` / `const`.**  
*Answer:* Both `var` and `let`/`const` are hoisted during compilation. However, `var` variables are immediately initialized with the value `undefined`, making them accessible before their declaration line. `let` and `const` remain uninitialized inside the Temporal Dead Zone (TDZ); accessing them before explicit declaration throws a `ReferenceError`.

**Question 2: What happens when an arithmetic operation attempts to mix a `BigInt` and a standard `Number`?**  
*Answer:* JavaScript throws an explicit `TypeError`. The engine prohibits implicit type coercion between `BigInt` and `Number` in arithmetic operations to prevent unintended precision loss.

**Question 3: How does `Object.is()` differ from strict equality (`===`) when comparing `NaN` values and signed zeroes (`0` and `-0`)?**  
*Answer:* Strict equality (`===`) evaluates `NaN === NaN` as `false` and `0 === -0` as `true`. In contrast, `Object.is()` follows the SameValue algorithm, evaluating `Object.is(NaN, NaN)` as `true` and `Object.is(0, -0)` as `false`.

**Question 4: Why does a closure prevent garbage collection of variables defined in an outer function that has already returned?**  
*Answer:* A closure maintains a persistent direct reference to the Lexical Environment Record in which it was defined. Because this reference path remains active on the closure object, the Garbage Collector cannot reclaim memory used by the outer environment's bound variables.

**Question 5: What occurs when `structuredClone()` is called on an object that contains a function or a DOM node?**  
*Answer:* The execution fails immediately, throwing a `DataCloneError` or `TypeError`, as functions and DOM nodes cannot be processed by the Structured Clone Algorithm.

**Question 6: How do legacy array methods (e.g., `forEach`) and modern array methods (e.g., `find` or `toSorted`) differ in their handling of empty slots in sparse arrays?**  
*Answer:* Legacy methods skip empty slots during iteration without calling the callback function. Modern methods do not skip empty slots; instead, they treat empty slots as if they hold the value `undefined`.

**Question 7: What is the main structural difference between the output of `Object.groupBy()` and `Map.groupBy()`?**  
*Answer:* `Object.groupBy()` returns a plain, null-prototype object where keys are implicitly coerced to strings or symbols. `Map.groupBy()` returns an instance of `Map`, allowing keys of any type, including arbitrary objects.

**Question 8: Why is `JSON.stringify()` unable to serialize `BigInt` values by default?**  
*Answer:* The standard JSON specification lacks a native data type representation for arbitrary-precision integers. Calling `JSON.stringify()` on a `BigInt` throws a `TypeError` unless a custom `toJSON()` method or a replacer parameter is provided.

---

## 3. Essay Prompts for Deeper Exploration

### Prompt 1: The Architecture of Execution Contexts, Memory Reclamation, and Closures
Deconstruct the step-by-step process that occurs when an outer function creates and returns an inner function that references local variables. Detail the lifecycle of the Call Stack, the setup of the Lexical Environment, the role of Environment Records, and how closure retention impacts Garbage Collection. Compare this with traditional function contexts that do not return closures.

### Prompt 2: Immutability Paradigms in Modern JavaScript: ES2023 Arrays, `structuredClone`, and Native Class Encapsulation
Analyze how modern ECMAScript specifications have moved toward data immutability and hard encapsulation. Evaluate the performance, safety, and operational trade-offs of using non-destructive array methods (`toSorted`, `toSpliced`, `with`) versus shallow copying via spread operators. Integrate a critique of class `#` private fields, explaining how engine-level private fields change object encapsulation compared to historical conventions or closure-based privacy.

### Prompt 3: The JavaScript Type System: Precision Boundaries, Coercion Traps, and Identity Verification
Discuss the computational structure of primitive vs. reference types in JavaScript. Focus on the mathematical and runtime differences between IEEE 754 floating-point `Number` structures and arbitrary-precision `BigInt` primitives. Explain the hazards of type coercion in equality comparisons (`==`), explicit type conversions, and JSON payloads, defending why `Object.is()` and strict non-coercing logic are necessary in enterprise applications.

---

## 4. Glossary of Important Terms

* **`BigInt`:** A primitive numerical data type capable of representing arbitrary-precision integers beyond the safe integer boundary of the standard `Number` type ($2^{53} - 1$).
* **Block Scope:** A variable visibility boundary delimited by curly braces (`{ ... }`), enforced by `let` and `const` declarations.
* **Call Stack:** A LIFO (Last-In, First-Out) stack data structure used by the JavaScript engine to track current function execution frames and execution contexts.
* **Closure:** The combination of a function bundled together with references to its surrounding Lexical Environment, allowing access to outer variables after the outer context ends.
* **Environment Record:** An internal component of a Lexical Environment that stores local variable bindings, function declarations, and parameter values.
* **Execution Context:** An internal structure that holds the execution state, scope chain, variable environments, and `this` binding for currently executing code.
* **`globalThis`:** A standardized global property providing access to the global scope object regardless of whether code is running in a browser, worker, or server environment.
* **Hoisting:** The process during the compilation phase in which variable and function declarations are recorded in memory before code execution begins.
* **Lexical Environment:** An internal data structure that binds identifier names to variable values based on physical lexical placement in the source code.
* **`Number.MAX_SAFE_INTEGER`:** The maximum safe double-precision floating-point integer representable in JavaScript without precision loss ($2^{53} - 1$, or $9,007,199,254,740,991$).
* **`Object.is()`:** A static method that compares two values using the SameValue algorithm, accurately distinguishing `-0` from `0` and recognizing `NaN` as equal to `NaN`.
* **Private Class Fields (`#`):** Engine-enforced private field syntax that renders class properties entirely inaccessible from outside the class instance.
* **Prototype Chain:** A series of linked objects connected via internal `[[Prototype]]` properties, facilitating property delegation and method inheritance.
* **Scope Chain:** A chain of nested Lexical Environments searched linearly by the engine during identifier resolution.
* **Sparse Array:** An array containing unallocated indices or "empty slots," behaving differently depending on whether legacy or modern array methods process it.
* **`structuredClone()`:** A global API that uses the Structured Clone Algorithm to perform deep copies of values, handling circular references and transferable memory structures.
* **Temporal Dead Zone (TDZ):** The execution window between the entering of a block scope and the explicit line where a `let` or `const` variable is declared, during which variable access throws a `ReferenceError`.
* **`WindowProxy`:** A security wrapper object returned when referencing global scope objects within browser contexts to prevent illegal cross-origin access between frames.

## Relacionados
- [[02 - Frontend/07 - JavaScript avanzado|JavaScript avanzado]]
- [[02 - Frontend/08 - Eventos|Eventos]]
- [[02 - Frontend/09 - Asincronía|Asincronía]]

---
← [[02 - Frontend/05 - DOM|DOM]] · [[02 - Frontend/00 - Índice Frontend|Índice Frontend]] · [[02 - Frontend/07 - JavaScript avanzado|JavaScript avanzado]] →
