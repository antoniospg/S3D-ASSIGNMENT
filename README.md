# L-Trees
A simple 3D L-System that can easily generate trees and bushes

![Overview](img/ovw.png)
**Figure 1**: Fractal trees, generated using the l-systems approach. From left to right: An ordinary tree, a bush, a seaweed, a sympodial tree and a willow.

## Overview

The common way to model a tree involves manually construction of these and demands high skills and a great amount of time for the person doing this, and, generally, random fluctuations need to be done individually without compromising the tree's species indentity.
A procedural approach can effectively automate the generation, using predetermined instructions acting on an initial state, we can also include random parameters in the instructions to create variation between the trees.

![](img/gif.gif)

The main objective of this assingment is to use Blender software to create a system for the procedural generation of 3D Trees using the L-Systems approach. To achive this goal, besides the basic L-System concepts, other techniques were also used, some of them are:

* Stochastic rules
* Parametric rules
* Tropism
* Bezier curve for the model

The fisrt section is dedicated to describe the procedural rules to generate the tree, while the second one for the surface's modelling.

## Generation

The common base of every system is to define a grammar G = (V, ω, P), where V is a set of symbols that can and cannot be replaced, ω (axiom) is the first sequence of symbols from V and P is the set of rules that rewrite a symbol of V for a sequence of symbols. The sequence starts as a string defined by ω and after each iteration the symbols of that string are replaced according to the rules defined in P.
This string can be interpreted as a sequence of commands to a turtle, who will move across the screen, drawing the tree. The code bellow shows the rules for the seaweed model shown in the title.
```
Axiom: F
Rules: ( F -> FF+[^F&F&F]-[&F^F^F]n[&f&f^f] ) 
``` 
The interpretaion for some of the symbols are:
```
F(l) or f(l):	 Move turtle forward by l, drawing the tree.
+(a):		 Turn turtle left by a.
-(a):		 Turn turtle right by a.
&(a):		 Pitch turtle down by a.
^(a):		 Pitch turtle up by a.
/(a):		 Roll turtle right by a.
n(a):		 Roll turtle left by a.
[: 		 Start branch.
]:		 End branch
```
Obs: Note that in this grammar, a and l are default values.


<div style="float: right">
<img src = "img/gif.gif">
<div>
This is the base for the generation of the tree, each model has it's own grammar, with it's own parameters, some of them uses others techniques, tha will be described in the sections bellow.
</div>
</div>
teste

### Stochastic L-Systems

We can set multiple rules for the same symbol, assigning to each one a probability to occur. In this assingment, we introduce this concept to the willow model, defining two different rules for the branching creation, the first one creates a single continous stem, while the other one creates a double stem. The result is shown in the figures bellow:

<div style="float: right">
<img src = "img/st1.png" height="160" width="319"> 
<img src = "img/st2.png" height="160" width="319"> 
</div>


### Parametric L-Systems

### Tropism



## Welcome to GitHub Pages

You can use the force [editor on GitHub](https://github.com/antoniospg/S3D-ASSINGMENT/edit/gh-pages/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Itali c_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/antoniospg/S3D-ASSINGMENT/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
