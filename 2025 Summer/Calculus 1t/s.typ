// 1. Import the ctheorems package and apply its show rules
#import "@preview/ctheorems:1.1.3": thmbox, thmrules
#show: thmrules.with(qed-symbol: $square$) // Applies theorem styling, QED symbol is optional

#set text(lang: "he", dir: rtl)

// 2. Define your custom 'theorem' environment
// The `thmbox` function by default links its numbering to the current heading structure
// through its `base: "heading"` parameter, which is what we want for "Chapter.Theorem" numbering.
#let theorem = thmbox(
  "theorem", // This is the unique identifier for the internal counter for theorems
  "משפט", // This is the displayed name of the environment (e.g., "Theorem 1.1")
  fill: rgb("#e8e8f8"), // Optional: adds a light blue background fill to the theorem box
  inset: (x: 1.2em, top: 1em, bottom: 0.8em), // Optional: adds padding inside the theorem box
  radius: 4pt // Optional: rounds the corners of the theorem box
)

// 3. Configure document headings to be numbered (e.g., "1.", "2.", etc.)
// This is essential for the "2.3" style numbering to work correctly.
#set heading(numbering: "1.")

// 4. Implement the crucial show rule to reset the 'theorem' counter
// whenever a new level 1 heading appears.
#show heading.where(level: 1): it => {
  // Reset the "theorem" counter to 0 at the start of every top-level heading.
  // The identifier "theorem" must match the one used in `thmbox` above.
  counter("theorem").update(0)
  it // Render the heading itself
}

// --- Example Document Content to Demonstrate Numbering ---

= חדו"א 1ת
#lorem(20) // Some placeholder text

#theorem[
  כל סדרה
] // This will be Theorem 1.1

#theorem[
  The set of rational numbers is dense in the set of real numbers.
] // This will be Theorem 1.2

== כותרת
#lorem(15)

#theorem[
  The Bolzano-Weierstrass theorem states that every bounded sequence in $bb(R)^n$ has a convergent subsequence.
] // This will be Theorem 1.3

= Advanced Topics in Calculus
#lorem(30) // Some placeholder text. This is the second level 1 heading.

#theorem[
  If a function $f$ is differentiable at a point $a$, then $f$ is continuous at $a$.
] // **This will be Theorem 2.1** (counter reset for new level 1 heading)

#theorem[
  The Fundamental Theorem of Calculus establishes a connection between the two main branches of calculus: differential calculus and integral calculus.
] // This will be Theorem 2.2

#theorem[
  For any real number $x$, the exponential function $e^x$ is equal to its own derivative.
] // **This will be Theorem 2.3**, matching your desired numbering.

=== Further Exploration (Under "Advanced Topics in Calculus")
#lorem(10)

#theorem[
  L'Hôpital's Rule can be used to evaluate indeterminate forms of limits.
] // This will be Theorem 2.4