# mdtex2html
python3-library to convert Markdown with included LaTeX-Formulas to HTML with MathML

## What is mdtex2html

`mdtex2html` is a library to convert (Github-flavored) Markdown-Code with included LaTex-formulas to HTML-Source. The formulas are converted to MathML.

An inline-formula can either start and end with `$` or it can start with `\(` and end with `\)`, according to valid LaTeX-Code. Block-formulas either start and end with `$$` or start with `\[` and end with `\]`.

An example that `mdtex2html` will convert:

```
# Example-Title

TeX-Formula: $\sqrt2=x^2 \Rightarrow x=\sqrt{\sqrt{2}}$

- This
- is
    - a List with `inline-Code`
```

## How to use mdtex2html

install it, i.e. using pip:

`python3 -m pip install mdtex2html`

then in python import in your code with

`import mdtex2html`

and convert your mdTeX with something like

`mdtex2html.convert('- Hello ${\sqrt{World}}^2$!')`

passing any mdTeX-Code to `mdtex2html.convert()`.

### Extra

You may want to (but don't need to) include this css-snippet on your page to hide error message texts, only showing on mouse-over:

```
.tooltip .tooltiptext {
    display: none;
}
.tooltip:hover .tooltiptext {
    display: inline;
    border-radius: 0.3em;
    background-color: #777;
    position: fixed;
}
```

### Markdown-Extensions

Starting with v1.1 you can use python-markdown-extensions for i.e. tables, definition-lists, html-attributes and much more by passing a list of the extension(s) to be used to the `convert`-command as described in the [python-markdown documentation](https://python-markdown.github.io/extensions/).

For example `mdtex2html.convert('Hello green\n{: style="color:green" }', extensions=['attr_list'])` will make use of the extension `attr_list`.

## Dependencies

This depends on:

- [latex2html](https://github.com/roniemartinez/latex2mathml)
- [Python-Markdown](https://github.com/Python-Markdown/markdown)

The dependencies will be installed when installing using pip.

## Limitations

The Firefox browser will display the result smoothly, as well as Safari (according to user reports).

Just be aware that the Chromium-engine (Browsers: Chrome, Edge, ...) still is not able to render MathML properly, but rumors say that in 2020 work has started again to make that happen, so maybe you want to check the status there.

## Credits

Special thanks to [Ronie Martinez](https://github.com/roniemartinez) for creating [latex2html](https://github.com/roniemartinez/latex2mathml)!

This library is just a few lines of code added to his work and to [Python-Markdown](https://github.com/Python-Markdown/markdown).
