local config = require("client")
local Actions = require("actions")
local Stats = require("stats")
local Location = require("location")
local State = require("state")
local Device = require("device")

-- Use a guaranteed writable path for key.json
local key_file = "/disk/key.json"
if not fs.exists("/disk") then
	fs.makeDir("/disk")
end

local SERVER = config.server_url .. "/heartbeat"

-- Load saved client_id and client_key safely
local function loadClientKey()
	if fs.exists(key_file) then
		local f = fs.open(key_file, "r")
		if not f then
			print("Warning: could not open key.json")
			return nil, nil
		end

		local content = f.readAll()
		f.close()

		if not content or content == "" then
			print("Warning: key.json is empty")
			return nil, nil
		end

		local ok, data = pcall(textutils.unserializeJSON, content)
		if not ok or not data then
			print("Warning: key.json contains invalid JSON")
			return nil, nil
		end

		if not data.id or not data.key then
			print("Warning: key.json missing id or key fields")
			return nil, nil
		end

		return data.id, data.key
	end

	return nil, nil
end

-- Save client_id and client_key locally
local function saveClientKey(id, key)
	if not id or not key then
		print("Error: cannot save nil id or key")
		return
	end

	local f = fs.open(key_file, "w")
	if f then
		f.write(textutils.serializeJSON({id = id, key = key}))
		f.close()
	else
		print("Error: could not open key.json for writing")
	end
end


-- Initialize client credentials
local turtle_id, client_key = loadClientKey()

-- Heartbeat fail tracking
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

	if turtle_id and client_key then
		payload.client_id = turtle_id
		payload.client_key = client_key
	else
		payload.server_key = config.server_key
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
		local ok, err

		if handler then
			ok, err = pcall(handler, cmd)
		else
			ok = false
			err = "unknown action"
		end

		State.commandFinished(cmd, ok, err)

		-- Report immediately
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

		local content = res.readAll()
		res.close()

		local ok, reply = pcall(textutils.unserializeJSON, content)
		if not ok or not reply then
			print("Invalid server response")
		else
		-- First-time registration: save key if server sends it
			if not turtle_id and reply.id and reply.client_key then
				turtle_id = reply.id
				client_key = reply.client_key
				os.setComputerLabel(turtle_id)
				saveClientKey(turtle_id, client_key)
				print("Registered with server. Assigned ID: " .. turtle_id)
			end

			if reply.stage then
				State.stage = reply.stage
			end

			if reply.actions then
				handleActions(reply.actions)
			end

			print("Heartbeat OK")
		end
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
