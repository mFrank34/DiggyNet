local config = require("client")
local Actions = require("actions")
local Stats = require("stats")
local Location = require("location")
local State = require("state")
local Device = require("device")


local SERVER = config.server_url .. "/heartbeat"
local key_file = "key.json"

-- Load saved client_id and client_key
local function loadClientKey()
	if fs.exists(key_file) then
		local f = fs.open(key_file, "r")
		local data = textutils.unserializeJSON(f.readAll())
		f.close()
		return data.id, data.key
	end
	return nil, nil
end

-- Save client_id and client_key locally
local function saveClientKey(id, key)
	local f = fs.open(key_file, "w")
	f.write(textutils.serializeJSON({id = id, key = key}))
	f.close()
end

-- Initialize client credentials
local turtle_id, client_key = loadClientKey()

local fail_count = 0
local MAX_FAILS = 5

-- Build heartbeat payload
local function buildHeartbeat()
	local payload = {
		role = config.role,
		status = State.status,
		task = { stage = State.stage },
		last_command = State.last_command,
		location = Location.get(),
		stats = Stats.collect(),
		vision = {
			front = Device.inspect(),
			up = Device.inspectUp(),
			down = Device.inspectDown()
		}

	}

	if not turtle_id then
	-- First-time registration requires server key
		payload.server_key = config.server_key
	else
		payload.client_id = turtle_id
		payload.client_key = client_key
	end

	return payload
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

		local handler = Actions[cmd.type] or Device.actions[cmd.type]

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

		-- First-time registration: save client_id and client_key
		if not turtle_id and reply.id and reply.client_key then
			turtle_id = reply.id
			client_key = reply.client_key
			os.setComputerLabel(turtle_id)
			saveClientKey(turtle_id, client_key)
			print("Registered with server. Assigned ID: " .. turtle_id)
		end

		-- Update stage if server sends it
		if reply.stage then
			State.stage = reply.stage
		end

		-- Execute actions if provided
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
