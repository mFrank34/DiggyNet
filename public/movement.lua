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

function Turtle.fuel()
	return turtle.getFuelLevel()
end

return Turtle
