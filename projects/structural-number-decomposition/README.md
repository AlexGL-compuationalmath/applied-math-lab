# Structural Number Decomposition (SND)

Structural Number Decomposition (SND) is an algorithm that represents a positive real number in an interpretable structural form by combining **binary scaling** with **simple rational approximation**.

The goal is to describe numbers not only numerically, but **structurally**.

---

## Idea

Every positive real number can be written exactly as

x = m · 2^k

where:

- k ∈ Z is the **binary scale**
- m ∈ [1,2) is the **normalized mantissa**

This decomposition corresponds to the normalization used in floating point systems.

The SND algorithm adds a second step: it searches for a **simple rational approximation** of the mantissa.

m ≈ p/q

with small integers p and q.

The final structural representation becomes

x ≈ (p/q) · 2^k

---

## Example

Example number:

x = 13.3

Binary normalization:

13.3 = 1.6625 · 2^3

Search for a simple rational close to 1.6625:

5/3 = 1.6667

Final representation:

13.3 ≈ (5/3) · 2^3

---

## Algorithm

Given a number x > 0:

1. Compute binary normalization

k = floor(log2(x))

m = x / 2^k

2. Generate candidate rational numbers

r = p/q

with bounded numerator and denominator.

3. For each candidate compute

- relative error  

error = |m - r| / m

- symbolic complexity  

complexity = p + q

4. Define a score function

score = α · error + β · complexity

5. Select the candidate with the smallest score.

---

## Output

The algorithm returns:

Binary representation

x = m · 2^k

Structural approximation

x ≈ (p/q) · 2^k

with the corresponding approximation error.

---

## Why this is interesting

Traditional floating-point representations focus on **precision**.

SND instead focuses on **interpretable structure**.

It attempts to answer:

> Is this number close to a simple mathematical form?

Examples:

| Number | Structural representation |
|------|------|
| 12 | (3/2) · 2³ |
| 10 | (5/4) · 2³ |
| 6 | (3/2) · 2² |

---

## Future Extensions

Possible improvements:

- include special constants (√2, φ, π fractions)
- use continued fractions for candidate generation
- symbolic complexity metrics
- multi-base decompositions

---

## Author

Alex GL  
Applied Math Lab
