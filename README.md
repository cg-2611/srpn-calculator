# SRPN Calculator

This calculator was the result of trying to recreate another SRPN calculator I was given, however I was given no source code and so I had to determine the functionality of the calculator by simply using it and trying different inputs. It differs from a regular RPN calculator since it performs saturation checking for maximum and minimum integer values.

### Supported Inputs:
---
The calculator supports all numbers and most arithmetic operators.
Other inputs include:
- `d`: outputs the stack
- `r`: pushes a pseudo-random number to the stack
- `e`: exits the calculator

Additionally, the calculator can convert between octal and decimal numbers. An octal number can be input by prepending the octal number with a 0, e.g. 014 indicates the number 14 in octal.

### Run
---
First clone the repository with:
```
git clone https://github.com/cg-2611/srpn-calculator.git
```
Next, open the directory created by the `git clone` command:
```
cd srpn-calculator
```
The to run the calculator, run:
```
python srpn_calculator.py
```
> Note: the calculator requires python 3.7 at a minimum and so the interpreter used to execute the program must support this version at least. The command `python3` might need to be used instead.
