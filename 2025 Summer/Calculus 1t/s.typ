// 1. Import the ctheorems package and apply its show rules
#import "@preview/ctheorems:1.1.3": thmbox, thmrules
#show: thmrules.with(qed-symbol: $square$) // Applies theorem styling, QED symbol is optional

// 2. Define your custom 'theorem' environment
// The crucial change is adding `base_level: 1`.
// This instructs `ctheorems` to only use the *first level* of the heading
// (e.g., '1' from '1.1') for its numbering base.
#let theorem = thmbox(
  "theorem",              // This is the unique identifier for the internal counter for theorems
  "Theorem",              // This is the displayed name of the environment (e.g., "Theorem 1.1")
  fill: rgb("#e8e8f8"),   // Optional: adds a light blue background fill to the theorem box
  inset: (x: 1.2em, top: 1em, bottom: 0.8em), // Optional: adds padding inside the theorem box
  radius: 4pt,            // Optional: rounds the corners of the theorem box
  // --- This is the key change: ---
  base_level: 1           // Limits the numbering base to only the first heading level [1, 2].
)

// 3. Configure document headings to be numbered (e.g., "1.", "1.1", "2.", etc.)
#set heading(numbering: "1.1") // Setting for multi-level heading numbering

// 4. Implement the crucial show rule to reset the 'theorem' counter
// whenever a new level 1 heading appears.
#show heading.where(level: 1): it => {
  // Reset the "theorem" counter to 0 at the start of every top-level heading.
  // The identifier "theorem" must match the one used in `thmbox` above.
  counter("theorem").update(0)
  it // Render the heading itself
}

// --- Example Document Content to Demonstrate Numbering ---

= Introduction to Real Analysis // This is heading 1.
#lorem(20) // Some placeholder text

#theorem[
  Every convergent sequence of real numbers is a Cauchy sequence.
] // This will be Theorem 1.1

#theorem[
  The set of rational numbers is dense in the set of real numbers.
] // This will be Theorem 1.2

== Intermediate Concepts // This is heading 1.1, a level 2 heading
#lorem(15)

#theorem[
  The Bolzano-Weierstrass theorem states that every bounded sequence in $bb(R)^n$ has a convergent subsequence.
] // **This will now be Theorem 1.3** (sequential within top-level 1, ignoring the '1.1' sub-heading)

= Advanced Topics in Calculus // This is heading 2.
#lorem(30) // Some placeholder text. This is the second level 1 heading.

#theorem[
  If a function $f$ is differentiable at a point $a$, then $f$ is continuous at $a$.
] // **This will be Theorem 2.1** (counter reset for new level 1 heading)

#theorem[
  The Fundamental Theorem of Calculus establishes a connection between the two main branches of calculus: differential calculus and integral calculus.
] // This will be Theorem 2.2

=== Further Exploration // This is heading 2.1.1, a level 3 heading under heading 2.1 (not explicitly defined)
#lorem(10)

#theorem[
  The Mean Value Theorem states that if a function is continuous on a closed interval and differentiable on the open interval, then there exists a point in that interval where the instantaneous rate of change equals the average rate of change.
] // **This will be Theorem 2.3**, matching your desired numbering.