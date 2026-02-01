local Turtle = require("turtle_api")

local Actions = {}

-- ---- Generic movement ----
Actions.move = function(cmd)
	local n = cmd.n or 1

	for i = 1, n do
		if cmd.dir == "forward" then
			Turtle.forward()
		elseif cmd.dir == "up" then
			Turtle.up()
		elseif cmd.dir == "down" then
			Turtle.down()
		else
			error("invalid move dir: " .. tostring(cmd.dir))
		end
	end
end

Actions.turn = function(cmd)
	if cmd.dir == "left" then
		Turtle.left()
	elseif cmd.dir == "right" then
		Turtle.right()
	else
		error("invalid turn dir: " .. tostring(cmd.dir))
	end
end

-- ---- Convenience moves (server uses these) ----
Actions.move_left = function()
	Turtle.left()
	Turtle.forward()
end

Actions.move_right = function()
	Turtle.right()
	Turtle.forward()
end

Actions.move_forward = function()
	Turtle.forward()
end

Actions.move_back = function()
	Turtle.back()
end

-- ---- Dig ----
Actions.dig = function()
	Turtle.dig()
end

-- ---- Refuel ----
Actions.refuel = function(cmd)
	local target = cmd.amount or math.huge
	local gained = 0

	for slot = 1, 16 do
		Turtle.select(slot)

		if Turtle.canRefuel() then
			while Turtle.itemCount() > 0 and gained < target do
				if Turtle.refuel(1) then
					gained = gained + 1
				else
					break
				end
			end
		end
	end

	if gained == 0 then
		error("no fuel available")
	end

	return gained
end

return Actions
