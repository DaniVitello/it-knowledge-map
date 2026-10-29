---
title: "CSS"
area: "Frontend"
numero: 3
aliases: ["CSS"]
tags: [concepto, it/frontend]
---
# CSS

> **Área:** [[02 - Frontend/00 - Índice Frontend|Índice Frontend]] · **Concepto 3 de 25**

## Qué abarca
- Cascade
- especificidad
- box model
- estilos

## Mis notas
<!-- ai:start -->
# Comprehensive Study Guide: CSS Cascade, Specificity, Box Model, and Value Processing Architecture
<!-- ai:end -->

---

## Section 1: Key Concepts & Module Summaries

### Module 1: The CSS Value Processing Pipeline

The browser rendering engine systematically processes every CSS property for every element through a mandatory six-stage pipeline to resolve declared rules into physical target pixels on the hardware display.

```
+-----------------------------------------------------------------+
|                       1. DECLARED VALUE                         |
|   Collect matching syntactically valid declarations per element  |
+-----------------------------------------------------------------+
                                |
                                v
+-----------------------------------------------------------------+
|                       2. CASCADED VALUE                         |
|   Sort declared values via cascade rules; highest priority wins |
+-----------------------------------------------------------------+
                                |
                                v
+-----------------------------------------------------------------+
|                       3. SPECIFIED VALUE                        |
|   Assign cascaded value, OR inherit, OR set initial fallback    |
+-----------------------------------------------------------------+
                                |
                                v
+-----------------------------------------------------------------+
|                       4. COMPUTED VALUE                         |
|   Resolve relative units/URLs into absolute terms (no layout)   |
+-----------------------------------------------------------------+
                                |
                                v
+-----------------------------------------------------------------+
|                         5. USED VALUE                           |
|   Calculate spatial layout dependencies against containing block |
+-----------------------------------------------------------------+
                                |
                                v
+-----------------------------------------------------------------+
|                        6. ACTUAL VALUE                          |
|   Apply physical device constraints (e.g., rounding to pixels)  |
+-----------------------------------------------------------------+
```

#### Pipeline Stages Detailed

1. **Declared Value**: The user agent identifies all syntactically valid style rules whose selectors match a given element for the target media type, filtering out rules that fail conditional media or feature queries.
2. **Cascaded Value**: The outcome of the cascade sorting algorithm. If competing declarations match an element property, the single declaration that wins based on origin, importance, cascade layer, specificity, and order of appearance becomes the cascaded value. If no declarations match, there is no cascaded value.
3. **Specified Value**: The defaulting phase guarantees that every property receives a concrete value. If a cascaded value exists, it becomes the specified value. If no cascaded value exists, the specified value is assigned via inheritance from the parent element (for inherited properties) or set to the property's specification-defined initial value (for non-inherited properties).
4. **Computed Value**: Relative values and keywords are converted into absolute metrics without requiring layout context. Units such as `rem` or `em` resolve to absolute pixel values based on font metrics, and relative URLs convert to absolute addresses. Non-resolvable URIs remain as specified. The computed value exists even if the property does not apply to the element and is the precise value passed down to child nodes during inheritance.
5. **Used Value**: Layout-dependent metrics are calculated after evaluating document geometry against containing blocks. For instance, percentage-based widths or `auto` margins cannot be determined until containing block dimensions are calculated. Resolving these dependencies yields the used value.
6. **Actual Value**: The used value adapted to the limitations of the local rendering environment. The user agent applies physical adjustments, such as rounding fractional sub-pixel widths to integer physical pixels or approximating colors for display constraints.

| Stage | Operational Definition | Example Transformation | Stage Output Characteristics |
| :--- | :--- | :--- | :--- |
| **Declared Value** | Syntactically valid rule matching an element | `font-size: 1.2rem;` | Raw declaration string |
| **Cascaded Value** | Winning declaration post-cascade sorting | `font-size: 1.2rem;` | Single victorious declaration |
| **Specified Value** | Result of cascade victory or defaulting fallback | `1.2rem` (from Cascade) | Explicit specified value |
| **Computed Value** | Absolute value resolved prior to layout context | `1.2rem` (Root: 16px) $\rightarrow$ `19.2px` | Absolute unit; value passed to children |
| **Used Value** | Metric resolved against layout geometry | `width: 50%` (Parent: 800px) $\rightarrow$ `400px` | Absolute spatial layout output |
| **Actual Value** | Hardware-adjusted metric for display targets | `400.33px` $\rightarrow$ `400px` | Integer device physical target |

---

### Module 2: Cascade Resolution Hierarchy, Origins, and Cascade Layers

The cascade algorithm evaluates competing property declarations using a strict, multi-tiered sorting hierarchy established across CSS specifications.

#### Cascade Origins and Precedence Hierarchy

Style declarations originate from three distinct authority tiers:
* **User Agent (UA)**: Default browser styles setting baseline rendering.
* **User**: Personal configuration or accessibility style overrides.
* **Author**: Application developer stylesheets (external, embedded, or inline).

The presence of the `!important` annotation fundamentally alters cascade precedence by explicitly inverting the origin authority hierarchy. Under standard conditions, Author styles override User styles, which override User Agent styles. When `!important` is applied, User Agent rules take highest priority, overriding User and Author rules.

Additionally, active CSS Keyframe Animations and active CSS Transitions interact with the cascade at explicit priority levels.

#### The 8-Tier Cascade Precedence Rank (Lowest to Highest)

1. **User Agent Normal**: Standard default browser stylesheet declarations.
2. **User Normal**: Normal accessibility and personalized browser setting styles.
3. **Author Normal**: Developer styles defined in external or embedded stylesheets.
4. **CSS Keyframe Animations**: Property values driven by active `@keyframes` rules (override normal author styles, but yield to all `!important` rules).
5. **Author `!important`**: Developer declarations flagged with `!important`.
6. **User `!important`**: User accessibility overrides flagged with `!important`.
7. **User Agent `!important`**: Critical system default styles flagged with `!important`.
8. **Active CSS Transitions**: Interpolated property values during active transition states (take absolute precedence over all other declarations, including `!important`).

#### Cascade Sorting Order Steps

To determine a property value, the user agent applies sorting in the following sequential order:
1. **Origin & Importance**: Sort by origin tier and normal vs. `!important` status.
2. **Cascade Layers (`@layer`)**: Within a single origin and importance tier, declarations are sorted by layer order.
3. **Selector Specificity**: Rules with identical origin, importance, and layer priority are sorted by selector specificity.
4. **Order of Appearance**: If origin, importance, layer, and specificity are identical, the last specified rule wins. Declarations in imported stylesheets (`@import`) are treated as appearing before rules in the importing stylesheet itself.

#### Cascade Layers (`@layer`) Dynamics

Cascade Layers (introduced in CSS Cascading and Inheritance Level 5) sit between origin/importance evaluation and selector specificity calculation:
* **Normal Rules**: Unlayered author styles automatically take precedence over layered author styles. Among layered styles, layers declared **later** in the document stream override layers declared **earlier**.
* **`!important` Rules**: The precedence order completely reverses. Layered `!important` declarations take precedence over unlayered `!important` declarations. Among layers, `!important` declarations in **earlier-declared** layers override `!important` declarations in **later-declared** layers.
* **Structure & Import**: Layers support dot-notation syntax (e.g., `@layer framework.components`). Unnamed/anonymous layers cannot be referenced elsewhere and create encapsulated style boundaries. `@import` rules must precede all other style rules (except `@charset`), and can import stylesheets directly into named or anonymous layers or specify media types.

---

### Module 3: Specificity Vector Calculations and Selector Dynamics

Specificity is a three-component vector tuple $\vec{S} = (a, b, c)$ calculated from the form of a selector to resolve conflicts among rules of equal origin, importance, and layer priority.

$$\vec{S} = (a, b, c)$$

* **Component $a$**: Count of ID attributes within the selector.
* **Component $b$**: Count of class selectors, attribute selectors, and pseudo-classes.
* **Component $c$**: Count of type (element) selectors and pseudo-elements.

*Note on Historical Context*: Older CSS2 specifications represented specificity as a four-component vector $(a, b, c, d)$, where $a=1$ represented inline rules defined via an element's HTML `style` attribute (which carry no selector), $b$ represented IDs, $c$ represented classes/attributes/pseudo-classes, and $d$ represented elements/pseudo-elements. Modern CSS Level 5 categorizes inline styles above unlayered author rules in the cascade order, evaluating selector specificity as $(a, b, c)$.

#### Lexicographical Comparison Rules

Vectors are evaluated from left to right. A higher count in a leftward position completely dominates any value in a rightward position, regardless of magnitude:

$$\text{If } a_1 > a_2, \text{ then } (a_1, b_1, c_1) > (a_2, b_2, c_2) \quad \forall b, c$$

Universal selectors (`*`), combinators (`+`, `>`, `~`, space), and scope boundaries contribute **zero** weight $(0, 0, 0)$.

#### Specificity Behavior of Functional Pseudo-Classes

* **`:is()`, `:not()`, `:has()`**: Contribute zero weight themselves. Instead, they inherit the specificity vector of the most specific selector in their comma-separated argument list.
  $$\text{Specificity of } :not(p, \#\text{main}) = \max(\text{Specificity}(p), \text{Specificity}(\#\text{main})) = (1, 0, 0)$$
* **`:where()`**: Always evaluates to $(0, 0, 0)$, completely ignoring the specificity of any arguments inside its list.
* **`:nth-child(An+B of S)`**: Contributes $(0, 1, 0)$ for the pseudo-class itself, plus the specificity of the most specific selector in list $S$.

#### Key Quirks and Constraints of the `:not()` Pseudo-Class

* **Argument Rules**: Requires a list of simple, compound, or complex selectors. Pseudo-elements are **prohibited** inside `:not()`.
* **Universal Negation**: Negating standard classes (e.g., `:not(.foo)`) will match every element that lacks `.foo`, **including `<html>` and `<body>`**.
* **Descendant Combinator Nuance**: A rule such as `body :not(table) a` will still select links inside a `<table>` because intermediate structural elements (`<tr>`, `<tbody>`, `<td>`) match `:not(table)`. To target links not inside tables, use `body a:not(table a)`.
* **Rule Invalidation & Resilience**: If any selector in a `:not()` argument list is invalid or unsupported, the entire CSS rule is invalidated. To make the rule forgiving, wrap arguments in `:is()`, e.g., `:not(:is(.foo, :invalid-pseudo))`.

| Selector Expression | ID Count ($a$) | Class Count ($b$) | Type Count ($c$) | Specificity Vector $(a,b,c)$ |
| :--- | :--- | :--- | :--- | :--- |
| `*` | 0 | 0 | 0 | $(0, 0, 0)$ |
| `li` | 0 | 0 | 1 | $(0, 0, 1)$ |
| `ul li` | 0 | 0 | 2 | $(0, 0, 2)$ |
| `h1 + *[rel=up]` | 0 | 1 | 1 | $(0, 1, 1)$ |
| `ul ol li.red` | 0 | 1 | 3 | $(0, 1, 3)$ |
| `li.red.level` | 0 | 2 | 1 | $(0, 2, 1)$ |
| `:where(#nav) a.link` | 0 | 1 | 1 | $(0, 1, 1)$ |
| `#x34y` | 1 | 0 | 0 | $(1, 0, 0)$ |
| `:is(p, .card, #hero)` | 1 | 0 | 0 | $(1, 0, 0)$ |
| `#mainNav .item:hover` | 1 | 2 | 0 | $(1, 2, 0)$ |
| `#mainNav#mainNav` | 2 | 0 | 0 | $(2, 0, 0)$ |

---

### Module 4: Inheritance Dynamics and Universal Value Keywords

Inheritance propagates computed property values from parent nodes to child nodes along the document tree. Text nodes are treated as element children that inherit all values via defaulting. Inheritance follows the document tree structure and is **not intercepted by anonymous boxes**.

#### Inherited vs. Non-Inherited Properties

* **Inherited Properties**: Primarily typography, text presentation, and list attributes (e.g., `color`, `font-family`, `font-size`, `line-height`, `text-align`, `visibility`). Automatically inherit parent computed values when no cascaded value exists.
* **Non-Inherited Properties**: Structural layout, sizing, positioning, borders, margins, padding, and display settings (e.g., `width`, `height`, `margin`, `padding`, `border`, `display`). Fall back to specification `initial` values when no cascaded value exists.

#### The 5 Universal Property Value Keywords

Any CSS property can explicitly accept the following universal keywords:

1. **`inherit`**: Forces an element to adopt the computed property value of its parent node, enabling explicitly forced inheritance for non-inherited properties. If applied to the root element, it assigns the property's initial value.
2. **`initial`**: Sets the property directly to its specification-defined initial default value, bypassing parent inheritance.
3. **`unset`**: Acts dynamically based on property type: functions as `inherit` for naturally inherited properties, and as `initial` for non-inherited properties.
4. **`revert`**: Rolls back property resolution to the value defined by the User or User Agent origin, stripping away author-level modifications.
5. **`revert-layer`**: Rolls back the property value to the matching declaration present in a preceding cascade layer within the same origin. *(Note: Marked as at-risk in Candidate Recommendation specifications).*

---

### Module 5: Box Model Physics, Margin Collapsing, and Formatting Contexts

Every element in the visual formatting model is structured as a set of concentric rectangular regions: Content, Padding, Border, and Margin.

```
+-----------------------------------------------------------------+
| MARGIN                                                          |
|   +---------------------------------------------------------+   |
|   | BORDER                                                  |   |
|   |   +-------------------------------------------------+   |   |
|   |   | PADDING                                         |   |   |
|   |   |   +-----------------------------------------+   |   |   |
|   |   |   | CONTENT                                 |   |   |   |
|   |   |   |                                         |   |   |   |
|   |   |   +-----------------------------------------+   |   |   |
|   |   +-------------------------------------------------+   |   |
|   +---------------------------------------------------------+   |
+-----------------------------------------------------------------+
```

#### Box Sizing Models

* **Content-Box (`box-sizing: content-box`)**: Default model. Declared `width` and `height` apply strictly to the inner Content region. Applied padding and borders add outward, increasing the rendered footprint.
  $$\text{Rendered Width} = \text{width} + \text{padding}_{\text{left}} + \text{padding}_{\text{right}} + \text{border}_{\text{left}} + \text{border}_{\text{right}}$$
  $$\text{Total Spatial Footprint} = \text{Rendered Width} + \text{margin}_{\text{left}} + \text{margin}_{\text{right}}$$
* **Border-Box (`box-sizing: border-box`)**: Modern model. Declared `width` and `height` encompass content, padding, and border. Inner content shrinks to absorb padding and border dimensions.
  $$\text{Rendered Width} = \text{width}$$
  $$\text{Inner Content Width} = \text{width} - (\text{padding}_{\text{left}} + \text{padding}_{\text{right}} + \text{border}_{\text{left}} + \text{border}_{\text{right}})$$

#### Vertical Margin Collapsing Mathematics

Adjacent vertical margins of block-level boxes in normal flow combine into a single collapsed margin based on the following mathematical rules:

* **Both Positive**:
  $$\text{Margin}_{\text{collapsed}} = \max(M_1, M_2)$$
* **Both Negative**:
  $$\text{Margin}_{\text{collapsed}} = \min(M_1, M_2) \quad \text{(selects the most negative value)}$$
* **Mixed (One Positive, One Negative)**:
  $$\text{Margin}_{\text{collapsed}} = \max(M_{\text{pos}}) + \min(M_{\text{neg}})$$

#### Suppression of Margin Collapsing

Margin collapsing does **not** occur under the following structural conditions:
1. Elements in Flex Formatting Contexts (`display: flex | inline-flex`).
2. Elements in Grid Formatting Contexts (`display: grid | inline-grid`).
3. Elements establishing a new Block Formatting Context (e.g., `display: flow-root`, `overflow: hidden`).
4. Elements participating in multi-column layout contexts.
5. Presence of intervening vertical padding or borders between parent and child elements.

#### Primary Formatting Contexts

* **Block Formatting Context (BFC)**: Triggers include `display: flow-root` or `overflow: hidden`. Stacks boxes vertically, encapsulates internal floats, and prevents vertical margin collapsing across container boundaries.
* **Inline Formatting Context (IFC)**: Lays out elements horizontally along line boxes, wrapping automatically when horizontal capacity is reached.
* **Flex Formatting Context (FFC)**: Triggered by `display: flex`. Establishes a 1D layout engine distributing space dynamically along main and cross axes.
* **Grid Formatting Context (GFC)**: Triggered by `display: grid`. Establishes a 2D matrix engine aligning elements across simultaneous row and column tracks.

---

## Section 2: Short-Answer Practice Questions & Answer Key

### Practice Questions

1. What are the six operational stages of the CSS value processing pipeline, in correct order?
2. How does the presence of an `!important` annotation alter the cascade precedence among User Agent, User, and Author origins?
3. In what order do normal vs. `!important` declarations sort across different `@layer` cascade layers?
4. Calculate the specificity vector $(a, b, c)$ for the selector `ul ol li.red`.
5. Why does the selector `:where(#nav) a.link` have a lower specificity than `#x34y`?
6. Describe how the specificity of the `:not()` functional pseudo-class is determined.
7. What is the computed value outcome when a child element inherits a relative length property (such as `font-size: 130%`) from a parent with `font-size: 10pt`?
8. Explain the dynamic behavior of the universal keyword `unset`.
9. Write the formula for the rendered visual width of an element configured with `box-sizing: content-box`.
10. Calculate the collapsed vertical margin between two adjacent block elements where the top element has `margin-bottom: 30px` and the bottom element has `margin-top: -15px`.
11. Name three layout environments or CSS triggers that completely prevent vertical margin collapsing.
12. What takes precedence in the cascade hierarchy: an active CSS Keyframe animation rule or an author style marked `!important`?

---

### Answer Key

1. **The six operational stages** are: Declared Value, Cascaded Value, Specified Value, Computed Value, Used Value, and Actual Value.
2. **`!important` origin inversion**: Under normal conditions, Author > User > User Agent. When `!important` is applied, the origin priority reverses completely: User Agent `!important` > User `!important` > Author `!important`.
3. **Cascade Layering sorting**:
   * For *normal* rules, unlayered styles override layered styles, and later-declared layers override earlier-declared layers.
   * For *`!important`* rules, layered styles override unlayered styles, and earlier-declared layers override later-declared layers.
4. **Specificity calculation for `ul ol li.red`**:
   * IDs ($a$) = 0
   * Classes/Attributes/Pseudo-classes ($b$) = 1 (`.red`)
   * Types/Pseudo-elements ($c$) = 3 (`ul`, `ol`, `li`)
   * **Vector**: $(0, 1, 3)$.
5. **`:where()` specificity**: The `:where()` pseudo-class strips all internal argument specificity to $(0, 0, 0)$. Thus, `:where(#nav) a.link` evaluates to $(0, 1, 1)$ ($b=1$ for `.link`, $c=1$ for `a`). The selector `#x34y` contains an ID selector, evaluating to $(1, 0, 0)$, which dominates $(0, 1, 1)$ lexicographically.
6. **`:not()` specificity**: `:not()` contributes zero specificity itself, but inherits the specificity vector of the most specific selector inside its argument list (identical to `:is()`).
7. **Inherited computed value**: Inheritance propagates computed values. $130\% \times 10\text{pt} = 13\text{pt}$. The parent's computed value of `13pt` becomes both the specified and computed value for the child element.
8. **Behavior of `unset`**: `unset` acts as `inherit` if applied to a naturally inherited property (e.g., `color`), and as `initial` if applied to a non-inherited property (e.g., `width`).
9. **`content-box` rendered width formula**:
   $$\text{Rendered Width} = \text{width} + \text{padding}_{\text{left}} + \text{padding}_{\text{right}} + \text{border}_{\text{left}} + \text{border}_{\text{right}}$$
10. **Mixed margin collapsing math**:
    $$\text{Margin}_{\text{collapsed}} = \max(M_{\text{pos}}) + \min(M_{\text{neg}}) = 30\text{px} + (-15\text{px}) = 15\text{px}$$
11. **Triggers suppressing margin collapsing**: Flex Formatting Contexts (`display: flex`), Grid Formatting Contexts (`display: grid`), establishing a new BFC (`display: flow-root` or `overflow: hidden`), or inserting vertical padding/borders between parent and child elements.
12. **Keyframes vs. Author `!important`**: An Author declaration marked `!important` (Precedence Rank 5) takes precedence over an active CSS Keyframe Animation rule (Precedence Rank 4). Keyframe animations yield to all `!important` rules.

---

## Section 3: Deep-Dives & Essay Prompts

### Prompt 1: The Dual Role of `!important` Across Cascade Origins and Cascade Layers
*Examine how the `!important` annotation alters standard cascade mechanics. Trace its impact across User Agent, User, and Author origins, as well as its interaction with normal and layered `@layer` styles and CSS animations/transitions.*

#### Key Architectural Points to Include
* Explain that `!important` is not merely a local specificity multiplier, but an authority-reversing operational flag.
* Detail the standard vs. `!important` origin hierarchy, explaining why User Agent and User `!important` rules must override Author `!important` rules to guarantee accessibility and system safety defaults.
* Contrast the layer sorting rules: Normal rules favor unlayered styles and later layers; `!important` rules favor layered styles and earlier layers. Explain how this allows baseline system layers to maintain unblockable safety constraints.
* Position active CSS keyframe animations (yielding to all `!important` rules) and active CSS transitions (overriding all rules, including `!important`) within the full 8-tier precedence hierarchy.

---

### Prompt 2: Specificity Vector Evaluation and Functional Pseudo-Class Mechanics
*Analyze the vector model $\vec{S} = (a, b, c)$ used for calculating selector specificity. Compare traditional selector counting with the spec-defined behavior of functional pseudo-classes (`:is()`, `:where()`, `:not()`, `:has()`, and `:nth-child()`).*

#### Key Architectural Points to Include
* Define the vector components $(a, b, c)$ and explain lexicographical comparison rules ($a$ dominates $b$, $b$ dominates $c$).
* Contrast the specificity inheritance of `:is()`, `:not()`, and `:has()` (which adopt the maximum specificity of their argument list) against `:where()` (which forces specificity to $(0, 0, 0)$).
* Explain practical architectural applications, such as using `:where()` to build low-specificity design-system defaults that developers can override effortlessly without specificity escalation.
* Detail the specific vector addition of `:nth-child(An+B of S)` ($(0, 1, 0) + \max(\text{Specificity}(S))$).
* Highlight structural quirks of `:not()`, including rule invalidation caused by invalid arguments and how wrapping arguments in `:is()` resolves invalidation.

---

### Prompt 3: The CSS Value Processing Pipeline and Defaulting Engines
*Trace the transformation of a CSS property value from raw stylesheet parsing to final hardware display rasterization. Detail the inputs, mathematical/logical calculations, and outputs for all six value stages.*

#### Key Architectural Points to Include
* Step sequentially through Declared, Cascaded, Specified, Computed, Used, and Actual values.
* Explain the defaulting process when no cascaded value exists, distinguishing between naturally inherited properties (using parent computed values) and non-inherited properties (using specification initial values).
* Describe why the Computed Value stage must resolve units like `rem` or relative URLs into absolute terms *before* spatial layout occurs, and why text nodes inherit computed values.
* Explain the layout dependencies evaluated during the Used Value stage (such as percentage widths calculated against containing block geometry).
* Detail physical environment constraints applied during the Actual Value stage, such as sub-pixel rounding for physical display density.

---

### Prompt 4: Box Model Geometry, Margin Collapsing Mathematics, and Formatting Contexts
*Compare the visual box geometry models (`content-box` vs. `border-box`) and provide a detailed architectural analysis of vertical margin collapsing math and structural layout primitives.*

#### Key Architectural Points to Include
* Contrast spatial footprint equations for `box-sizing: content-box` and `box-sizing: border-box`.
* State the exact mathematical formulas governing vertical margin collapsing across positive, negative, and mixed margin combinations.
* Detail the structural conditions that prevent margin collapsing (Flexbox, Grid, Multi-column, and BFC establishment via `display: flow-root` or `overflow: hidden`).
* Compare the dimensional behaviors and spatial alignment controls of Block Formatting Contexts (BFC), Inline Formatting Contexts (IFC), Flex Formatting Contexts (FFC), and Grid Formatting Contexts (GFC).

---

## Section 4: Comprehensive Glossary of Terms

* **Actual Value**: The final stage of the CSS value processing pipeline, representing the used value after user agent approximations and physical hardware display constraints (such as pixel rounding) have been applied.
* **Author Style Sheet**: Styles specified by application developers within document stylesheets, inline `style` attributes, or embedded style blocks.
* **Block Formatting Context (BFC)**: An isolated 1D vertical visual formatting environment that stacks block-level boxes sequentially, encapsulates internal floating elements, and prevents vertical margin collapsing across its boundary.
* **Border-Box (`box-sizing: border-box`)**: A box sizing model where an element's declared `width` and `height` include content, padding, and borders simultaneously.
* **Cascade**: The multi-tiered sorting algorithm used by browser engines to resolve conflicts among competing style declarations targeted at document elements.
* **Cascade Layers (`@layer`)**: A CSS mechanism introduced in Level 5 that establishes explicit architecture-level priority layers within an origin, sorting styles independently of selector specificity.
* **Cascaded Value**: The single victorious declaration that emerges from the cascade sorting algorithm. If no declarations match, no cascaded value exists.
* **Computed Value**: The third processing stage, where relative units (`rem`, `em`) and relative addresses are converted into absolute values without requiring spatial layout context. This is the value passed to child nodes during inheritance.
* **Content-Box (`box-sizing: content-box`)**: The default box sizing model, where declared `width` and `height` apply exclusively to the inner content rectangle, causing applied padding and borders to expand the rendered footprint.
* **Declared Value**: Syntactically valid CSS style declarations that match a target element and satisfy media/feature conditional queries.
* **Defaulting**: The process of assigning a specified value when no cascaded value exists for an element property, operating via parent inheritance or fallback to initial specification values.
* **Flex Formatting Context (FFC)**: A 1D axis-driven layout environment established by `display: flex` that dynamically distributes available space and aligns items along main and cross axes.
* **Grid Formatting Context (GFC)**: A 2D matrix layout environment established by `display: grid` that coordinates element positioning across intersecting horizontal row and vertical column tracks.
* **Inline Formatting Context (IFC)**: A visual layout environment that arranges elements horizontally along line boxes, wrapping automatically when horizontal spatial capacity is exhausted.
* **Inherited Property**: A property category (primarily governing typography, text, and list formatting) whose computed value automatically propagates from parent nodes to child nodes in the absence of an explicit cascade declaration.
* **Initial Value**: The default baseline value assigned to a CSS property as defined in its official W3C specification.
* **Margin Collapsing**: The intrinsic CSS layout behavior where adjacent vertical margins of block-level boxes in normal flow combine into a single collapsed margin.
* **Negation Pseudo-Class (`:not()`)**: A functional functional pseudo-class that matches elements that do not match its argument list of selectors.
* **Non-Inherited Property**: A property category (encompassing structural layout, borders, margins, padding, and display settings) that falls back to its specification `initial` value rather than propagating down the document tree.
* **Specified Value**: The value determined during defaulting, resulting either from cascade victory, parent inheritance, or initial value fallback.
* **Specificity**: A calculated numeric weight vector tuple $\vec{S} = (a, b, c)$ used to sort competing rules within the same origin, importance, and cascade layer.
* **Used Value**: The stage in the value pipeline where layout-dependent relative metrics (such as percentage widths) are converted into absolute pixel dimensions based on containing block geometry.
* **User Agent Style Sheet**: Default baseline styles provided natively by the browser to establish standard element rendering rules.
* **User Style Sheet**: Styles configured by end-users to adapt document presentation to personal needs or accessibility requirements.

## Relacionados
- [[02 - Frontend/02 - HTML|HTML]]
- [[02 - Frontend/04 - Layout|Layout]]
- [[02 - Frontend/05 - DOM|DOM]]

---
← [[02 - Frontend/02 - HTML|HTML]] · [[02 - Frontend/00 - Índice Frontend|Índice Frontend]] · [[02 - Frontend/04 - Layout|Layout]] →
