-- stats.lua
local T = require("turtle")

local Stats = {}

function Stats.collect()
	local inv = {}

	for slot = 1, 16 do
		local item = T.itemCount(slot) -- <- use interface
		if item > 0 then
			table.insert(inv, {slot = slot, count = item})
		end
	end

	return {
		fuel = T.fuel(),           -- <- use interface
		selected_slot = turtle.getSelectedSlot(),  -- optional, can wrap T.select
		inventory = inv
	}
end

return Stats
