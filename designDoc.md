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

Docstrings will be a prevelant part of the code, will be included with most functions and will follow the guidelines below.

For all functions we will use Google's docstring style. This includes having 1-2 sentences describing what the code does and also includes a section describing the arguments and a section describing the return values. If there are no argument/return values, there is no need to include those sections. You can optionally include a more detailed explanation after the initial description if you want to add more documentation. Triple double quotes will be used (as opposed to triple single quotes).

Example: 
```
    def function_with_types_in_docstring(param1, param2):
        """
        Example function with types documented in the docstring.

        Args:
            param1 (int): The first parameter.
            param2 (str): The second parameter.

        Returns:
            bool: The return value. True for success, False otherwise.
        """
        <code
```

Example:
```
    def copy_mouse_position():
        """
        Copies the current mouse position on the screen to the console and your clipboard when the 'insert' key is pressed. 
        This position can be used in clicking functions that will click a particular area. 
        """
        print('Running copy_mouse_position.py. Press the \'insert\' key to copy mouse position.')
        print('Press ctrl + c while in the terminal window to exit.')
        while True:
            keyboard.wait('insert')
            x, y = pyautogui.position()
            pyperclip.copy(f'{str(x)}, {str(y)}')   
            print(f'\'Insert\' key was pressed! Copied mouse position ({str(x)}, {str(y)}) to clipboard. Press ctrl + c while in the terminal window to exit. Waiting again...')
```

## White Spacing
Two empty lines above function declarations





