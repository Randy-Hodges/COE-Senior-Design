# Design Doc

---

This document will describe general guidelines on how we design and structure our code so that the style is consistent across files.

## Structure
All code will have a basic header that can be found in boilerplate.txt. The relevant portions can be found below

Desc - Gives an overview of what is happening within the file. What is the file used for? What is it doing? How does it interact with other files? If the file is a class, this section would describe what the class does and what it is used for. 
Length: Somewhere between 1 sentence and 1 paragraph. 

Warnings - This will generally be a bulleted list (with "-" characters or whichever character you choose) that describe things that viewers/users of the code should be aware of. Are there any known bugs? Are there any incomplete parts that the reader should be aware of? Is anything a little bit janky? These warnings go here. 
Length: Empty to less than 10 bullets. If there are more bullets, there is probably a way to condense them. 

TODO - This will contain a list of todo items. If readers want to contribute to the code, they can look here for what to do next. 
Length: Ideally 0-3 focused items, although you can further break things down if you want.

Imports occur after this commented-out header and then the actual code.

## Docstrings

Docstrings will be a prevelant part of the code, will be included with most functions and will follow the guidelines below. These "rules" can change depending on the complexity of a function (ie complex small functions will need more documentation, simple long functions will need less), but they are included as a general rule of thumb.

#### Small
If the function is small (roughly 2-3 lines of code or less) and simple, no docstrings are needed. The name of the function should be enough to understand what is happening. This will be a rare case.
>Example: 
>    def add_two_Numbers(a: int, b: int):
>        answer = a + b
>        return answer

#### Medium
If the function is somewhere between 4-10 lines of code and is relatively simple, a single sentence for the docstring will likely suffice. If using this style, it should be clear what inputs and outputs do if they exist.
>Example:
>    def merge_two_dicts(x, y):
>        """Given two dictionaries, merge them into a new dict as a shallow copy."""
>        z = x.copy()
>        z.update(y)
>        return z

#### Long
If the function is long and complex, we will use Google's docstring style. This includes having 1-2 sentences describing what the code does and also includes a section describing the arguments and a scetion describing the return values.
>Example: 
>    def function_with_types_in_docstring(param1, param2):
>        """
>        Example function with types documented in the docstring.
>
>        Args:
>            param1 (int): The first parameter.
>            param2 (str): The second parameter.
>
>        Returns:
>            bool: The return value. True for success, False otherwise.
>        """
>        <code>

## White Spacing
Two empty lines above function declarations





