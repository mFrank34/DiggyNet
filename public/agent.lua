local config = require("client")
local Actions = require("actions")
local Stats = require("stats")
local Location = require("location")
local State = require("state")

local SERVER = config.server_url .. "/heartbeat"
local turtle_id = nil

local fail_count = 0
local MAX_FAILS = 5

-- Build heartbeat payload
local function buildHeartbeat()
	return {
		id = turtle_id,
		role = config.role,
		status = State.status,
		task = {
			stage = State.stage
		},
		last_command = State.last_command,
		location = Location.get(),
		stats = Stats.collect()
	}
end

-- Send heartbeat
local function sendHeartbeat()
	return http.post(
		SERVER,
		textutils.serializeJSON(buildHeartbeat()),
		{ ["Content-Type"] = "application/json" }
	)
end

-- Execute actions from server
local function handleActions(actions)
	for _, cmd in ipairs(actions) do
		State.commandStarted(cmd)

		local handler = Actions[cmd.type]
		local ok, err

		if handler then
			ok, err = pcall(handler, cmd)
		else
			ok = false
			err = "unknown action"
		end

		State.commandFinished(cmd, ok, err)

		-- Immediate report after command
		local res = sendHeartbeat()
		if res then
			res.close()
		end
	end
end

-- Main loop
while true do
	local res = sendHeartbeat()

	if res then
		fail_count = 0

		local reply = textutils.unserializeJSON(res.readAll())
		res.close()

		if not turtle_id and reply.id then
			turtle_id = reply.id
			os.setComputerLabel(turtle_id)
		end

		if reply.stage then
			State.stage = reply.stage
		end

		if reply.actions then
			handleActions(reply.actions)
		end

		print("Heartbeat OK")
	else
		fail_count = fail_count + 1
		print("Server unreachable (" .. fail_count .. "/" .. MAX_FAILS .. ")")

		if fail_count >= MAX_FAILS then
			print("Max failures reached. Exiting.")
			return
		end
	end

	sleep(config.heartbeat_interval)
end
