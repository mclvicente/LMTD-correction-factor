# LMTD Correction Factor Calculator

A simple MATLAB script to calculate the LMTD correction factor ($F_t$) for shell-and-tube heat exchangers.

### Why use this?
Reading $F_t$ values manually from textbook charts is tedious and prone to human visual error. This script gives you exact numerical values instantly, eliminating chart interpolation.

### Method & Formulas
* **Single Shell (1-2 pass):** Based on the analytical formulas from **Underwood (1934)** and **Bowman, Mueller & Nagle (1940)**.
* **N Shells in Series:** Extends the calculation to multiple shells ($2\text{--}4$, $3\text{--}6$, $4\text{--}8$, etc.) using the equivalent shell effectiveness method by **Ahmad et al.**
* **Handles Edge Cases:** Includes checks for special conditions (like $R = 1$) to prevent division-by-zero errors.
