local Location = {}

function Location.get()
	local x, y, z = gps.locate(3)
	if not x then
		return nil
	end
	return { x = x, y = y, z = z }
end

return Location
