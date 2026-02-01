local Turtle = {}

-- ---- Movement ----
function Turtle.forward()
	while not turtle.forward() do
		turtle.dig()
		sleep(0.2)
	end
end

function Turtle.back()
	turtle.back()
end

function Turtle.up()
	while not turtle.up() do
		turtle.digUp()
		sleep(0.2)
	end
end

function Turtle.down()
	while not turtle.down() do
		turtle.digDown()
		sleep(0.2)
	end
end

function Turtle.left()
	turtle.turnLeft()
end

function Turtle.right()
	turtle.turnRight()
end

-- ---- Actions ----
function Turtle.dig()
	turtle.dig()
end

function Turtle.place()
	turtle.place()
end

function Turtle.refuel(slot)
	if slot then
		turtle.select(slot)
	end
	turtle.refuel()
end

-- ---- Inventory / Fuel helpers ----
function Turtle.select(slot)
	turtle.select(slot)
end

function Turtle.itemCount()
	return turtle.getItemCount()
end

function Turtle.canRefuel()
	return turtle.refuel(0)
end

function Turtle.fuel()
	return turtle.getFuelLevel()
end

-- Returns true if block is present in front
function Turtle.detect()
	return turtle.detect()
end

function Turtle.detectUp()
	return turtle.detectUp()
end

function Turtle.detectDown()
	return turtle.detectDown()
end

-- Returns block info if present, else nil
function Turtle.inspect()
	local ok, info = turtle.inspect()
	return ok and info or nil
end

function Turtle.inspectUp()
	local ok, info = turtle.inspectUp()
	return ok and info or nil
end

function Turtle.inspectDown()
	local ok, info = turtle.inspectDown()
	return ok and info or nil
end

return Turtle
