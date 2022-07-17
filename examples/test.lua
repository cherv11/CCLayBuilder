--[[
  This code was created automatically using CClayBuilder:
    https://github.com/cherv11/CCLayBuilder
--]]
y = 10
z = 5
x = 5
data = {{{2, 0, 0, 0, 2}, {0, 2, 0, 2, 0}, {0, 0, 2, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}}, {{0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}}, {{0, 0, 2, 2, 2}, {0, 0, 2, 2, 2}, {0, 0, 2, 2, 2}, {0, 0, 2, 2, 2}, {0, 0, 2, 2, 2}}, {{2, 2, 2, 0, 0}, {2, 2, 2, 0, 0}, {2, 2, 2, 0, 0}, {2, 2, 2, 0, 0}, {2, 2, 2, 0, 0}}, {{2, 2, 2, 2, 2}, {2, 2, 2, 2, 2}, {2, 2, 2, 2, 2}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}}, {{0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}, {2, 2, 2, 2, 2}, {2, 2, 2, 2, 2}, {2, 2, 2, 2, 2}}, {{0, 0, 0, 0, 0}, {2, 2, 2, 2, 2}, {0, 0, 0, 0, 0}, {2, 2, 2, 2, 2}, {0, 0, 0, 0, 0}}, {{0, 2, 0, 2, 0}, {0, 2, 0, 2, 0}, {0, 2, 0, 2, 0}, {0, 2, 0, 2, 0}, {0, 2, 0, 2, 0}}, {{0, 0, 0, 0, 0}, {0, 2, 2, 2, 0}, {0, 2, 2, 2, 0}, {0, 2, 2, 2, 0}, {0, 0, 0, 0, 0}}, {{0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 2, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}}}
blocks = {'minecraft:cobblestone', 'minecraft:red_wool', 'minecraft:redstone_block', 'minecraft:hay_block', '', '', '', '', '', '', '', '', '', '', '', '', 'minecraft:purple_wool'}

movedx = false
movedz = false
turns = 0
fuelMoves = 80
moves = 0

function moved()
    moves = moves + 1
    if moves >= fuelMoves then
        refuel()
        moves = 0
    end
end

function refuel()
    if not turtle.compareTo(1) then
        turtle.select(1)
    end
    turtle.refuel(1)
    local fuelCount = turtle.getItemCount(1)
    if fuelCount == 0 then
        print("Low fuel level!")
        return
    end
end

function place(id)
    if id == 0 then return end
    block = blocks[id]
    local success = false
    for i = 2, 16 do
        local details = turtle.getItemDetail(i)
        if details ~= nil then
            if details["name"] == block then
                if not turtle.compareTo(i) then
                    turtle.select(i)
                end
                success = true
                break
            end
        end
    end
    if success then
        turtle.placeDown()
    end
end

function empty_line(kv)
    for j = 1, z do
        if kv[j] ~= 0 then
            return false
        end
    end
    return true
end

function empty_surface(kv)
    for i = 1, x do
        for j = 1, z do
            if kv[i][j] ~= 0 then
                return false
            end
        end
    end
    return true
end

function turn(x)
    if math.abs(x-turns) > 2 then
        if x-turns > 0 then
            turtle.turnLeft()
            turns = turns - 1
        else
            turtle.turnRight()
            turns = turns + 1
        turns = turns % 4    
        return
        end
    end
    while x-turns > 0 do
        turtle.turnRight()
        turns = turns + 1
    end
    while x-turns < 0 do
        turtle.turnLeft()
        turns = turns - 1
    end
    turns = turns % 4
end

refuel()
turtle.forward()
moved()
for k = 1, y do
    turtle.up()
    moved()
    if not empty_surface(data[k]) then
        for i = 1, x do
            if movedx then
                i, lasti = x-i+1, 1
            else
                lasti = x
            end
            if not empty_line(data[k][i]) then
                for j = 1, z do
                    if movedz then
                        j, lastj = z-j+1, 1
                        turn(2)
                    else
                        lastj = z
                        turn(0)
                    end
                    place(data[k][i][j])
                    if j ~= lastj then
                        turtle.forward()
                        moved()
                    end
                end
                movedz = not movedz
            end
            if i ~= lasti then
                if movedx then
                    turn(3)
                else
                    turn(1)
                end
                turtle.forward()
                moved()
            end
        end
        movedx = not movedx
    end
end
