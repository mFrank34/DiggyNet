-- stats.lua
local Stats = {}

function Stats.collect()
	local inv = {}

	-- Collect non-empty slots
	for slot = 1, 16 do
		local count = T.itemCount(slot)  -- interface function
		if count > 0 then
			table.insert(inv, {slot = slot, count = count})
		end
	end

	return {
		fuel = turtle.getFuelLevel(),       -- native turtle function
		selected_slot = turtle.getSelectedSlot(), -- native turtle function
		inventory = inv
	}
end

return Stats
