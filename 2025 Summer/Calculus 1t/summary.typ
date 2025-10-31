#import "@preview/ctheorems:1.1.3": *
#show: thmrules
// #import "../../utils.typ": שם-מייל, הרצאה, innerp, Rn, Cn, Rnn, Cnn, קותח

#set text(lang: "he", dir: rtl)

#set page(
  margin: (
    left: 1in,
    right: 1in,
    top: 1in,
    bottom: 1in,
  ),
  columns: 1, // Ensure single column layout for easier reading
)
#set text(lang: "en", font: "New Computer Modern")
#set par(justify: true)

// 1. Initialize a counter for theorems
#let theorem-counter = counter("theorem")

// 2. Initialize a state variable to store all theorems
// It will hold an array of dictionaries, each containing theorem details.
#let all-theorems = state("all-theorems", ())

// 3. Define a custom theorem function
// This function will display the theorem, increment its counter,
// create a unique label, and store its details in the `all-theorems` state.
#let theorem(title, body) = context {
  // Step the theorem counter for the new theorem
  theorem-counter.step()

  // Get the current location in the document. This is crucial for creating clickable links.
  let current-location = here()

  // Format the theorem number (e.g., "1", "1.1" if nested, etc.)
  let theorem-number = theorem-counter.display()

  // Create a unique label for this theorem. Labels are necessary for linking.
  // We use the raw counter value to ensure uniqueness.
  let theorem-label = "thm-" + str(theorem-counter.get().first())

  // Create the full name/title for the theorem list
  let theorem-display-name = "Theorem " + theorem-number + ": " + title

  // Update the global state with the current theorem's information
  // We append a dictionary with the display name, its location, and its unique label.
  all-theorems.update(theorems => theorems + ((
    name: theorem-display-name,
    location: current-location,
    label: theorem-label
  ),))

  // Display the theorem in the main document
  block(
    fill: luma(240), // Light grey background for theorems
    inset: 1em,
    radius: 4pt,
    width: 100%,
    breakable: true, // Allow theorems to break across pages if needed
    [
      *#theorem-display-name* #label(theorem-label) // Display name and attach the unique label
      #body
    ]
  )
}

// 4. Define a function to display the collected list of theorems
#let display-theorems-list() = context {
  // Retrieve the final collected list of theorems from the state
  let theorems = all-theorems.final()

  // Only display the list if there are any theorems
  if theorems.len() > 0 {
    pagebreak() // Start the list on a new page for clarity

    // Heading for the list of theorems
    set heading(level: 1, numbering: none) // No numbering for this specific heading
     //List of Theorems

    // Iterate through each collected theorem and create a clickable list item
    for t in theorems [
      // Create a clickable link that jumps back to the theorem's original location
      // The text of the link is the theorem's display name
      - #link(t.location)[#t.name]
    ]
  }
}

// 5. Integrate the display function at the end of the document
// This #show rule ensures that the list is generated after all document content has been processed.
#show: doc => {
  doc // Renders the main document content first
  display-theorems-list() // Then appends the list of theorems
}

// --- Your Calculus Lecture Notes Start Here ---

= Introduction to Calculus

#lorem(10)

#theorem[The Squeeze Theorem][
  If $f(x) <= g(x) <= h(x)$ for all $x$ in an open interval containing $c$,
  except possibly at $c$ itself, and if $lim_(x->c) f(x) = L$ and $lim_(x->c) h(x) = L$,
  then $lim_(x->c) g(x) = L$.
]

#lorem(10)

#theorem[Intermediate Value Theorem (IVT)][
  If $f$ is a continuous function on a closed interval $[a, b]$,
  and $y_0$ is any value between $f(a)$ and $f(b)$ (inclusive),
  then there is at least one number $c$ in $[a, b]$ such that $f(c) = y_0$.
]

#lorem(10)

= Derivatives

#lorem(10)

#theorem[Product Rule][
  If $f$ and $g$ are differentiable functions, then the derivative of their product is
  $diff/d x (f(x)g(x)) = f'(x)g(x) + f(x)g'(x)$.
]

#lorem(10)

#theorem[Quotient Rule][
  If $f$ and $g$ are differentiable functions, and $g(x) != 0$, then the derivative of their quotient is
  $diff/d x (f(x)/g(x)) = (f'(x)g(x) - f(x)g'(x))/(g(x))^2$.
]

#lorem(10)