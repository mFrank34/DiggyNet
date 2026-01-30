local T = require("turtle")

local Actions = {}

Actions.move = function(cmd)
	local n = cmd.n or 1
	for i = 1, n do
		if cmd.dir == "forward" then
			T.forward()
		elseif cmd.dir == "up" then
			T.up()
		elseif cmd.dir == "down" then
			T.down()
		end
	end
end

Actions.turn = function(cmd)
	if cmd.dir == "left" then
		T.left()
	elseif cmd.dir == "right" then
		T.right()
	end
end

Actions.dig = function()
	T.dig()
end

return Actions
