# CCLayBuilder
Python (pygame) + Lua Script for building with ComputerCraft

## How to use
- Run **laybuilder.py**. Configure the size, the components (minecraft block ids) and the name of the file. Then build what you want, layer by layer:  
 ![image](https://user-images.githubusercontent.com/56085790/179429266-696e398c-fdb7-418c-b00a-5b03757c1d26.png)
- Save it with [B] button and checkout the **.lua** file.
- Copy the contents of .lua file to **pastebin.com** creating new paste. Remember the code of the paste (it looks like **XxXxXxX**).
- Place your CC Turtle to the world like it placed on the screen (the program automatically deletes all empty lines):
 ![image](https://user-images.githubusercontent.com/56085790/179428939-a75838a9-45f2-4fd0-8f8e-b624ae680517.png)
- Put coal (or another fuel, but you will have to change the **fuelMoves** variable according to [this API doc](https://www.computercraft.info/wiki/Turtle.refuel)) to slot 1, and other items to any other slots. Use the **pastebin run XxXxXxX** command in your ComputerCraft turtle to build:
 ![image](https://user-images.githubusercontent.com/56085790/179428638-8fa20a67-8af6-44a9-a5f0-4e9712563b6e.png)
- Wait for some time...
- Enjoy the result! Here is an example from examples/house.lua file in progress:
 ![image](https://user-images.githubusercontent.com/56085790/179429577-a4498236-3275-4481-9e34-5097fd9f34ca.png)


## Other
### Useful links
[Minecraft ID list](https://minecraftitemids.com/)

### Controls in English:  
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
 
 
