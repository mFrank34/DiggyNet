local turtle = require("turtle")

local Actions = {}

-- ---- Movement ----
Actions.move = function(cmd)
	local n = cmd.n or 1

	for i = 1, n do
		if cmd.dir == "forward" then
			turtle.forward()
		elseif cmd.dir == "up" then
			turtle.up()
		elseif cmd.dir == "down" then
			turtle.down()
		else
			error("invalid move dir: " .. tostring(cmd.dir))
		end
	end
end

Actions.turn = function(cmd)
	if cmd.dir == "left" then
		turtle.left()
	elseif cmd.dir == "right" then
		turtle.right()
	else
		error("invalid turn dir: " .. tostring(cmd.dir))
	end
end

-- Convenience dance-style moves (mapped from server-enqueued dance steps)
Actions.move_left = function()
	-- turn left and step forward to simulate a left step
	turtle.turnLeft()
	turtle.forward()
end

Actions.move_right = function()
	-- turn right and step forward to simulate a right step
	turtle.turnRight()
	turtle.forward()
end

Actions.move_forward = function()
	turtle.forward()
end

Actions.move_back = function()
	-- attempt to move back (Turtle.back exists on the client)
	turtle.back()
end

Actions.dig = function()
	turtle.dig()
end

-- ---- Refuel ----
Actions.refuel = function(cmd)
	local target = cmd.amount or math.huge
	local gained = 0

	for slot = 1, 16 do
		turtle.select(slot)

		if turtle.canRefuel() then
			while turtle.itemCount() > 0 and gained < target do
				if turtle.refuel(1) then
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