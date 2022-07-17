# CCLayBuilder
Python (pygame) + Lua Script for building with ComputerCraft

## Using
- Run **laybuilder.py**. Configure the size, the components (minecraft block ids) and the name of the file. Then build what you want, layer by layer:  
 ![image](https://user-images.githubusercontent.com/56085790/179425457-9ec1ef68-a518-4b2c-a9bb-337c844d51c5.png)  
- Save it with [B] button and checkout the **.lua** file.
- Copy the contents of .lua file to **pastebin.com** creating new paste.
- Use the **pastebin run XxXxXxX** command in your ComputerCraft turtle to build what you want. Put coal (or another fuel, but you will have to change the **fuelMoves** variable according to [this API doc](https://www.computercraft.info/wiki/Turtle.refuel)) to slot 1, and other items to any other slots.
- Enjoy the result! Here is an example from examples/test.lua file:
 ![image](https://user-images.githubusercontent.com/56085790/179426415-ce0a1a7e-8f64-4577-987e-d67b05a3aecd.png)


## Other
### Here are the controls in English:  
 Change layer: **[A][D]**  
 Change color: **[Q][E]**  
 Draw: **[LMB]**  
 Erase: **[RMB]**  
 Toggle grid: **[G]**  
 Toggle info: **[H]**  
 Toggle ghost mode (shows prev surface): **[J]**  
 Save: **[B]**  
 Exit: **[Esc]**  
 Clear all: **[P]** 
 
 
