// 1. Import the ctheorems package and apply its show rules
#import "@preview/ctheorems:1.1.3": thmbox, thmrules
#show: thmrules.with(qed-symbol: $square$) // Applies theorem styling, QED symbol is optional

#set text(lang: "he", dir: rtl)
#set heading(numbering: "1.1")

// 2. Define your custom 'theorem' environment
// The `thmbox` function by default links its numbering to the current heading structure
// through its `base: "heading"` parameter, which is what we want for "Chapter.Theorem" numbering.

#let all-theorems = state("all-theorems", ())
#let theorem-counter = counter("theorem")

#let theorem = thmbox(
  "theorem", // This is the unique identifier for the internal counter for theorems
  "משפט", // This is the displayed name of the environment (e.g., "Theorem 1.1")
  fill: rgb("#e8e8f8"), // Optional: adds a light blue background fill to the theorem box
  inset: (x: 1.2em, top: 1em, bottom: 0.8em), // Optional: adds padding inside the theorem box
  radius: 4pt // Optional: rounds the corners of the theorem box
)

#let משפט(body, title: none) = context {
  let current = here()      // location captured *before* the theorem
  let t = theorem(title)[#text(body)]
  t
  // Get the current location in the document. This is crucial for creating clickable links.
  let current-location = here()
  
  // Format the theorem number (e.g., "1", "1.1" if nested, etc.)
  let theorem-number = theorem-counter.display()
  
  // Create a unique label for this theorem. Labels are necessary for linking.
  // We use the raw counter value to ensure uniqueness.
  let theorem-label = "thm-" + str(theorem-counter.get().first())

  // Create the full name/title for the theorem list
  if 1 < 2 {
    
  }
  let theorem-display-name = "Theorem " + theorem-number + ": " + title

  // Update the global state with the current theorem's information
  // We append a dictionary with the display name, its location, and its unique label.
  all-theorems.update(theorems => theorems + ((
    name: theorem-display-name,
    location: current-location,
    label: theorem-label
  ),))

   all-theorems.update(theorems => theorems + ((
    name: theorem-display-name,
    location: current-location,
    label: theorem-label
  ),))
}


// 4. Implement the crucial show rule to reset the 'theorem' counter
// whenever a new level 1 heading appears.
#show heading.where(level: 1): it => {
  // Reset the "theorem" counter to 0 at the start of every top-level heading.
  // The identifier "theorem" must match the one used in `thmbox` above.
  counter("theorem").update(0)
  it // Render the heading itself
}



// --- Example Document Content to Demonstrate Numbering ---
#theorem($x > 4$)[כי $x=3$ כי]
= חדו"א 1ת
#lorem(20) // Some placeholder text



#משפט()[פשוט כי $a² + b² = c²$]

#משפט("פיתגורס")[פשוט כי $a² + b² = c²$]


// #משפט[
  // The set of rational numbers is dense in the set of real numbers.
// ] // This will be Theorem 1.2

== כותרת
#lorem(15)

// #משפט[
//   The Bolzano-Weierstrass theorem states that every bounded sequence in $bb(R)^n$ has a convergent subsequence.
// ] <bs>

= Advanced Topics in Calculus
#lorem(30) // Some placeholder text. This is the second level 1 heading.

// #משפט[
//   If a function $f$ is differentiable at a point $a$, then $f$ is continuous at $a$.
// ] // **This will be Theorem 2.1** (counter reset for new level 1 heading)

// #משפט[
//   The Fundamental Theorem of Calculus establishes a connection between the two main branches of calculus: differential calculus and integral calculus.
// ] // This will be Theorem 2.2

// #משפט[
//   For any real number $x$, the exponential function $e^x$ is equal to its own derivative.
// ] // **This will be Theorem 2.3**, matching your desired numbering.

=== Further Exploration (Under "Advanced Topics in Calculus")
#lorem(10)

// #משפט[
//   L'Hôpital's Rule can be used to evaluate indeterminate forms of limits.
// ] // This will be Theorem 2.4