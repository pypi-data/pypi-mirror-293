# Donations
It takes me a long time to make these libraries. If you would like to support my work, Then you can follow my patreon :)

https://www.patreon.com/Schkimansky

# Library
Made as a part of the zen standard library python project, This library is the successor / replacer of the standard module string. 
This replacement is easier to use, And has more features. Here's a example with a TextTemplate (Called "Template" in string)
```python
import zstring

template = zstring.TextTemplate("Hello, $name! I heard that you're feeling $mood")
values = {"name": "alice", "mood": "sad"}

print(template.fill(values))
```

# Installation
```bash
pip install zstring
```
