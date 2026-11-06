---
title: "DOM"
area: "Frontend"
numero: 5
aliases: ["DOM"]
tags: [concepto, it/frontend]
---
# DOM

> **Área:** [[02 - Frontend/00 - Índice Frontend|Índice Frontend]] · **Concepto 5 de 25**

## Qué abarca
- Árbol de documentos
- nodos
- manipulación

## Mis notas
<!-- ai:start -->
<!-- ai:end -->

---

## Key Concepts & Detailed Technical Review

### 1. DOM Hierarchy, Specification Standards, and Engine Architecture

#### WHATWG DOM Specification and Interface Inheritance
The Document Object Model (DOM) is a platform-neutral API defining the memory representation of structured documents (HTML/XML) and event handling mechanisms. Under the **WHATWG DOM Living Standard**, the document is modeled as a tree of logical objects derived from a unified inheritance chain:

*   **`EventTarget`**: The root interface of the object hierarchy. It provides event handling abilities (`addEventListener`, `removeEventListener`, `dispatchEvent`).
*   **`Node`**: Abstract base class inheriting directly from `EventTarget`. Defines tree traversal properties (`parentNode`, `childNodes`, `nextSibling`) and basic structural mutation methods (`appendChild`, `removeChild`).
*   **`Document`**: Represents the root node of the entire document residing in memory. Serves as the primary factory for creating new nodes.
*   **`Element`**: Extends `Node` to represent structural XML/HTML elements (`<div>`, `<p>`). Handles attributes, class names, geometrical metadata, and CSS selector matching.
*   **`CharacterData`**: Abstract interface extending `Node` for text-containing objects. It concrete implementations include:
    *   `Text`: Plain text content nodes inside elements.
    *   `Comment`: Represents HTML/XML comment structures (`<!-- comment -->`).
    *   `CDATASection`: Represents unparsed text blocks in XML documents.
*   **`DocumentFragment`**: A lightweight, abstract sub-tree container detached from the primary document tree. Operations performed within a `DocumentFragment` do not trigger layout recalculations or browser reflows.

#### Node Types and the DOM4 Specification Shift
The `Node.nodeType` property returns an integer value representing the specific interface type of a node. Historical standards (DOM Levels 1–3) defined 12 node constants. The DOM4 standard and WHATWG Living Standard marked several types as **deprecated** to reduce engine memory overhead and streamline tree traversal algorithms:

| Integer Value | Type Constant Identifier | Specification Status | Description |
| :--- | :--- | :--- | :--- |
| **1** | `Node.ELEMENT_NODE` | Active | Structural HTML or XML element nodes. |
| **2** | `Node.ATTRIBUTE_NODE` | Deprecado (DOM4) | Attribute objects. Removed from direct tree child status; now stored as key-value metadata maps on `Element`. |
| **3** | `Node.TEXT_NODE` | Active | Direct textual content within elements or attributes. |
| **4** | `Node.CDATA_SECTION_NODE` | Deprecado | XML CDATA text blocks. |
| **5** | `Node.ENTITY_REFERENCE_NODE` | Deprecado | Historic XML entity references. |
| **6** | `Node.ENTITY_NODE` | Deprecado | DTD XML entity definitions. |
| **7** | `Node.PROCESSING_INSTRUCTION_NODE` | Active | Processing instructions (e.g., XML stylesheet directives). |
| **8** | `Node.COMMENT_NODE` | Active | Comments in source markup. |
| **9** | `Node.DOCUMENT_NODE` | Active | Root object representing the document (`document`). |
| **10** | `Node.DOCUMENT_TYPE_NODE` | Active | Doctype declaration node (`<!DOCTYPE html>`). |
| **11** | `Node.DOCUMENT_FRAGMENT_NODE` | Active | Lightweight detached subtree root container. |
| **12** | `Node.NOTATION_NODE` | Deprecado | Notation definitions in XML DTDs. |

#### Engine Implementation Case Study: Lexbor DOM Architecture
Low-level web engines (e.g., `Lexbor`) demonstrate optimized DOM structures designed in C:
*   **First-Field Embedding Pattern ("Poor Man's Inheritance")**: Structs are nested such that the parent struct (`lxb_dom_node_t`) is always the first member of a child struct (`lxb_dom_element_t`). This permits zero-cost interface type-casting between types without memory conversion overhead.
*   **Two-Pool Memory Allocation Architecture**:
    *   `mraw` (Structure Pool): Allocates fixed-size node structures (`lxb_dom_element_t`, `lxb_dom_attr_t`).
    *   `text` (Text Pool): Allocates variable-length string data (attribute values, text content).
    *   *Cleanup Strategy*: Destroying a document (`lxb_html_document_destroy`) instantly reclaims both memory pools at once without necessitating manual node-by-node deallocations.
*   **Tag Name and Namespace Memory Optimization (`uintptr_t`)**:
    *   Properties like `local_name`, `prefix`, and `ns` use `uintptr_t` to store either a small integer ID or a heap memory pointer.
    *   Predefined compile-time tags (e.g., `LXB_TAG_DIV = 0x0033`) are stored directly as small integers up to a threshold (`LXB_TAG__LAST_ENTRY = 0x00c6`).
    *   Custom or unknown tags higher than this threshold are evaluated directly as pointers to entries in a global tag hash table, eliminating hash lookup overhead for standard HTML tags.

#### Node State and Equality Semantics
*   `isConnected`: Boolean property returning `true` if a node is currently connected directly or indirectly to the global `Document` context.
*   `isSameNode(otherNode)`: Evaluates **reference identity** (verifying if both variables point to the exact same object address in memory).
*   `isEqualNode(otherNode)`: Evaluates **deep structural equality** (verifying if two nodes share identical node types, attributes, data, and identical child hierarchies, even if they occupy separate memory addresses).

---

### 2. Tree Traversal, Manipulation, and Rendering Performance

#### Navigation and Collections
*   **Live Collections** (`childNodes`, `getElementsByTagName`): Dynamic arrays reflecting real-time structural changes in the DOM tree. Mutating the DOM while iterating over a live collection dynamically alters its `.length`, which can result in infinite loops if index counters are not carefully managed.
*   **Static Snapshots** (`querySelectorAll`): Immutably scoped `NodeList` collections captured at the exact moment of execution. DOM mutations do not alter the size or order of static lists during iteration.

#### Structural Mutation Methods Comparison

| Operation | Traditional `Node` Interface Methods | Modern `ChildNode` / `Element` Methods | Technical Advantages of Modern Methods |
| :--- | :--- | :--- | :--- |
| **Append** | `parentNode.appendChild(node)` | `element.append(...nodesOrStrings)` | Accepts multiple arguments; automatically converts raw string arguments into `Text` nodes. |
| **Prepend** | `parentNode.insertBefore(node, parentNode.firstChild)` | `element.prepend(...nodesOrStrings)` | Direct positional entry without requiring access to the first child pointer. |
| **Insert Before** | `parentNode.insertBefore(node, referenceNode)` | `referenceNode.before(...nodesOrStrings)` | Invoked directly on the target reference node without referencing the parent node. |
| **Insert After** | `parentNode.insertBefore(node, referenceNode.nextSibling)` | `referenceNode.after(...nodesOrStrings)` | Handles insertions safely without throwing errors when `nextSibling` returns `null`. |
| **Replace** | `parentNode.replaceChild(newNode, oldNode)` | `oldNode.replaceWith(...nodesOrStrings)` | Direct substitution interface on the target object. |
| **Remove** | `node.parentNode.removeChild(node)` | `node.remove()` | Direct node self-removal without requiring explicit parent references. |

#### Positional HTML Parsing APIs
To avoid the CPU costs of `innerHTML` (which destroys, re-parses, and replaces all child nodes of a target element, detaching registered event listeners), engines provide positional insertion methods:
*   `insertAdjacentHTML(position, string)`: Parses the markup string into nodes and injects them directly into one of four relative positions:
    *   `'beforebegin'`: Immediately before the element itself as a preceding sibling.
    *   `'afterbegin'`: Inside the element, before its first child node.
    *   `'beforeend'`: Inside the element, after its last child node.
    *   `'afterend'`: Immediately after the element as a following sibling.
*   `insertAdjacentElement(position, element)`: Injects an existing `Element` object directly into the defined position.

#### The Critical Rendering Path and Performance Bottlenecks
1.  **Render Tree Construction**: The engine combines the logical **DOM** and style **CSSOM** trees. Subtrees styled with `display: none` are omitted from the Render Tree.
2.  **Layout (Reflow)**: Computes the precise visual geometry, pixel dimensions, and spatial position of every rendered element.
3.  **Paint (Repaint)**: Rasterizes visual properties (`color`, `background-color`, `shadows`) onto bitmapped render layers without altering element geometry.
4.  **Compositing**: Draws rasterized layers to the display via GPU processing.

#### Forced Synchronous Layout and Layout Thrashing
Browsers attempt to queue DOM writes in a pending buffer, executing reflow operations asynchronously during the next frame tick. 
*   **Forced Synchronous Layout**: Occurs when JavaScript reads a calculated geometrical property (such as `offsetWidth`, `clientHeight`, `scrollTop`, `getBoundingClientRect()`, or `window.getComputedStyle()`) *immediately after* writing structural or style updates to the DOM. This forces the browser to flush the write queue synchronously to re-calculate layout geometry in real time.
*   **Layout Thrashing**: Caused by interleaving geometric DOM writes and reads inside a loop. The browser is forced to recalculate element layout repeatedly per iteration, dropping frame rates dramatically.
*   *Mitigation Strategy*: Batch all layout reading operations together first, and defer structural writes using `requestAnimationFrame()`.

---

### 3. Native Observer APIs and Wrapper Design Strategies

Browsers provide three asynchronous observation APIs to replace resource-heavy polling routines and deprecated synchronous events (e.g., `MutationEvents`).

#### 1. MutationObserver
Monitors structural tree changes, attribute modifications, and character data edits. Callbacks execute asynchronously within the browser's **Microtask Queue** immediately before rendering repaints.

*Configuration Flags*:
*   `subtree`: Expands observation to all descendant nodes.
*   `childList`: Tracks additions and removals of immediate child nodes.
*   `attributes`: Monitors changes to element attribute values.
*   `attributeFilter`: An array of specific attribute names to observe.
*   `attributeOldValue`: Captures the previous value of modified attributes.
*   `characterData`: Tracks textual changes inside `Text` nodes.
*   `characterDataOldValue`: Captures previous textual content.

#### 2. IntersectionObserver
Asynchronously tracks the visibility ratio and geometric bounding intersection of a target element relative to a parent root container or the viewport. Executes during the layout analysis phase without forcing synchronous layout recalculations.

*Configuration Flags*:
*   `root`: The boundary box element used to evaluate visibility (defaults to top-level viewport if `null`).
*   `rootMargin`: Offsets applied to the root boundary box (e.g., `"0px 0px 200px 0px"`).
*   `threshold`: Array of percentage intersection thresholds (e.g., `[0.0, 0.5, 1.0]`) triggering execution.

#### 3. ResizeObserver
Monitors physical content-box or border-box geometry changes of individual elements independently of global viewport changes.
*   *Infinite Loop Prevention*: Modifying an observed element's dimensions inside its own callback can trigger infinite updates. The browser prevents crashes by deferring notifications for elements deeper in the DOM hierarchy to the next frame tick, outputting the error: `"ResizeObserver loop completed with undelivered notifications"`.

#### Native Observer Functionality Comparison

| API Interface | Monitored Targets | Execution Mechanism | Key Configuration Options | Primary Practical Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| **MutationObserver** | DOM structure additions/deletions, attributes, text nodes. | Microtask queue prior to browser repaint. | `childList`, `attributes`, `subtree`, `characterData`, `attributeFilter`. | External script monitoring, UI state persistence, reactive DOM framework engines. |
| **IntersectionObserver** | Spatial intersection relative to root container or viewport. | Asynchronous during layout evaluation. | `root`, `rootMargin`, `threshold`. | Image/component lazy loading, infinite scrolling lists, ad impression analytics. |
| **ResizeObserver** | Geometric box dimensions (`content-box`, `border-box`). | Asynchronous post-layout before repaint. | `box` (`content-box`, `border-box`, `device-pixel-content-box`). | Responsive component layout (software container queries), dynamic canvas/chart sizing. |

#### Refactoring Native Observers: Utility Wrapper Patterns
Native observer APIs require repetitive instantiation, explicit parameter passing, and entry loop iteration. Modern abstraction designs (e.g., utilities in *Splendid Labz*) wrap native APIs into streamlined functional utilities supporting both callback and custom event patterns.

##### Key Architecture of the Refactored API
*   **Unified Interface Setup**: Combines observer creation, options passing, target element registration, and teardown logic into single multi-pattern function calls (`mutationObserver`, `intersectionObserver`, `resizeObserver`).
*   **Dual Handlers**: Automatically dispatches a `CustomEvent` (e.g., `mutate`, `intersect`) on target nodes if no direct inline callback option is provided.
*   **Safe Teardown via `takeRecords()`**: To prevent dropping unhandled mutation or intersection entries when disconnecting observers, wrapped `disconnect()` implementations extract unprocessed records using `observer.takeRecords()` and process them through the execution callback *before* calling `observer.disconnect()`.
*   **Multi-Element Batch Operations**: Wrappers extend support to observe or unobserve `NodeList` arrays simultaneously.

##### Architectural Perspective: FP Wrappers vs. Class Inheritance
*   **Functional Wrapping Pattern**: Simplifies boilerplate code, provides convenient event-listening abstractions, and exposes unified clean return structures (`{ disconnect, unobserve, takeRecords }`).
*   **Object-Oriented Subclassing (OOP Pattern)**: Supported by developers who argue that native browser observer APIs are already robust. Extending native classes directly and overriding internal handler loops (using declarative `observe:${type}` hooks or switch tables) leverages standard JS/TS subclassing patterns without adding functional layer abstractions.

---

### 4. Event Mechanics, Propagation, and Abort Architecture

#### Event Propagation Phases
Events dispatched to nodes participating in a DOM tree proceed through three sequential phases:
1.  **`CAPTURING_PHASE` (Numeric Value: 1)**: The event propagates downward from the top-level `Window` / `Document` through inclusive ancestors toward the target node. Listeners registered with `{ capture: true }` execute.
2.  **`AT_TARGET` (Numeric Value: 2)**: The event reaches the intended invocation target node (`e.target`). Listeners attached directly to the target execute regardless of their capture flag.
3.  **`BUBBLING_PHASE` (Numeric Value: 3)**: The event travels backward up the tree hierarchy from the target node back to the root `Window`. Listeners registered with `capture: false` execute, provided `e.bubbles` is set to `true`.

```
                    [Window / Document]
                           |   ^
   CAPTURING_PHASE (1)     |   |     BUBBLING_PHASE (3)
   (Downward path)         v   |     (Upward path)
                      [Parent Node]
                           |   ^
                           v   |
                    [Target Element]  <-- AT_TARGET (2)
```

#### Event Propagation Control Methods
*   `e.stopPropagation()`: Prevents an event from traveling to any other DOM nodes beyond the current node during capturing or bubbling propagation phases.
*   `e.stopImmediatePropagation()`: Prevents propagation to other nodes *and* instantly blocks any subsequent event listeners attached to the current element from executing.
*   `e.preventDefault()`: Cancels the browser's default native action associated with the event (e.g., blocking form submissions or link navigations), provided `e.cancelable` is `true`. Leaves propagation intact.
*   `cancelBubble`: Legacy getter/setter alias mapping directly to `stopPropagation()`.

#### Listener Registration Options (`addEventListener`)
*   `capture`: Boolean flag indicating whether the listener executes during the capturing phase.
*   `once`: Boolean flag that automatically removes the event listener immediately after its first execution.
*   `passive`: Boolean flag promising that the callback will **never** call `e.preventDefault()`. This allows browsers to execute touch and wheel scrolling asynchronously on the compositor thread without waiting for JavaScript execution, avoiding scroll lag.
    *   *Default Passive Values*: Browsers automatically default `passive` to `true` for `touchstart`, `touchmove`, `wheel`, and `mousewheel` events attached to `Window`, `Document`, or `body`.
*   `signal`: Accepts an `AbortSignal` object. Passing an aborted signal unbinds and cleans up the listener automatically.

#### Synthetic Events and Shadow DOM Retargeting
*   **`CustomEvent`**: Derived interface used to dispatch synthetic data across applications using the `detail` property: `new CustomEvent("topic", { detail: { data: 123 }, bubbles: true })`.
*   **Shadow DOM Retargeting**: When an event originates inside a Shadow DOM component tree and crosses the shadow boundary into the light DOM, `e.target` is dynamically retargeted to the host element encapsulating the shadow tree to preserve component abstraction. The full internal target path is accessible via `e.composedPath()` provided the `composed` flag is set to `true`.

#### Standardized Abort Operations: `AbortController` and `AbortSignal`
`AbortController` provides a standardized mechanism for canceling asynchronous promises, event listeners, and network operations.

*   `AbortController`: Controls an operational activity. Exposes a `.signal` property (`AbortSignal`) and an `.abort([reason])` method.
*   `AbortSignal`: Extends `EventTarget` to emit `abort` events.
    *   `signal.aborted`: Read-only boolean property indicating whether the operational task was aborted.
    *   `signal.reason`: Contains the specific abort reason (defaults to an `AbortError` `DOMException` if left unspecified).
    *   `signal.throwIfAborted()`: Throws `signal.reason` directly if the signal was canceled; otherwise does nothing.

##### Static Utility Methods (`DOM Standard`)
*   `AbortSignal.abort(reason)`: Generates a pre-aborted `AbortSignal` instance.
*   `AbortSignal.timeout(milliseconds)`: Generates an `AbortSignal` instance that automatically aborts after a specified duration with a `TimeoutError` `DOMException`.
*   `AbortSignal.any(signals)`: Takes an array of `AbortSignal` instances and returns a combined dependent signal that aborts as soon as **any** input signal aborts.

##### Dependent Signals Garbage Collection Rules
A non-aborted dependent `AbortSignal` **must not** be garbage collected while its source signals list is non-empty *and* it has active `abort` event listeners or registered internal abort algorithms.

---

## Short-Answer Practice Questions

### Question 1
**What structural changes occurred in the transition to DOM4 regarding `Node.ATTRIBUTE_NODE` (type constant 2), and why was this architectural change made?**

#### Answer
In DOM4 and the WHATWG Living Standard, `Node.ATTRIBUTE_NODE` was deprecated as a direct node within the DOM tree hierarchy. Attributes no longer act as structural child/parent tree nodes; instead, they operate as a separate key-value metadata map associated directly with an `Element`. This change eliminated unnecessary tree hierarchy pointers, reducing memory overhead in rendering engines and accelerating document tree traversal algorithms.

---

### Question 2
**Compare the operational mechanics and performance characteristics of live collections versus static snapshots.**

#### Answer
Live collections (e.g., `node.childNodes`, `getElementsByTagName`) maintain dynamic references directly linked to internal browser engine structures. Structural additions or deletions in the DOM immediately mutate the collection's `.length` and indices in real time during execution. Static collections (e.g., `querySelectorAll`) represent an immutable snapshot of the matching nodes at the exact time of query execution; subsequent DOM mutations do not alter the length or composition of static collections.

---

### Question 3
**How does the C-based Lexbor DOM engine optimize memory allocations for known standard HTML tags compared to custom elements?**

#### Answer
Lexbor uses a `uintptr_t` integer/pointer hybrid type for the `local_name` node property. For standard compile-time HTML tags (e.g., `<div>`, `<span>`), `local_name` directly stores a small compile-time integer ID below a threshold (`LXB_TAG__LAST_ENTRY = 0x00c6`). For unknown or custom tags (e.g., `<my-component>`), `local_name` stores a direct heap pointer to an entry in a tag hash table. Because heap pointers always exceed `0x00c6`, the engine evaluates standard tag IDs instantly with zero pointer dereferences or hash lookups.

---

### Question 4
**Explain the technical cause of Layout Thrashing and detail how it can be mitigated programmatically.**

#### Answer
Layout Thrashing is caused by alternating DOM style/structure write operations with geometry reading operations (such as `offsetWidth`, `getBoundingClientRect()`, or `scrollTop`) inside an execution loop. The read request forces the browser to flush its pending asynchronous mutation queue and perform a Forced Synchronous Layout to return accurate spatial metrics, dropping frame rates. It is mitigated by batching all geometric read operations together first, storing values in variables, and scheduling all DOM writes inside a deferred `requestAnimationFrame()` callback.

---

### Question 5
**What critical step must be executed prior to calling `observer.disconnect()` when building clean wrapper abstractions for `MutationObserver` or `IntersectionObserver`?**

#### Answer
Before invoking `observer.disconnect()`, wrapper libraries should call `observer.takeRecords()` to collect any unprocessed entries currently pending in the observer's queue. If records exist, they should be processed through the callback handler *prior* to disconnecting the observer instance to ensure no DOM changes or visibility transitions are silently ignored.

---

### Question 6
**How does `ResizeObserver` handle circular dimension changes to prevent browser infinite loops?**

#### Answer
If an observed element's dimensions are altered inside its own `ResizeObserver` callback, it risks creating an infinite layout loop. The engine prevents infinite execution by processing updates hierarchically and deferring notifications for elements located deeper in the DOM tree to the next frame tick, while outputting a non-fatal warning: `"ResizeObserver loop completed with undelivered notifications"`.

---

### Question 7
**What is the functional difference between `e.stopPropagation()` and `e.stopImmediatePropagation()` during event execution?**

#### Answer
`e.stopPropagation()` prevents the event from propagating further along the capture or bubble path to ancestor or descendant nodes in the DOM tree. `e.stopImmediatePropagation()` performs the same tree propagation stop *and* instantly blocks any remaining event listeners attached to the *current* target element from executing during that event tick.

---

### Question 8
**Why are passive event listeners critical for scroll performance on touch-enabled devices?**

#### Answer
By default, the browser engine must pause scrolling threads on touch/wheel events to wait for JavaScript execution in case `e.preventDefault()` is called to cancel scrolling. Registering a listener with `{ passive: true }` guarantees that `e.preventDefault()` will never be invoked, allowing the browser to process smooth asynchronous scrolling immediately on the compositor thread without waiting for main-thread JS execution.

---

### Question 9
**Explain the mechanics and utility of `AbortSignal.timeout()` and `AbortSignal.any()`.**

#### Answer
*   `AbortSignal.timeout(ms)`: Returns an `AbortSignal` instance that automatically triggers an abort action after a specified time limit, setting its `.reason` to a `TimeoutError` `DOMException`.
*   `AbortSignal.any(signals)`: Accepts an array of `AbortSignal` instances and returns a single dependent `AbortSignal`. The combined signal automatically aborts as soon as **any** signal in the provided array is aborted, inheriting the abort reason of whichever signal triggered first.

---

## Essay Prompts for Deeper Exploration

1.  **Engine Architectural Paradigms**: Analyze how low-level memory strategies (such as Lexbor's two-pool allocation architecture, zero-cost first-field struct inheritance, and `uintptr_t` union hashing) compare to high-level JavaScript DOM implementations. Discuss how memory pool sharing between `Document` and `DocumentFragment` instances impacts performance during large-scale HTML parsing.
2.  **Modern Web Application Performance Optimization**: Evaluate the Critical Rendering Path from DOM/CSSOM tree creation to layer compositing. Contrast the performance footprint of traditional DOM mutations (`innerHTML`, direct geometric reads) against modern observation-based patterns (`IntersectionObserver`, `ResizeObserver`, software container queries). Detail how batching reads and writes with `requestAnimationFrame` prevents Forced Synchronous Layouts.
3.  **Observer API Abstraction Strategies**: Compare functional wrapper functions (e.g., Splendid Labz utilities supporting dual event/callback APIs and multi-element arrays) against object-oriented subclassing strategies (extending native Observers with switch tables or type-specific hooks). Debate the performance, readability, and maintenance tradeoffs of both paradigms for modern application architectures.
4.  **Event Driven Architecture and Propagation Mechanics**: Detail the path of an event through the DOM propagation phases (`CAPTURING_PHASE`, `AT_TARGET`, `BUBBLING_PHASE`). Integrate into your analysis the concepts of event retargeting across Shadow DOM boundaries, passive scroll listeners, and modern task cancellation patterns using `AbortController`, `AbortSignal.any()`, and dependent signal garbage collection rules.

---

## Glossary of Important Terms

*   **`AbortController`**: A standard interface used to instantiate an `AbortSignal` object and trigger operational cancellation across promises, network calls, or event handling routines.
*   **`AbortSignal`**: An `EventTarget` interface emitting abort notifications. Tracks operational cancellation status via its `.aborted` boolean and `.reason` payload.
*   **`attr_class` / `attr_id`**: Cached internal engine pointers residing on element structs (`lxb_dom_element_t`) providing $O(1)$ fast access time to `id` and `class` attributes without iterating through linked lists.
*   **`CharacterData`**: An abstract interface extending `Node` that encapsulates text storage fields (`Text`, `Comment`, `CDATASection`).
*   **Compositing**: The final stage of the browser rendering pipeline where rasterized render layers are combined and drawn to the physical display screen via GPU processing.
*   **`DocumentFragment`**: A lightweight, unattached DOM `Node` container used to batch structural DOM operations off-screen, avoiding reflow penalties on the primary visible tree.
*   **Event Retargeting**: The dynamic re-assignment of an event's `.target` property when an event crosses a Shadow DOM boundary, preserving encapsulation by setting the target to the enclosing shadow host element.
*   **First-Field Embedding Pattern**: A C-language struct inheritance technique where the parent structure is embedded as the first member of a child structure, enabling zero-cost type casting between interfaces.
*   **Forced Synchronous Layout**: A performance bottleneck caused when JavaScript reads geometry properties (`offsetWidth`, `getBoundingClientRect()`) immediately after making DOM modifications, forcing the rendering engine to recalculate layout geometry synchronously.
*   **`insertAdjacentHTML()`**: A DOM method that parses an HTML string and injects the resulting nodes into a specified location relative to a target element (`beforebegin`, `afterbegin`, `beforeend`, `afterend`) without destroying existing children.
*   **`IntersectionObserver`**: An asynchronous browser API that tracks when a target element intersects visually with a designated root container or the viewport.
*   **Layout (Reflow)**: The critical rendering path phase where the browser calculates the precise pixel dimensions, geometry, and spatial positioning of elements within the render tree.
*   **Layout Thrashing**: An execution pattern where reading and writing layout geometry are repeatedly interleaved inside a loop, causing the browser to perform multiple synchronous layout recalculations within a single frame.
*   **Live Collection**: A dynamic array or list (e.g., `childNodes`, `getElementsByTagName`) that updates automatically when changes occur in the underlying DOM tree.
*   **Microtask Queue**: A high-priority JavaScript engine execution queue used to run asynchronous callbacks (such as `MutationObserver` entries and Promise handlers) before the browser paints the next visual frame.
*   **`MutationObserver`**: An asynchronous browser API that records structural modifications, attribute edits, or textual data changes within a DOM subtree.
*   **`Node.nodeType`**: A read-only integer property identifying the concrete type of a node object (e.g., 1 for `ELEMENT_NODE`, 3 for `TEXT_NODE`, 9 for `DOCUMENT_NODE`).
*   **Paint (Repaint)**: The critical rendering path phase where visual styling properties (`color`, `background-color`, `shadows`) are converted into pixel bitmaps across render layers without affecting geometric structure.
*   **Passive Listener Option**: An `addEventListener` setting (`{ passive: true }`) guaranteeing that `preventDefault()` will not be called, enabling immediate asynchronous scrolling on the compositor thread.
*   **`ResizeObserver`**: An asynchronous browser API that monitors changes to an element's geometric bounding box (`content-box` or `border-box`).
*   **Static Snapshot**: A static node list snapshot (e.g., returned by `querySelectorAll`) captured at query time that does not update when subsequent DOM tree mutations occur.
*   **`takeRecords()`**: A method available on observer APIs that synchronously flushes and returns any unhandled notification records currently waiting in the execution queue.
*   **`uintptr_t` (Lexbor Name Optimization)**: A pointer-sized integer type storing small tag/namespace IDs directly for predefined tags while holding direct heap memory pointers for custom/unknown markup tags.
*   **WHATWG DOM Living Standard**: The standard specification defining modern DOM data structures, event propagation mechanics, and tree manipulation algorithms across web engines.

## Relacionados
- [[02 - Frontend/02 - HTML|HTML]]
- [[02 - Frontend/03 - CSS|CSS]]
- [[02 - Frontend/04 - Layout|Layout]]

---
← [[02 - Frontend/04 - Layout|Layout]] · [[02 - Frontend/00 - Índice Frontend|Índice Frontend]] · [[02 - Frontend/06 - JavaScript|JavaScript]] →
