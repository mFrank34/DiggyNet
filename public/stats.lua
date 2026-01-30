local Stats = {}

function Stats.collect()
	local inv = {}

	for slot = 1, 16 do
		local item = turtle.getItemDetail(slot)
		if item then
			table.insert(inv, {
				slot = slot,
				name = item.name,
				count = item.count
			})
		end
	end

	return {
		fuel = turtle.getFuelLevel(),
		selected_slot = turtle.getSelectedSlot(),
		inventory = inv
	}
end

return Stats
