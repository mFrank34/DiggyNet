-- device.lua
local Device = {}

-- Default stubs (generic computer)
Device.inspect = function() return nil
end
Device.inspectUp = function() return nil
end
Device.inspectDown = function() return nil
end

-- If running on a turtle, override functions
if turtle then
	Device.inspect = turtle.inspect
	Device.inspectUp = turtle.inspectUp
	Device.inspectDown = turtle.inspectDown
end

return Device
