local Pos = {
	x = 0,
	y = 0,
	z = 0,
	facing = 0 -- 0=N, 1=E, 2=S, 3=W
}

function Pos.forward()
	if turtle.forward() then
		if Pos.facing == 0 then
			Pos.z = Pos.z - 1
		elseif Pos.facing == 1 then
			Pos.x = Pos.x + 1
		elseif Pos.facing == 2 then
			Pos.z = Pos.z + 1
		elseif Pos.facing == 3 then
			Pos.x = Pos.x - 1
		end
		return true
	end
end

function Pos.up()
	if turtle.up() then
		Pos.y = Pos.y + 1
	end
end

function Pos.down()
	if turtle.down() then
		Pos.y = Pos.y - 1
	end
end

function Pos.left()
	turtle.turnLeft()
	Pos.facing = (Pos.facing + 3) % 4
end

function Pos.right()
	turtle.turnRight()
	Pos.facing = (Pos.facing + 1) % 4
end

function Pos.get()
	return {
		x = Pos.x,
		y = Pos.y,
		z = Pos.z,
		facing = Pos.facing
	}
end

return Pos
