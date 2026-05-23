# Typst Template Updates & Technical Notes

This document summarizes the changes made to the homework template and explains the technical constraints encountered.

## 1. Automatic Equation Unnumbering

### The Problem
In homework assignments, equations within Question (`שאלה`) and Section (`סעיף`) blocks usually don't need numbering, as they are part of the problem statement. Manually wrapping every equation in `#nonum(...)` was repetitive.

### The Solution
Modified `typst/templates/hw.typ` to include a local `set` rule within the function definitions:

```typst
#let שאלה(כותרת: "", מזהה: none, טקסט) = {
  // ...
  showybox(
    // ...
    {
      set math.equation(numbering: none)
      טקסט
    }
  )
}
```

This scoped rule ensures all equations inside these blocks are unnumbered by default, while equations in the rest of the document (like Answers) remain numbered.

---

## 2. Label Attachment Fix

### The Problem
Attempts to join a label (`מזהה`) to a heading using the `+` operator or standard variable placement caused compilation errors:
- `error: cannot join content with label`
- `error: cannot add content and label`

### The Solution
Used Typst's markup joining syntax to safely attach the optional label to the heading element:

```typst
[#heading(level: 1, supplement: [שאלה])[שאלה] #מזהה]
```

This ensures that if `מזהה` is provided (e.g., `<q1>`), it is correctly anchored to the heading for referencing.

---

## 3. Why Labels Can't Be Created Automatically

A common request is to have the template automatically generate labels like `<שאלה-1>` so they don't have to be passed manually. However, this is currently **not possible** in Typst for several reasons:

### A. Labels are Syntactic Sugar
In Typst, labels (like `<label>`) are special tokens that are resolved during the early stages of compilation. You cannot "construct" a label from a string at runtime. 
For example:
- `label("שאלה-" + str(num))` is **not** the same as `<שאלה-1>`.
- You cannot use a string-constructed label with the `@` symbol.

### B. Pure Functionality
Typst functions are generally "pure." A function cannot "decide" to create a global identifier that the rest of the document can reference unless it is explicitly defined in the markup.

### C. Reference Ambiguity
Even if we could generate them, Typst wouldn't know how to resolve `@שאלה-1` if the label wasn't physically present in the source code at the time of parsing.

### Current Workaround
You must continue to pass labels explicitly if you wish to reference them:
```typst
#שאלה(מזהה: <q1>)[ ... ]
// Reference as:
ראה @q1.
```

---

## 4. Compilation Commands
To compile correctly from the project root while respecting absolute paths:
```powershell
typst compile --root . 2026S/Quantum1/HW/HW01/main.typ
```
