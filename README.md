## KRT - Knowledge Representation Tool

![](/images/knewt_600.png)

KRT is a tool. A small light library to represents knowledge through graphs. It's goal is to be quick, frictionless way of representing knowledge. It is not prescriptive but a tool that gives the author the ability to describe, represent and evolve their current mental model of a domain. 

## Quick Start 

All you need to get started is a list of tuples representing your edges. 

``` python 
from krt import Graph
from krt.renderers import dot_render, display_graph

g = Graph.from_tuples([("a","b"),("c","d"),("c","d"),("c","b"),("d","e")])
dot_render(g)
```

And that's it. You'll get the following render

![](/images/example_1.png)

## Another Quick Example 

Here's a sentence from a NYT article about painist. 

```
His speech caused a commotion, as audience members called out, both attacking and defending him.
```
 ![](/images/example_2.png)

First step is to parse the sentence. 

```

import spacy
nlp = spacy.load("en")
s =  nlp(u"His speech caused a commotion, as audience members called out, both attacking and defending him.")
```

Then create your list of tuples.  In this example I used my parser of choice (SPACY) and removed punctuation. 

```
g  = Graph.from_tuples ( [ (t.head, t) for t in s  if t.pos_ not in [u'PUNCT']])
dot_render(g)

```

### Example 1 : New York Times  

![](/images/krt_nytimes_600.png)  


### Example 2 : Hadoop Code Base 

TBD 


### After thoughts 

Domain Representation Tool. (DRT). KRT is a cartography for the mind. At least that's what it attempts to be. 


* descriptive ( vs prescriptive) 
* exploratory ( vs ? ) 
* 
