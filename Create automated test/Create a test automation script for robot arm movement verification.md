
# Domain objects 


### Point
(2d): (x,y)
### Work-area
The system has a rectangular shape measuring work area specified by points which coordinates are specified under the input file. 

4 points for the 4 corners -> can be simplified to two points if fancy, can be controlled for errors too (not a rectangle)

Example:
```txt
Rectangle
(-4, -150), (-4, 150), (160, -150), (160, 150)
...
```

Shall implement isInside() function - as an abstraction upwards.
### Expected visited points

Array of indefinite size

Example:
```txt
...
Points
(-3, -149)
(4, 150)
```

Potential errors: 
* Point is not inside the work area
* Point is not in the actual visited points 
### Actual visited points

Array of indefinite size

Example:
```txt
(0,0)
error
(150, -155)
```

Potential errors:
* gibberish coordinate -- give a warning, but ultimately silence that, because based on the supplied data, it looks like that the robot armed move outside of the work area rectangle, so it homed itself. The hard error shall come from the outside coordinate, not the error line.

### Functions
There shall be an inputFileReader and an outputFileReader - both functions for now, as I don't see an encapsulation reason to make it a class.

There shall be a testResultfileGenerator, function for now, again no encapsulation reason.


## Approach

We dump context to AI, and verify AI code. Instruction used (after giving the repo's folder as the work-folder):

```
See the file "Robot-arm-task-rewrite-for-ai-delegation" and the file "Create a test automation script for robot arm movement verification" for context.  
Start working your way through the context. Propose a plan & share it with me for feedback.
```

[[Robot-arm-task-rewrite-for-ai-delegation]]

We shall review code line-by-line level (hence the size constraint for AI)

*Benchmarking:
Time spent with delegating to AI: 2 hours
Tokens used: 191.6k
*Could be better, but I forgot to spec the folder structure and that took a bit to clean up*

