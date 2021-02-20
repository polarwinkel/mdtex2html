# mdtex2html
python3-library to convert Markdown with included LaTeX-Formulas to HTML with MathML

## What is this?

`mdtex2html` is a library to convert (Github-flavored) Markdown-Code with includes LaTex-formulas to HTML-Source. The Formulas are converted to MathML-Code.

An inline-formula can either start and end with `$` or it can start with `\(` and end with `\)`, according to valid LaTeX-Code. Block-formulas either start and end with `$$` or start with `\[` an end with `\]`.

An example that `mdtex2html` will convert:

```
# Example-Title

TeX-Formula: $\sqrt2=x^2 \Rightarrow x=\sqrt{\sqrt{2}}$

- This
- is
    - a List

Delete this and write your own `mdTeX`!
```

## Limitations

The Firefox browser will display the result smoothly, as well as Safari (according to user reports).

Just be aware, that the Cromium-engine still is not able to render MathML, but rumors say that in 2020 work has started again to make that happen, so maybe you want to check the status there.
