---
title: "HTML"
area: "Frontend"
numero: 2
aliases: ["HTML"]
tags: [concepto, it/frontend]
---
# HTML

> **Área:** [[02 - Frontend/00 - Índice Frontend|Índice Frontend]] · **Concepto 2 de 25**

## Qué abarca
- Estructura
- elementos
- atributos
- semántica

## Mis notas
<!-- ai:start -->
# Web Architecture & Accessibility: Comprehensive Study Guide

This study guide provides a systematic, highly technical synthesis of modern web architecture, HTML document structure, script execution mechanics, and web accessibility standards aligned with the Web Content Accessibility Guidelines (WCAG) 2.2 and WAI-ARIA standards.
<!-- ai:end -->

---

## Section 1: Key Concepts & Detailed Theoretical Synthesis

### Module 1: Document Structure, Rendering Modes, and Parsing Execution

#### 1.1 The DOCTYPE Declaration and Browser Rendering Modes
The Document Type Declaration (`<!DOCTYPE html>` or `<!doctype html>`) is a required, case-insensitive preamble positioned at the very first line of an HTML document. In modern HTML5, it no longer links to a formal Standard Generalized Markup Language (SGML) Document Type Definition (DTD). Instead, its primary functional purpose is to act as a rendering mode switch within the browser engine (such as Blink, Gecko, or WebKit), forcing the browser to render the document in **No-Quirks Mode** (Full Standards Mode).

```
Document Processing Pipeline:
[Raw HTML Document] ──> [Parser Reads Preamble] 
                            │
                            ├── Contains valid <!DOCTYPE html> ──> No-Quirks Mode (Full Standards)
                            ├── Historical Transitional DTD   ──> Limited-Quirks Mode
                            └── Missing / Preceded by Text    ──> Quirks Mode (IE5 Emulation)
```

Browsers operate under three primary rendering modes depending on the presence and structure of the DOCTYPE:

*   **No-Quirks Mode (Full Standards Mode):** Triggered by the modern `<!DOCTYPE html>` preamble. The layout engine strictly adheres to modern W3C and WHATWG specifications for HTML, CSS, and the Document Object Model (DOM). In JavaScript execution environments, `document.compatMode` evaluates to `"CSS1Compat"`.
*   **Limited-Quirks Mode (Almost Standards Mode):** Triggered by specific historical HTML4 Transitional DOCTYPEs accompanied by a System Identifier (URI). The browser engine adheres to modern standards for almost all layout calculations, with a single historical exception: vertical alignment and cell sizing calculations inside HTML table cells. In JavaScript, `document.compatMode` evaluates to `"CSS1Compat"`.
*   **Quirks Mode:** Triggered when the DOCTYPE is completely omitted, malformed, or preceded by text or other markup nodes. The browser disables modern web features and emulates the legacy behavior of Internet Explorer 5 and Netscape Navigator 4. It accepts malformed, non-standard code, uses a non-standard CSS box model (where `width` and `height` absorb `padding` and `border`), alters font size inheritance, and aligns content to the bottom of layout boxes instead of text baselines. In JavaScript, `document.compatMode` evaluates to `"BackCompat"`.

| Feature / Metric | No-Quirks Mode (*Full Standards*) | Limited-Quirks Mode (*Almost Standards*) | Quirks Mode (*Compatibility*) |
| :--- | :--- | :--- | :--- |
| **Syntactic Trigger** | `<!DOCTYPE html>` | Historical HTML4 Transitional with URI | Omitted or malformed DOCTYPE |
| **`document.compatMode`** | `"CSS1Compat"` | `"CSS1Compat"` | `"BackCompat"` |
| **Layout Model** | Standard W3C Box Model | Standard W3C Box Model (except table cells) | Legacy IE5 Box Model (padding/border absorbed) |
| **Font Size Inheritance** | Inherited standardly | Inherited standardly | Non-standard font size inheritance |
| **Vertical Text Alignment** | Aligned to text baseline | Deviates inside table cell sizing | Aligned to bottom of container box |

#### 1.2 Anatomy of an HTML Document and Head Sequence Requirements
An HTML document represents an explicit tree hierarchy rooted at the `<html>` element (the root element). The document divides into two distinct functional branches:
1.  `<head>`: A non-rendered container for document metadata, scripts, stylesheets, viewport settings, and document instructions.
2.  `<body>`: The container for all rendered, visible interface content (text, images, media, interactive widgets).

Within the `<head>`, the sequence of child elements directly impacts security, character encoding validation, and performance:

```
<head>
  <!-- 1. Must appear within first bytes to prevent re-parsing or character injection -->
  <meta charset="utf-8" />
  
  <!-- 2. Disables desktop screen emulation on mobile hardware -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  
  <!-- 3. Defines window/tab title and bookmark name -->
  <title>Document Title</title>
</head>
```

*   **Character Encoding (`<meta charset="utf-8" />`):** Must be declared within the first bytes of the document, ideally as the very first child of `<head>`. This ensures the HTML parser applies UTF-8 decoding prior to processing any readable text, including `<title>`, preventing character injection vulnerabilities and glyph corruption across non-ASCII Unicode characters.
*   **Viewport Configuration (`<meta name="viewport" content="width=device-width, initial-scale=1.0" />`):** Prevents mobile web browsers from emulating a desktop view layout viewport (typically ~980px). It aligns the layout viewport directly to the physical device width and sets the initial zoom scale to 1.0.

#### 1.3 The HTML Parser Pipeline and Script Execution Strategies
The browser processes HTML via a single-threaded, sequential parsing pipeline. When the parser encounters a standard, synchronous `<script src="...">` element, it executes a **parser-blocking operation**: DOM construction is paused immediately, a network request is issued for the script, and the script is parsed and executed before the HTML parser resumes DOM construction.

To optimize application performance, three asynchronous loading strategies are available:

```
Standard Synchronous Script:
HTML Parsing ────► [ PAUSED (Network Fetch & Execution) ] ────► Resume Parsing ──► DOMContentLoaded

async Script:
HTML Parsing ───────────────────────────► [ PAUSED (Exec) ] ──► Resume Parsing
Fetch Script (Parallel) ──► [ Executed Immediately ]

defer Script:
HTML Parsing ───────────────────────────────────────────────► DOMContentLoaded
Fetch Script (Parallel) ─────────────► [ Executed in Order ]

type="module" Script:
HTML Parsing ───────────────────────────────────────────────► DOMContentLoaded
Fetch Module Graph (Parallel) ───────► [ Executed in Order ]
```

*   **`async` Attribute:** Downloads the script file in parallel with HTML parsing. The moment the file finishes downloading, the HTML parser is **interrupted immediately** to execute the script. The execution order of multiple `async` scripts is non-deterministic (dependent strictly on file size and network delivery speeds). It must only be used for modular scripts that do not depend on DOM readiness or external dependencies (e.g., third-party analytics).
*   **`defer` Attribute:** Downloads the script file in parallel with HTML parsing, but **defers execution** until HTML parsing is completely finished, executing just before the `DOMContentLoaded` event. `defer` strictly preserves the document's original syntactic execution sequence across multiple deferred scripts.
*   **`type="module"` Scripts:** ES modules default to `defer` execution behavior automatically (fetching in parallel, executing sequentially after DOM construction). Modules execute strictly under JavaScript `strict mode`, maintain isolated module-level scopes (preventing global `window` pollution), and statically resolve dependency graphs (`import`/`export`) prior to evaluation. If `async` is explicitly attached to a module script (`<script type="module" src="..." async>`), deferred execution is overridden, and the module executes as soon as it and its resolved dependency graph are delivered over the network.
*   **`fetchpriority` Attribute:** Accepts `"high"` or `"low"` signals to explicitly tune network scheduler prioritizations for critical modules or low-priority scripts.

| Script Type / Attribute | Network Fetching | Execution Timing | Execution Order | Parser-Blocking Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **Synchronous Script** | Sequential / Blocking | Immediate upon fetch completion | Strict document order | **Yes:** Completely halts DOM construction |
| **`async`** | Asynchronous (Parallel) | Immediate upon fetch completion | Non-deterministic (Network-dependent) | **Partial:** Pauses parser only during execution |
| **`defer`** | Asynchronous (Parallel) | Post-parsing, prior to `DOMContentLoaded` | Strict document order | **No:** Allows uninhibited DOM parsing |
| **`type="module"`** | Asynchronous (Parallel) | Post-parsing (Default `defer` behavior) | Strict syntax/import order | **No:** Default deferred execution |

---

### Module 2: Semantic HTML, Content Models, and Architectural Landmarks

#### 2.1 Content Models: Void Elements vs. Container Elements
HTML syntax is governed by structural content models:

```
Container Element Anatomy:
 <p class="text-sample"> Content text goes here... </p>
 │  │                    │                         │
 │  └─ Attribute         └─ Element Content        └─ Closing Tag (Mandatory)
 └─ Opening Tag

Void Element Anatomy:
 <img src="chart.png" alt="Sales growth graph" />
 │    │
 │    └─ Attributes (Key-value parameters)
 └─ Opening Tag Only (NO content, NO closing tag)
```

*   **Container (Paired) Elements:** Consist of an opening tag (`<tag>`), contained text or child DOM nodes, and an explicit closing tag (`</tag>`). Omitting closing tags leads to DOM hierarchy parsing errors and unpredictable layout tree rendering.
*   **Void Elements:** Closed structural entities that **cannot contain text or descendents**. They consist strictly of a single opening tag housing attributes. Explicit closing tags (e.g., `</input>`) are syntactically illegal. Examples include `<meta>`, `<link>`, `<img>`, `<input>`, `<br>`, and `<hr>`. In HTML5, the trailing slash syntax (`<img />`) is optional and ignored by the parser.

#### 2.2 Semantic Elements and Landmark Regions
Semantic HTML utilizes markup tags that explicitly convey the structural role and data meaning of content to user agents, search engine NLP crawlers, and assistive technologies. HTML5 introduces landmark regions that map directly to accessibility tree structures without requiring explicit custom ARIA markup:

| Semantic Tag | Implied Landmark Role | Structural Constraints & Purpose |
| :--- | :--- | :--- |
| `<header>` | `banner` | Houses site branding, global search, and top-level identity. Restricted to **one global banner** per page context. |
| `<nav>` | `navigation` | Encloses primary or secondary navigation links. If multiple `<nav>` elements exist, they must be differentiated via distinct `aria-label` attributes. |
| `<main>` | `main` | Wraps the central, primary content unique to the document. Strictly **only one** `<main>` element may exist per document. |
| `<footer>` | `contentinfo` | Houses site-wide metadata, copyright statements, and legal links. Restricted to **one global contentinfo** region per page context. |
| `<aside>` | `complementary` | Wraps secondary content that supports or complements the main region (e.g., sidebars). Must hold a distinct context relative to `<main>`. |
| `<article>` | `article` | Defines an independent, self-contained composition capable of standalone distribution or reuse. |
| `<section>` | `region` | Groups thematic content. **Only generates a landmark region** in the accessibility tree if provided with an explicit accessible name via `aria-label` or `aria-labelledby`. |

---

### Module 3: The Accessibility Tree, WAI-ARIA Specifications, and Focus Management

#### 3.1 The Accessibility Tree Mechanics
Parallel to the visual DOM tree, browser engines construct an **Accessibility Tree** (`Accessibility Tree`). This secondary data abstraction strips visual presentation styling (CSS background colors, fonts, layout coordinates) and transforms DOM nodes into standardized nodes exposed to system Accessibility APIs (such as VoiceOver, Narrator, or NVDA).

```
Visual DOM Node ──────► [ Browser Engine Synthesis ] ──────► Accessibility Tree Node
                                                                │
  <button disabled>                                             ├── Role:  "button"
    Submit                                                      ├── Name:  "Submit"
  </button>                                                     ├── State: "disabled"
                                                                └── Value: ""
```

Every accessible node in the accessibility tree is characterized by four core properties:
1.  **Role:** Defines what the element is or does (e.g., `button`, `checkbox`, `navigation`, `banner`).
2.  **Name (Accessible Name):** The programmatically determined human-readable text label announced by screen readers (derived from text content, `alt` attributes, `aria-label`, or `aria-labelledby`).
3.  **State:** Mutable conditions of the element that change across its application lifecycle (e.g., `checked`, `disabled`, `expanded`, `readonly`, `aria-invalid`).
4.  **Value:** The current internal data value held by the node (e.g., input text, slider position).

#### 3.2 WAI-ARIA Attributes and Override Hierarchies
WAI-ARIA (Web Accessibility Initiative - Accessible Rich Internet Applications) provides explicit attributes to modify the Accessibility Tree. **ARIA alters only how assistive technology perceives an element; it injects zero native behavior, keyboard handling, or focusability.**

##### The First Rule of ARIA
> *If a native HTML element or attribute already exists that provides the semantics, keyboard navigation, and state management you require, use native HTML instead of custom elements augmented with ARIA.*

Using native `<button>` provides built-in `<Tab>` keyboard focus, `<Enter>` and `<Spacebar>` click event dispatching, and implicit `role="button"`. Recreating this via `<div role="button" tabindex="0">` forces developers to manually rewrite keyboard event handlers in JavaScript and increases code fragility.

##### ARIA Accessible Name Precedence
When determining an element's accessible name, browsers evaluate attributes according to a strict priority hierarchy:

$$\text{Precedence Order: } \text{aria-labelledby} > \text{aria-label} > \text{Native Content/Label} > \text{title}$$

```html
<!-- Example of ARIA Precedence -->
<button aria-label="Blue" aria-labelledby="color">Red</button>
<span id="color">Yellow</span>
```
*Evaluation:* In the example above, `aria-labelledby="color"` takes absolute precedence over `aria-label="Blue"` and the child text content `"Red"`. A screen reader will announce this button as **"Yellow"**.

##### ARIA Live Regions (`aria-live`)
Dynamic single-page application (SPA) updates do not trigger page reloads. Assistive technologies rely on `aria-live` declarations to announce dynamic content injected into the DOM post-load:
*   `aria-live="polite"`: The screen reader waits until the user finishes their current action/speech queue before announcing the update (low priority).
*   `aria-live="assertive"`: The update interrupts the screen reader's current activity immediately to announce the change (high priority).
*   `role="alert"`: Implicits an `aria-live="assertive"` boundary.

```html
<!-- Live Region Examples -->
<div aria-live="polite">Background upload complete.</div>
<div aria-live="assertive">Session timeout warning!</div>
<div role="alert">Network connection lost.</div>
```

---

### Module 4: WCAG 2.2 Principles, Conformance Levels, and Technical Success Criteria

The Web Content Accessibility Guidelines (WCAG 2.2) organize web accessibility standards under four fundamental principles (**POUR**): **Perceivable**, **Operable**, **Understandable**, and **Robust**. Conformance is categorized into three escalating levels: **A** (minimum compliance), **AA** (standard legal compliance, required by international frameworks such as BFSG), and **AAA** (specialized, maximum compliance).

```
          WCAG Conformance Hierarchy
                 ┌───────────┐
                 │ Level AAA │  (Complete text alternatives for all audio/video)
              ┌──┴───────────┴──┐
              │    Level AA     │  (BFSG Target: 4.5:1 text contrast, live captions)
           ┌──┴─────────────────┴──┐
           │       Level A         │  (Pre-recorded captions, basic alt text, keyboard access)
           └───────────────────────┘
```

#### 4.1 Principle 1: Perceivable
Information and user interface components must be presentable to users in ways they can perceive.

*   **Text Alternatives (WCAG 1.1.1):** Provide descriptive `alt` text for non-text informative content. Convey *semantic meaning*, not literal visual descriptors (e.g., use `alt="Search"` rather than `alt="Magnifying glass"`).
    *   *Decorative Images:* Must use an explicit empty attribute (`alt=""`) or `role="presentation"` to ensure screen readers skip them completely. Omitting the `alt` attribute entirely causes screen readers to read the file URL path aloud.
*   **Color Contrast Ratios (WCAG 1.4.3 & 1.4.11 - Level AA):**
    *   **Normal Text (< 24px / < 18.66px bold):** Must meet a minimum contrast ratio of **$\ge$ 4.5:1** against its actual background luminance.
    *   **Large Text ($\ge$ 24px or $\ge$ 18.66px bold):** Must meet a minimum contrast ratio of **$\ge$ 3:1**.
    *   **Non-Text UI Components (Icons, Form Input Borders, Focus Rings):** Must meet a minimum contrast ratio of **$\ge$ 3:1**.
*   **Use of Color (WCAG 1.4.1):** Color must never be used as the *sole visual means* of conveying information, indicating an action, or distinguishing an element. Error states must pair red borders with explicit error text labels or status icons. Links embedded within body text must include non-color identifiers (e.g., underlines).
*   **Zoom and Reflow (WCAG 1.4.4 & 1.4.10):** Text must scale up to **200%** without loss of content or functionality. Content must reflow down to **320 CSS pixels wide** without forcing vertical and horizontal dual-axis scrolling.
    *   *Prohibited syntax:* `<meta name="viewport" content="user-scalable=no">` or `maximum-scale=1` fail compliance because they block pinch-zoom mechanics.

#### 4.2 Principle 2: Operable
User interface components and navigation must be operable strictly via standard input interfaces.

*   **Keyboard Accessibility (WCAG 2.1.1):** All interactive controls must be reachable and operable via keyboard alone (`Tab`, `Shift+Tab`, `Enter`, `Spacebar`, Arrow keys).
    *   *Keyboard Traps:* Must be eliminated. If focus can be moved to a element using the keyboard, focus must be capable of leaving that element using the keyboard alone.
    *   *Device-Independent Event Handlers:* Avoid mouse-only listeners like `onMouseDown`. Use device-independent handlers like `onClick`.
*   **Focus Visible & Management (WCAG 2.4.7):** Any keyboard-operable control must possess a clearly visible focus indicator ring when focused. Focus styles must never be suppressed via CSS (`outline: none`) without providing an explicit `:focus-visible` replacement styling.
*   **Focus Order & Tab Indexing:** Natural focus order follows DOM source order. Custom positive `tabindex` values (`tabindex="1"`) are strictly forbidden as they override the logical reading order.
    *   `tabindex="0"`: Places a non-interactive element into the natural keyboard tab sequence.
    *   `tabindex="-1"`: Removes an element from the sequential tab order, but allows it to receive programmatic focus via JavaScript (`element.focus()`).
*   **Skip Links (WCAG 2.4.1 - Level A):** Provide a "Skip to main content" anchor as the first focusable element in the DOM to allow keyboard users to bypass repeated global navigation bars.

```css
/* Skip Link CSS Pattern */
.skip-link {
  position: absolute;
  left: -9999px; /* Hide off-screen */
}
.skip-link:focus {
  left: 1rem;   /* Reveal in viewport when focused */
  top: 1rem;
  z-index: 1000;
}
```

*   **Modal Focus Trapping:** Opening a modal dialog must shift focus inside the dialog, trap keyboard focus within its boundary while open, and **return focus to the triggering element** upon closing. Utilizing native `<dialog>` elements alongside `dialog.showModal()` handles focus trapping, top-layer elevation, and `<Esc>` key dismissal natively.

#### 4.3 Principle 3: Understandable
Information and the operation of the user interface must be understandable.

*   **Document Language (WCAG 3.1.1 - Level A):** The primary human language of the document must be declared on the root `<html>` tag via the `lang` attribute (e.g., `<html lang="en-US">` or `<html lang="de">`). This instructs speech synthesizers to load correct phonetic packages and assists search engines with content geolocalization.
*   **Input Assistance and Error Handling (WCAG 3.3.1 & 3.3.2):** Form fields must have programmatically associated `<label>` tags via matching `for` and `id` attributes. Error messages must explicitly describe how to fix validation failures. Generic error messages (e.g., "Invalid input") fail compliance; descriptive assistance must be provided (e.g., "Password must be at least 8 characters long and include a number").
    *   *Placeholders are NOT Labels:* `<input placeholder="...">` is unsuited as a label substitute because placeholder text disappears upon typing, typically fails color contrast minimums, and is inconsistently announced by screen readers.

```html
<!-- Compliant Form Input & Associated Error Pattern -->
<label for="email">Email Address</label>
<input 
  id="email" 
  type="email" 
  name="email" 
  aria-describedby="email-error" 
  aria-invalid="true" 
  required 
/>
<p id="email-error" role="alert">Enter a valid email address containing an '@' symbol.</p>
```

#### 4.4 Principle 4: Robust
Content must be robust enough that it can be interpreted reliably by a wide variety of user agents, including assistive technologies.

*   Ensure all programmatic names, roles, and states can be calculated deterministically.
*   Ensure custom UI components strictly enforce proper nesting rules, valid attributes, and standardized states to prevent DOM rendering engines from failing.

#### 4.5 New Success Criteria in WCAG 2.2

WCAG 2.2 introduces nine new success criteria extending WCAG 2.1. Key practical developer additions include:

1.  **Focus Not Obscured (Minimum) (Criterion 2.4.11 - Level AA):** Ensures that when an element receives keyboard focus, it is not completely hidden or covered by sticky headers, fixed footers, or non-modal banners.
2.  **Target Size (Minimum) (Criterion 2.5.8 - Level AA):** Pointer target sizes for interactive controls must be at least **24 $\times$ 24 CSS pixels**, unless an adequate spatial offset boundary surrounds a smaller target.
3.  **Dragging Movements (Criterion 2.5.7 - Level AA):** Any feature requiring a complex drag-and-drop movement must offer a single-pointer alternative (e.g., clicking up/down arrow buttons to reorder list items).
4.  **Accessible Authentication (Minimum) (Criterion 3.3.8 - Level AA):** Cognitive function tests (such as memorizing passwords, solving puzzles, or transcribing CAPTCHAs) must not be required for authentication without providing an accessible alternative mechanism. Never block paste operations on password inputs (`onpaste="return false"` is prohibited), and support password managers and WebAuthn passkeys.

---

### Module 5: Accessibility Testing Paradigms and Automated vs. Manual Diagnostics

A comprehensive accessibility validation strategy relies on layered diagnostics combining automated audits, browser DevTools analysis, manual keyboard testing, and screen reader verification.

```
                  Layered Diagnostic Pipeline
 ┌────────────────────────────────────────────────────────────┐
 │  Automated Scanners (Lighthouse / axe)                     │ ──► Catches 30%–50% of issues
 ├────────────────────────────────────────────────────────────┤     (Missing alt, low contrast)
 │  DevTools Inspection (Tab order, Accessibility Tree)       │
 ├────────────────────────────────────────────────────────────┤
 │  Manual Keyboard Testing (Tab navigation, Focus rings)     │ ──► Catches Focus Traps, Logical
 ├────────────────────────────────────────────────────────────┤     Reading Order, Target Sizes
 │  Screen Reader Diagnostics (VoiceOver / NVDA / Narrator)   │
 └────────────────────────────────────────────────────────────┘
```

1.  **Automated Audit Scanners (Lighthouse / axe):** High-speed automated analysis embedded in Chrome/Edge DevTools or CI/CD pipelines.
    *   *Scope Limit:* **Automated tools detect only 30% to 50% of total potential accessibility bugs.** A Lighthouse score of "100" does *not* guarantee compliance; it validates syntax rules like image `alt` presence, standard contrast minimums, and duplicate ID presence. It cannot evaluate human semantic context, such as whether an image's `alt` description is meaningful.
2.  **Accessibility Tree DevTools Inspection:** Inspecting browser engine representations (`DevTools > Elements > Accessibility`). Allows developers to ensure names, roles, and states exposed to ATs match UI designs.
3.  **Keyboard Tab-Order Visualization:** Utilizing tools (such as Firefox `DevTools > Accessibility > Show Tab Order`) to visually verify sequential keyboard focus, ensuring visual focus paths match source DOM layout logic without positive `tabindex` interruptions.
4.  **Integrated Screen Readers:** Manual testing using native screen reader software—VoiceOver (macOS/iOS), Narrator (Windows), or NVDA (open-source Windows)—to evaluate actual audio output, dynamic live region announcements, and modal focus containment.

---

## Section 2: Short-Answer Practice Questions

### Question 1
**Explain the technical impact on the browser layout engine when an HTML document completely omits the `<!DOCTYPE html>` preamble. Reference specific rendering properties and `document.compatMode`.**

#### Model Answer
Omitting the `<!DOCTYPE html>` preamble forces the browser layout engine to enter **Quirks Mode** to maintain backward compatibility with legacy web pages built for older browsers like Internet Explorer 5. In Quirks Mode, the layout engine disables modern CSS and HTML standards specifications. The CSS box model is altered so that an element's `width` and `height` properties improperly absorb padding and border dimensions. Font size inheritance across structural elements breaks, and vertical text alignments resolve to container box bottoms rather than text baselines. In JavaScript, `document.compatMode` evaluates to `"BackCompat"` instead of `"CSS1Compat"`.

---

### Question 2
**Contrast the execution flow, parser-blocking behavior, and sequence determinism of `<script async src="...">` versus `<script defer src="...">`.**

#### Model Answer
*   `async`: Downloads the script file in parallel with HTML parsing. The instant network delivery finishes, the HTML parser is **interrupted** and paused while the script executes immediately. If multiple `async` scripts are declared, their execution sequence is non-deterministic, executing entirely on a first-downloaded, first-executed basis.
*   `defer`: Downloads the script file in parallel with HTML parsing, but **defers execution** until HTML parsing has completely finished, executing immediately prior to the `DOMContentLoaded` event. `defer` scripts never pause the HTML parser during downloading, and they strictly execute in the exact order they were declared in the document source code.

---

### Question 3
**Evaluate the following line of HTML code for screen reader output based on ARIA name precedence rules:**
```html
<button aria-label="Submit Form" aria-labelledby="lbl-text">Cancel Action</button>
<span id="lbl-text">Confirm Entry</span>
```
**What text string will a screen reader read aloud when focusing this button?**

#### Model Answer
The screen reader will read **"Confirm Entry"**. According to WAI-ARIA accessible name computation rules, `aria-labelledby` holds absolute highest priority over all other label declarations. It overrides both the `aria-label` attribute ("Submit Form") and the child text node contained within the button tag ("Cancel Action").

---

### Question 4
**What are the minimum WCAG 2.2 Level AA color contrast requirements for (a) normal body text, (b) large heading text, and (c) active form input border boundaries? Define the exact pixel boundaries for "large text."**

#### Model Answer
*   (a) **Normal text:** Minimum contrast ratio of **4.5:1** against its background luminance.
*   (b) **Large text:** Minimum contrast ratio of **3.1** against its background luminance. Large text is defined as text measuring at least **24 CSS pixels** ($\text{1.5rem}$), or at least **18.66 CSS pixels** ($\text{1.167rem}$) when explicitly styled as **bold**.
*   (c) **Form input border boundaries:** Categorized as non-text user interface components and require a minimum contrast ratio of **3:1** against adjacent background pixels.

---

### Question 5
**Identify the critical accessibility flaw in using `<input placeholder="Enter First Name">` without an associated `<label>` tag. State two reasons why placeholder text cannot replace an input label.**

#### Model Answer
Placeholders are not programmatically associated input labels under WCAG 3.3.2. Primary flaws include:
1.  Placeholder text disappears completely the moment a user begins typing input text, leaving users with low vision or cognitive differences without a persistent visible indication of the field's purpose.
2.  Default browser placeholder text fails the mandatory 4.5:1 color contrast ratio.
3.  Many assistive technologies fail to reliably announce placeholder text as the field's accessible name, resulting in screen readers announcing the input simply as "edit text" without context.

---

### Question 6
**Explain the First Rule of ARIA. Provide an example of bad ARIA markup and write its correct native semantic HTML replacement.**

#### Model Answer
The First Rule of ARIA dictates that if a native HTML element already exists that possesses the exact semantics, keyboard capabilities, and focus behaviors required, you must use the native HTML element instead of using ARIA to emulate those properties on non-semantic tags.

*   *Incorrect (Bad ARIA):*
    ```html
    <div role="button" tabindex="0" onclick="saveData()">Save</div>
    ```
    *(Requires writing custom JS handlers for `<Enter>` and `<Spacebar>` key presses and managing visual focus state manually).*
*   *Correct (Native HTML):*
    ```html
    <button type="button" onclick="saveData()">Save</button>
    ```

---

### Question 7
**Explain the functional difference between `alt=""` and omitting the `alt` attribute entirely on an `<img>` tag.**

#### Model Answer
*   `alt=""` (Empty alt attribute): Explicitly marks an image as purely decorative. The browser's layout engine strips the image node from the Accessibility Tree, causing screen readers to skip over the image completely without making an announcement.
*   *Omitting `alt` entirely:* Informs assistive technology that the image's status is unlabelled. Instead of skipping the image, many screen readers will fall back to reading the raw file path URL (e.g., `"https://example.com/assets/images/header-banner-v2-final.png"`), causing a confusing audio experience for visual-at-risk users.

---

### Question 8
**Describe two new success criteria introduced in WCAG 2.2 and provide developer guidelines for complying with them.**

#### Model Answer
1.  **Target Size (Minimum) (Criterion 2.5.8 - Level AA):** Requires all interactive pointer targets (buttons, links, icon toggles) to measure at least **24 $\times$ 24 CSS pixels**, or ensure CSS spacing/margins around smaller targets provide an equivalent 24px bounding radius. Compliance is achieved by setting `min-width: 24px; min-height: 24px;` in CSS on icon buttons.
2.  **Accessible Authentication (Minimum) (Criterion 3.3.8 - Level AA):** Authentication flows must not rely on cognitive function tests (such as remembering complex passwords, solving math puzzles, or typing CAPTCHAs) without offering an accessible alternative. Developers comply by supporting WebAuthn passkeys, permitting password manager autofill, and ensuring password inputs **never disable text pasting** (`onpaste="return false"` must be avoided).

---

## Section 3: Essay Prompts for Deeper Exploration

### Essay Prompt 1: The Anatomy of Browser Rendering and Script Orchestration
> Deconstruct the end-to-end browser execution pipeline from the processing of the initial network byte stream to the execution of the `DOMContentLoaded` event. In your essay, analyze how rendering modes (`document.compatMode`), `<head>` sequencing, parser-blocking script tags, `async`/`defer` modifiers, and ES module trees (`type="module"`) interact with DOM parsing performance. Detail the technical mechanics that cause parser blocking, and articulate how modern loading strategies prevent degradation of interactive performance metrics.

---

### Essay Prompt 2: Accessibility Tree Architecture and the Mechanics of WAI-ARIA
> Analyze the architectural relationship between the Document Object Model (DOM) and the Accessibility Tree (`Accessibility Tree`). Explain how system accessibility APIs consume accessibility tree properties (Role, Name, State, Value) to render content to screen readers. In the second half of your essay, critique the misuse of WAI-ARIA in modern Web development. Ground your critique in the "First Rule of ARIA," evaluating why ARIA overuse frequently increases accessibility defects according to empirical testing studies. Provide code examples contrasting bad ARIA implementations against semantic HTML replacements.

---

### Essay Prompt 3: WCAG 2.2 Conformance Engineering: POUR Principles in Single-Page Applications
> You are tasked with leading the accessibility architecture overhaul for a complex enterprise Single-Page Application (SPA) to ensure strict compliance with WCAG 2.2 Level AA guidelines (and the Barrierefreiheitsstärkungsgesetz framework). Systematically address how your engineering team will implement compliance across all four POUR principles. Detail technical strategies for:
> 1. Managing dynamic route changes and live dynamic content (`aria-live`, dynamic `<title>` updates).
> 2. Complex focus management (focus trapping in modals via `<dialog>`, preventing obscured focus under sticky toolbars per WCAG 2.4.11).
> 3. Form input validation and error feedback loops.
> 4. Meeting WCAG 2.2 color contrast, 200% zoom reflow, and 24px minimum touch target size constraints.

---

### Essay Prompt 4: Diagnostic Frameworks: Automated Tooling vs. Manual Accessibility Validation
> "A web page achieving a 100/100 score on Lighthouse or passing automated axe-core audits can still be completely unusable for a screen-reader or keyboard-only user." Critique this statement. Evaluate the technical capabilities and fundamental boundaries of automated accessibility scanners. Construct a comprehensive, multi-layered quality assurance testing framework that integrates automated static analysis, browser DevTools inspection, manual keyboard navigation routines, and native screen reader testing workflows. Specify exactly which WCAG criteria require human manual intervention to validate.

---

## Section 4: Comprehensive Glossary of Important Terms

```
   ┌─────────────────────────────────────────────────────────┐
   │                  Glossary Index Map                     │
   │  [A] Accessibility Tree, ARIA, Async, Auth (Accessible) │
   │  [B] BFSG, Boolean Attributes                           │
   │  [C] Character Entity Ref, Color Contrast, Container    │
   │  [D] Defer, DOCTYPE, DOM                                │
   │  [F] Fetchpriority, Focus Trap                          │
   │  [K] Keyboard Accessibility                             │
   │  [L] Landmark Regions, Live Regions                     │
   │  [N] No-Quirks Mode                                     │
   │  [P] Parser-Blocking, POUR Principles                   │
   │  [Q] Quirks Mode                                        │
   │  [S] Semantic HTML, Skip Links                          │
   │  [T] Target Size, Tabindex                              │
   │  [V] Viewport, Void Elements                            │
   │  [W] WCAG 2.2                                           │
   └─────────────────────────────────────────────────────────┘
```

### Accessibility Tree
A specialized, secondary data structure generated by the browser layout engine alongside the visual DOM tree. It converts DOM nodes into standardized accessibility nodes characterized by explicit **Roles**, **Names**, **States**, and **Values**, exposing them to operating system accessibility APIs (e.g., VoiceOver, NVDA, Narrator).

### Accessible Authentication (WCAG 2.2 Criterion 3.3.8)
A Level AA WCAG 2.2 requirement mandating that user authentication mechanisms do not rely on cognitive function tests (such as memorizing passwords, transcriptions, or solving puzzles) unless an alternative accessible method (e.g., passkey support, password manager autofill, paste enablement) is available.

### ARIA (Accessible Rich Internet Applications)
A set of technical specifications published by the W3C that adds semantic roles, states, and properties (`aria-*`) to HTML markup. ARIA modifies how an element is interpreted within the Accessibility Tree without adding functional behavior, styles, or native keyboard event handling.

### `async`
A boolean attribute applied to `<script>` elements that downloads the target script file asynchronously in parallel with HTML DOM parsing. Once downloading completes, the browser parser halts parsing to execute the script immediately. Execution order across multiple `async` scripts is non-deterministic.

### Barrierefreiheitsstärkungsgesetz (BFSG)
German legislation (enacted June 2025) mandating digital accessibility standard compliance across web applications and commercial digital services, aligned directly with WCAG Level A and Level AA standards.

### Boolean Attribute
An HTML attribute whose structural presence in an opening tag indicates a `true` logical state, while its total omission indicates a `false` state. In syntax, setting explicit values is redundant (e.g., `<input disabled>` is equivalent to `<input disabled="disabled">`).

### Character Entity Reference
A standardized alphanumeric string beginning with an ampersand (`&`) and terminating with a semicolon (`;`), used to encode reserved HTML syntax characters inside text nodes. Primary references include `&lt;` (`<`), `&gt;` (`>`), `&quot;` (`"`), `&apos;` (`'`), and `&amp;` (`&`).

### Color Contrast Ratio
The calculated ratio of relative luminance between foreground element colors (text or icons) and background surface colors. WCAG 2.2 AA requires minimums of **4.5:1** for normal text, **3:1** for large text ($\ge$ 24px or $\ge$ 18.66px bold), and **3:1** for UI visual boundaries/icons.

### Container Elements
HTML structural elements composed of an opening tag, inner text content or DOM child nodes, and an explicit closing tag (e.g., `<p>text</p>`). Omitting closing tags leads to malformed DOM tree parsing.

### `defer`
A execution modifier attribute attached to `<script>` elements. It instructs the browser to download the script in parallel with HTML parsing, but defer script execution until DOM construction completes entirely, immediately preceding `DOMContentLoaded`. It guarantees code execution follows document declaration sequence.

### DOCTYPE
The document type declaration preamble placed at the absolute top of HTML files (`<!DOCTYPE html>`). Its function in modern web standards is to switch the browser layout engine into **No-Quirks Mode** (Full Standards Mode) and set `document.compatMode` to `"CSS1Compat"`.

### DOM (Document Object Model)
The primary memory-resident tree object representation constructed by the browser HTML parser. It exposes all HTML tags, attributes, and text nodes as mutable programmatic objects accessible via JavaScript.

### `fetchpriority`
An attribute attached to scripts or link resources accepting values `"high"` or `"low"`. It provides priority signals to the browser network request scheduler to adjust resource download sequencing.

### Focus Not Obscured (WCAG 2.2 Criterion 2.4.11)
A WCAG 2.2 Level AA success criterion mandating that when an interactive component receives keyboard focus, layout elements (such as fixed headers, sticky footers, or floating overlays) do not fully cover or obscure the visible focus ring indicator.

### Focus Trap
An accessibility defect where a keyboard user navigates into a component or container (such as a custom modal overlay) using `<Tab>`, but cannot navigate focus back out to the rest of the document without using a mouse.

### Keyboard Accessibility
The principle that every interactive interface control reachable by a mouse pointer must be entirely reachable, focusable, and operable using a physical keyboard alone via standardized key bindings (`Tab`, `Shift+Tab`, `Enter`, `Spacebar`, Arrow keys).

### Landmark Region
High-level structural regions defined via semantic HTML elements (`<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>`) or ARIA landmark roles that allow assistive technology users to jump directly to specific functional content sections within a document.

### Live Region (`aria-live`)
A designated DOM node decorated with `aria-live="polite"` or `aria-live="assertive"` attributes. It monitors background JavaScript changes to its child nodes and automatically instructs screen readers to announce textual updates without disrupting page context.

### No-Quirks Mode
The modern browser rendering mode activated by the `<!DOCTYPE html>` preamble. The layout engine renders all CSS properties, HTML elements, and DOM APIs according to strict modern W3C/WHATWG specifications. Reflected by `document.compatMode === "CSS1Compat"`.

### Parser-Blocking Operations
Occurs when the browser HTML parser encounters a standard synchronous `<script src="...">` tag. The parser must halt DOM tree construction, execute a network fetch for the script file, and parse and execute its JavaScript content before re-starting HTML parsing.

### POUR Principles
The foundational architectural categorization framework of WCAG accessibility standards:
*   **P**erceivable (information presentable in usable senses)
*   **O**perable (interface components workable by keyboard/inputs)
*   **U**nderstandable (operation and layout logically predictable)
*   **R**obust (compatible across legacy and modern user agents/ATs)

### Quirks Mode
A legacy rendering mode activated when an HTML document lacks a valid DOCTYPE declaration. The layout engine emulates Internet Explorer 5 layout bugs, uses a non-standard CSS box model, alters font-size inheritance, and sets `document.compatMode` to `"BackCompat"`.

### Semantic HTML
The practice of structuring web pages using HTML elements that explicitly convey structural role, content type, and structural purpose (`<article>`, `<button>`, `<label>`) rather than unsemantic, generic container tags (`<div>`, `<span>`).

### Skip Link
An accessible navigation pattern consisting of an anchor link positioned as the very first focusable element in the DOM (e.g., `<a href="#main" class="skip-link">Skip to main content</a>`). It allows keyboard users to bypass global navigation blocks.

### Target Size (Minimum) (WCAG 2.2 Criterion 2.5.8)
A WCAG 2.2 Level AA criterion requiring pointer input controls (buttons, links, click targets) to measure a minimum size of **24 $\times$ 24 CSS pixels**, or provide sufficient spatial margins to ensure adjacent target boundaries do not overlap.

### `tabindex`
A global HTML attribute controlling an element's focusability and sequential keyboard tab navigation order:
*   `tabindex="0"`: Inserts a non-interactive element into the natural keyboard tab flow.
*   `tabindex="-1"`: Removes an element from sequential tab order while keeping it programmatically focusable via JavaScript.
*   *Positive `tabindex` values (`tabindex="1"`):* Strictly forbidden because they break reading logic.

### Viewport `<meta>` Tag
A required head element (`<meta name="viewport" content="width=device-width, initial-scale=1.0">`) that sets the browser layout viewport width to match the physical device hardware width, disabling artificial desktop view scale emulations on mobile devices.

### Void Elements
A defined class of HTML tags that are forbidden from holding inner text content or descending DOM nodes. They consist strictly of a single opening tag housing parameters (e.g., `<meta>`, `<link>`, `<img>`, `<input>`, `<br>`, `<hr>`). Self-closing syntax (`<br />`) is optional.

### WCAG 2.2
The Web Content Accessibility Guidelines version 2.2; the internationally recognized standard for digital accessibility technical compliance, maintained by the World Wide Web Consortium (W3C). Organized under the 4 POUR principles and 3 conformance levels (A, AA, AAA).

## Relacionados
- [[02 - Frontend/03 - CSS|CSS]]
- [[02 - Frontend/04 - Layout|Layout]]
- [[02 - Frontend/05 - DOM|DOM]]

---
← [[02 - Frontend/01 - Internet & Web|Internet & Web]] · [[02 - Frontend/00 - Índice Frontend|Índice Frontend]] · [[02 - Frontend/03 - CSS|CSS]] →
