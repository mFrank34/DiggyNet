local config = require("client")
local Actions = require("actions")
local Stats = require("stats")
local Location = require("location")
local State = require("state")
local Device = require("device")

local key_file = "/disk/key.json"
if not fs.exists("/disk") then
	fs.makeDir("/disk")
end

local SERVER = config.server_url .. "/heartbeat"

-- Load saved credentials
local function loadClientKey()
	if not fs.exists(key_file) then
		return nil, nil
	end

	local f = fs.open(key_file, "r")
	if not f then
		return nil, nil
	end

	local content = f.readAll()
	f.close()

	if not content or content == "" then
		return nil, nil
	end

	local ok, data = pcall(textutils.unserializeJSON, content)
	if not ok or not data then
		return nil, nil
	end

	return data.id, data.key
end

-- Save credentials
local function saveClientKey(id, key)
	local f = fs.open(key_file, "w")
	f.write(textutils.serializeJSON({ id = id, key = key }))
	f.close()
end

local client_id, client_key = loadClientKey()

local function buildHeartbeat()
	local payload = {
		id = client_id,
		key = client_key,
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

	if not client_id or not client_key then
		payload.server_key = config.server_key
	end

	return payload
end

local function sendHeartbeat()
	return http.post(
		SERVER,
		textutils.serializeJSON(buildHeartbeat()),
		{ ["Content-Type"] = "application/json" }
	)
end

local function handleActions(actions)
	for _, cmd in ipairs(actions) do
		State.commandStarted(cmd)

		local handler = Actions[cmd.type] or Device.actions[cmd.type]
		local ok, err = pcall(handler or function()
		end, cmd)

		State.commandFinished(cmd, ok, err)

		local res = sendHeartbeat()
		if res then
			res.close()
		end
	end
end

while true do
	local res = sendHeartbeat()

	if res then
		local content = res.readAll()
		res.close()

		local ok, reply = pcall(textutils.unserializeJSON, content)
		if ok and reply then

		-- Registration or credential update
			if reply.id and reply.key then
				client_id = tostring(reply.id)
				client_key = reply.key
				saveClientKey(client_id, client_key)
				os.setComputerLabel(client_id)
			end

			if reply.stage then
				State.stage = reply.stage
			end
			if reply.actions then
				handleActions(reply.actions)
			end
		end
	end

	sleep(config.heartbeat_interval)
end
