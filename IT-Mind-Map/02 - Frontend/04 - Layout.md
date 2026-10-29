---
title: "Layout"
area: "Frontend"
numero: 4
aliases: ["Layout"]
tags: [concepto, it/frontend]
---
# Layout

> **Área:** [[02 - Frontend/00 - Índice Frontend|Índice Frontend]] · **Concepto 4 de 25**

## Qué abarca
- Flexbox
- Grid
- posicionamiento
- responsive

## Mis notas
<!-- ai:start -->
# Modern Web Layout Architecture: Comprehensive Study Guide

This study guide provides a structured analysis of modern CSS layout specifications, geometric calculations, positioning systems, and responsive design paradigms based on technical documentation and authoritative web standards.
<!-- ai:end -->

---

## 1. Key Concepts Review

### Module 1: Flexible Box Layout (Flexbox)

#### Core Axes and Flow Direction
*   **Dimensional Model:** Flexbox is a one-dimensional layout system designed to distribute space and align items along a primary axis (**main axis**) and an perpendicular axis (**cross axis**).
*   **Directional Mapping:** The layout direction is governed by `flex-direction` (`row`, `row-reverse`, `column`, `column-reverse`).
*   **Writing Mode Relativity:** Alignment relies on abstract directions (`main-start`, `main-end`, `cross-start`, `cross-end`) rather than fixed physical boundaries (left, right, top, bottom).
    *   *Example:* In `flex-direction: row`, an English layout (Left-to-Right) places `main-start` on the left and `main-end` on the right. In an Arabic layout (Right-to-Left), `main-start` is on the right and `main-end` is on the left. In both horizontal writing modes, `cross-start` is at the top and `cross-end` is at the bottom.

#### Sizing Algorithms and Free Space Calculation
The final geometry of a flex item is computed dynamically by calculating the positive or negative free space in the flex container:
1.  **Base Sizing (`flex-basis`):** Defines the initial size of an item before space distribution. 
    *   Default value is `auto`. If `auto` is set, the rendering engine checks for an explicit `width` or `height`. If none exists, `auto` resolves to `max-content`.
    *   The `content` keyword forces sizing based strictly on content dimensions, ignoring explicit `width`/`height`.
    *   *Critical Case (`flex-basis: 0` vs `flex-basis: 0%`):* In column layouts (`flex-direction: column`) where the container has no explicit height, `0` resolves to an absolute length of `0px`. Conversely, `0%` attempts to resolve relative to the container's height; since the container height is unresolved, `0%` fails and falls back to `content`, causing major layout discrepancies.
2.  **Positive Free Space (`flex-grow`):** When the sum of item bases is less than the container's inner dimension, positive free space exists. The `flex-grow` unitless factor determines the proportional allocation of remaining space.
    *   *Calculation:* If items have growth factors of `1`, `1`, and `2`, the remaining free space is divided into 4 equal portions ($1+1+2$). Items receive 25%, 25%, and 50% of the surplus space, respectively.
3.  **Negative Free Space (`flex-shrink`):** When the sum of item bases exceeds container capacity, negative free space is generated. The `flex-shrink` algorithm weights both the shrink factor **and** the item's original `flex-basis`. Items with larger base sizes shrink faster to preserve relative visual balance. Items will not shrink below their `min-content` size unless `min-width` or `min-height` are explicitly overridden.

#### Flex Shorthands Summary
The specification strongly encourages using the `flex` shorthand property (`flex: <flex-grow> <flex-shrink> <flex-basis>`):

| Shorthand | Full Expansion | Geometric Behavior |
| :--- | :--- | :--- |
| `flex: initial` | `0 1 auto` | Inflexible to growth. Shrinks under negative free space. Uses intrinsic or explicit dimensions. |
| `flex: auto` | `1 1 auto` | Fully flexible. Absorbs positive free space and shrinks under negative free space from base size. |
| `flex: none` | `0 0 auto` | Fully inflexible. Strictly maintains content or explicit width/height dimensions. |
| `flex: <number>` | `<number> 1 0%` | Pure proportional ratios. Sets base to `0%` to ignore content size and distribute space exact to ratios. |

---

### Module 2: CSS Grid Layout & Auto-Placement Mechanics

#### Matrix Dimensions & Implicit vs. Explicit Grid
*   **Two-Dimensional Grid:** CSS Grid manages rows and columns simultaneously within a matrix bounded by grid lines, tracks, areas, and cells.
*   **Explicit Grid:** Defined explicitly via `grid-template-columns` and `grid-template-rows`.
*   **Implicit Grid:** Automatically generated when items are positioned outside explicit track boundaries or placed by the auto-placement algorithm beyond defined cells.
    *   Implicit track sizes are controlled via `grid-auto-columns` and `grid-auto-rows`.
    *   Implicit tracks default to `auto`, sizing themselves to fit content without causing overflow.
    *   Flow direction of implicit tracks is set by `grid-auto-flow` (`row` or `column`).

#### Sizing Functions and Track Algorithms
*   **Fraction Unit (`fr`):** Represents a fraction of available free space after deducting fixed/non-flexible track sizes (e.g., `px`, `em`, `min-content`) from total container dimensions.
*   **`minmax(min, max)`:** Constrains a track within a minimum and maximum range (e.g., `minmax(200px, 1fr)` ensures a track never shrinks below 200px while expanding flexibly).
*   **`fit-content(limit)`:** Clamps track growth using the suppression formula:
    $$\min(\text{max-content}, \max(\text{auto}, \text{limit}))$$
*   **`auto-fill` vs. `auto-fit`:**
    *   `auto-fill`: Creates the maximum possible number of tracks without overflowing the container. Empty tracks are preserved in the visual DOM.
    *   `auto-fit`: Calculates tracks like `auto-fill`, but automatically collapses empty tracks down to `0px` (treating them as fixed 0px tracks and removing adjacent gaps), allowing occupied `1fr` tracks to expand and fill all remaining container space.

#### Grid Auto-Placement Algorithm Rules
1.  **Order Modified Document Order:** Unplaced items are positioned according to the `order` property if present; otherwise, they follow source document (DOM) order.
2.  **Explicit Placement Precedence:** The engine places items with explicit positions (e.g., `grid-column`, `grid-row`) **first**. Auto-placed items then fill remaining open spaces in DOM order without placing themselves prior to already placed items unless dense packing is activated.
3.  **Spanning and Gaps:** When an auto-placed item spans multiple tracks (e.g., `grid-column-end: span 2`), if it encounters a space where it cannot fit, the engine skips to the next row/column, leaving a visual gap.
4.  **Dense Packing (`grid-auto-flow: dense`):** Directs the engine to backfill layout gaps by pulling later items out of DOM order if they fit into earlier visual gaps. *Note: This visually reorders elements without altering DOM or tab keyboard navigation order.*
5.  **Anonymous Grid Items:** Unwrapped strings of text directly inside a grid container become anonymous grid items. They are always handled via auto-placement rules because they cannot be targeted with CSS selectors.

#### Subgrid Integration
*   The `subgrid` value (applicable to `grid-template-columns` and `grid-template-rows`) allows nested grid containers to inherit track definitions and line names directly from the parent grid.
*   Enables multi-column cross-alignment of nested child elements (such as headers, body text, and footers across adjacent cards) regardless of individual text content lengths.

---

### Module 3: Render Contexts, Positioning, & Spatial Mapping

#### Rules of Containing Block Determination
An element's size and offsets (`top`, `right`, `bottom`, `left`) depend on its Containing Block, determined by its `position` value:

1.  **`position: static`, `relative`, or `sticky`:** Containing block is formed by the **content box** of the nearest block-level ancestor.
2.  **`position: absolute`:** Containing block is formed by the **padding box** of the nearest ancestor with a `position` other than `static` (`relative`, `absolute`, `fixed`, or `sticky`). If no such ancestor exists, it defaults to the **initial containing block** (viewport dimensions).
3.  **`position: fixed`:** Containing block is the **initial containing block** (viewport).
4.  **Ancestor Property Overrides:** If an ancestor applies any of the following, it becomes the containing block for **both** `absolute` and `fixed` descendants:
    *   `transform`, `perspective`, or `filter` values other than `none`.
    *   `contain` property set to `layout`, `paint`, `strict`, or `content`.
    *   `container-type` with a dimensional value.

#### Structural Positioning Matrix

| Position Scheme | In Normal Flow? | Offset Reference Point | Creates Internal BFC? |
| :--- | :--- | :--- | :--- |
| `static` | Yes | N/A (Flow and margins) | No |
| `relative` | Yes (Retains DOM space) | Own normal flow position | No |
| `absolute` | No (Removed from flow) | Padding box of positioned ancestor / ICB | Yes (For its content) |
| `fixed` | No (Removed from flow) | Viewport / Special Ancestor | Yes (For its content) |
| `sticky` | Yes (Until scroll threshold) | Normal flow relative to scroll container | No |

#### Block Formatting Context (BFC) Mechanics
A BFC is an isolated rendering region that enforces three structural behaviors:
1.  **Internal Float Containment:** Encloses internal floating elements, preventing container height collapse.
2.  **External Float Isolation:** Prevents element boxes within the BFC from overlapping adjacent external floats.
3.  **Margin Collapse Suppression:** Prevents vertical margins of contained elements from collapsing with external margins.

**Triggers for BFC Creation:** `display: flow-root` (modern standard method), `position: absolute` or `fixed`, `float` other than `none`, non-item Flex/Grid containers, `overflow` other than `visible` or `clip`, and explicit containment (`contain: layout / paint / strict`).

#### Stacking Contexts (Z-Axis Rendering)
Without explicit `z-index` declarations, standard visual rendering follows a bottom-to-top sequence:
1.  Root element background and borders.
2.  Non-positioned elements in DOM order.
3.  Positioned elements in HTML order.

**Triggers for New Stacking Context Formation:**
*   Root element (`<html>`).
*   `position: relative` or `absolute` with `z-index` other than `auto`.
*   `position: fixed` or `sticky`.
*   `opacity` less than `1`.
*   `transform`, `filter`, or `perspective` other than `none`.
*   `isolation: isolate`.
*   `contain: paint` or `contain: layout`.

*Atomic Encapsulation:* Stacking contexts isolate their child layers. A child with `z-index: 9999` nested inside a parent with a lower stacking level will remain visually **behind** a sibling of the parent that has a higher stacking level.

---

### Module 4: Container Queries & Component-Driven Responsiveness

#### Paradigmatic Shift
Traditional Media Queries (`@media`) evaluate the overall browser viewport, which fails to reflect the actual available space of sub-components in modular architectures. Container Queries evaluate the metric context of a parent container.

#### Context Setup & Containment Rules
To establish a containment context, the parent must declare `container-type`:
*   `container-type: inline-size`: Applies inline-size, layout, and style containment. Isolates the element in its inline axis (horizontal in LTR) to prevent infinite layout loops (where child size changes parent size, invalidating child size).
*   `container-type: size`: Applies dimensional containment across both inline and block axes.
*   `container-name`: Optional identifier to target specific containers in `@container` rules.
*   *Shorthand:* `container: <name> / <type>` (e.g., `container: card / inline-size`).

#### Container Query Length Units
Units are calculated as percentages of the query container's dimensions:
*   `cqw`: 1% of query container width.
*   `cqh`: 1% of query container height.
*   `cqi`: 1% of query container inline size.
*   `cqb`: 1% of query container block size.
*   `cqmin`: The smaller value between `cqi` and `cqb`.
*   `cqmax`: The larger value between `cqi` and `cqb`.

---

## 2. Short-Answer Practice Questions

**Question 1:** How does the CSS engine calculate positive free space in a Flexbox container, and what determines how `flex-grow` distributes it?
> **Answer:** Positive free space is calculated as the difference between the flex container's inner main size and the sum of the `flex-basis` values of all child flex items. `flex-grow` distributes this space proportionally based on each item's unitless numerical factor relative to the total sum of all `flex-grow` factors in the container.

**Question 2:** Explain why declaring `flex-basis: 0%` inside a column flex container without an explicit container height causes layout bugs, whereas `flex-basis: 0` does not.
> **Answer:** `flex-basis: 0` is treated as an absolute length of `0px`. `flex-basis: 0%` is a relative percentage that must resolve against the container's height. Because the container height is unconstrained/indefinite, the percentage cannot be calculated and falls back to `content` (intrinsic content size), altering the layout geometry.

**Question 3:** What is the technical difference between `auto-fill` and `auto-fit` in CSS Grid Layout?
> **Answer:** Both evaluate container capacity to create the maximum number of tracks without overflow. However, `auto-fill` preserves empty tracks in the layout, whereas `auto-fit` automatically collapses empty tracks to `0px` and removes their gaps, allowing occupied `1fr` tracks to expand and absorb all remaining space.

**Question 4:** According to the track suppression formula for `fit-content(limit)`, what is the resulting track size if `max-content` is `350px`, `auto` is `150px`, and the `limit` argument is `250px`?
> **Answer:** The formula is $\min(\text{max-content}, \max(\text{auto}, \text{limit}))$.
> 1. Evaluate $\max(150\text{px}, 250\text{px}) = 250\text{px}$.
> 2. Evaluate $\min(350\text{px}, 250\text{px}) = 250\text{px}$.
> The resulting track size is **`250px`**.

**Question 5:** Name three CSS properties that, when declared with values other than `none`, transform an ancestor element into a Containing Block for a `position: fixed` child element.
> **Answer:** Any three of the following: `transform`, `perspective`, `filter`, `contain: layout` (or `paint`/`strict`/`content`), or `container-type` with a dimensional setting (`inline-size` or `size`).

**Question 6:** What are the three core layout problems solved by creating a Block Formatting Context (BFC)?
> **Answer:** A BFC (1) encloses internal floating elements to prevent parent height collapse, (2) isolates internal content from overlapping adjacent external floats, and (3) suppresses vertical margin collapsing across its boundary.

**Question 7:** Why does a child element with `z-index: 9999` sometimes appear visually behind a element with `z-index: 1`?
> **Answer:** This occurs when the child element belongs to a localized Stacking Context created by its parent, and that parent element sits in a lower stacking context relative to the sibling element. Stacking contexts are atomically encapsulated; Z-index values cannot escape their parent context.

**Question 8:** What is `grid-auto-flow: dense` used for, and what accessibility trade-off does it introduce?
> **Answer:** It activates dense packing in the grid auto-placement algorithm, filling layout gaps by placing later DOM items into earlier visual gaps. The trade-off is that it disconnects visual display order from logical DOM/source order, which can disrupt keyboard navigation (tab order) and screen reader user experience.

**Question 9:** How do Anonymous Grid Items originate, and how are they managed by the layout engine?
> **Answer:** They are created when unwrapped strings of text sit directly inside a `display: grid` container without enclosing HTML elements. They cannot be targeted with CSS selectors and are therefore handled strictly through default grid auto-placement rules.

**Question 10:** What is the operational purpose of `container-type: inline-size` in Container Queries?
> **Answer:** It defines an element as a query container along its inline axis while applying layout, style, and inline-size containment. This isolates the container's layout calculations, preventing infinite rendering loops where child modifications alter parent size and re-trigger layout evaluation.

---

## 3. Essay Prompts for Deeper Exploration

1.  **Architectural Layout Decoupling: Grid vs. Flexbox vs. Positioning Systems**
    *   *Prompt:* Analyze the architectural criteria for selecting between CSS Grid, Flexbox, and Absolute Positioning in complex web application development. Compare track-first (2D) and content-first (1D) sizing logic. Detail how combining these layout modes inappropriately leads to structural fragilities such as unnecessary reflows, unwanted overflow bugs, or brittle breakpoint dependencies.

2.  **Context Isolation and Stacking Hydration**
    *   *Prompt:* Discuss the mechanisms of layout encapsulation in modern CSS. Explain how Block Formatting Contexts (BFCs) and Stacking Contexts manage spatial rendering. Detail how modern properties (`display: flow-root`, `isolation: isolate`, `contain`) allow developers to create predictable, component-level layouts without global side effects or `z-index` escalation.

3.  **The Modular Responsive Paradigm: Container Queries and Subgrid Architecture**
    *   *Prompt:* Evaluate the transition from viewport-centric media queries to component-driven design via Container Queries and Subgrid. Explain how `@container` rules combined with `subgrid` solve long-standing structural challenges in design systems (such as card alignment across varying column layouts). Support your analysis with references to containment rules and container unit scales (`cqi`, `cqb`).

---

## 4. Glossary of Important Terms

*   **Anonymous Grid Item:** An unwrapped string of text directly inside a grid container that forms a distinct grid item; it cannot be targeted via CSS and is governed entirely by auto-placement algorithms.
*   **Auto-fit:** A CSS Grid keyword for `repeat()` that creates tracks to fill container space and automatically collapses any empty tracks down to `0px`, allowing filled tracks to grow.
*   **Auto-fill:** A CSS Grid keyword for `repeat()` that creates the maximum number of tracks possible to fit the container width, preserving empty tracks as space in the layout.
*   **Block Formatting Context (BFC):** An isolated rendering region in a Web page where block boxes are laid out, internal floats are contained, margin collapse is suppressed, and external floats are isolated.
*   **Containing Block:** A rectangle that serves as the reference box for determining the position, size, and offsets of an element.
*   **Container Queries:** CSS rules (`@container`) that evaluate the styles and geometry of an ancestor container rather than the overall browser viewport.
*   **Cross Axis:** The axis perpendicular to the main axis in a Flexbox container, governed by `flex-direction`.
*   **Flex-basis:** The property that sets the initial main size of a flex item before space distribution algorithms run.
*   **Flex-grow:** A unitless factor that defines how much of the positive free space in a flex container a flex item will absorb.
*   **Flex-shrink:** A unitless factor that defines how a flex item contracts relative to its size and shrink factor when negative free space is present.
*   **Fraction Unit (`fr`):** A CSS Grid length unit representing a fractional share of the remaining positive free space in the grid container.
*   **Implicit Grid:** Tracks automatically generated by the CSS Grid engine when items are placed beyond the declared `grid-template-*` matrix.
*   **Initial Containing Block:** The top-level containing block formatted to the dimensions of the browser viewport, serving as the default reference for `fixed` and un-parented `absolute` elements.
*   **Inline-size Containment:** A performance and safety constraint that prevents child elements from influencing the inline dimension of their query container, avoiding recursive layout loops.
*   **Main Axis:** The primary axis of a Flexbox container along which flex items are placed, defined by `flex-direction`.
*   **Negative Free Space:** The excess spatial length generated when the total sum of flex items' base sizes exceeds the flex container's inner dimension.
*   **Order Modified Document Order:** The sequential flow order used by CSS layout algorithms, which prioritizes explicit `order` properties over source DOM order.
*   **Positive Free Space:** The remaining unallocated space in a flex container when the sum of flex items' bases is smaller than the container's capacity.
*   **Stacking Context:** A three-dimensional conceptual grouping of elements along the visual Z-axis relative to the user, within which child layers are atomically encapsulated.
*   **Subgrid:** A value for `grid-template-columns` or `grid-template-rows` that allows a nested grid to inherit the track definitions and line names of its parent grid container.

## Relacionados
- [[02 - Frontend/02 - HTML|HTML]]
- [[02 - Frontend/03 - CSS|CSS]]
- [[02 - Frontend/05 - DOM|DOM]]
- [[08 - UX & UI/19 - Responsive Design|Responsive Design]] · *UX / UI*

---
← [[02 - Frontend/03 - CSS|CSS]] · [[02 - Frontend/00 - Índice Frontend|Índice Frontend]] · [[02 - Frontend/05 - DOM|DOM]] →
