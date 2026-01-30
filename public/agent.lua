local config = require("client")
local Actions = require("actions")


local SERVER = config.server_url .. "/heartbeat"
local turtle_id = nil

local fail_count = 0
local MAX_FAILS = 5

while true do
	local data = {
		id = turtle_id,
		status = config.role
	}

	local res = http.post(
		SERVER,
		textutils.serializeJSON(data),
		{ ["Content-Type"] = "application/json" }
	)

	if res then
		fail_count = 0 -- reset on success

		local reply = textutils.unserializeJSON(res.readAll())
		res.close()

		if not turtle_id and reply.id then
			turtle_id = reply.id
			os.setComputerLabel(turtle_id)
		end

		print("heartbeat sent")
	else
		fail_count = fail_count + 1
		print("server unreachable (" .. fail_count .. "/" .. MAX_FAILS .. ")")

		if fail_count >= MAX_FAILS then
			print("Max connection attempts reached. Exiting.")
			return -- stops the program
		end
	end

	sleep(config.heartbeat_interval)
end