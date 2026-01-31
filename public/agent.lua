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
local current_job = nil

-- Credentials ---
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

local function saveClientKey(id, key)
	local f = fs.open(key_file, "w")
	f.write(textutils.serializeJSON({ id = id, key = key }))
	f.close()
end

local client_id, client_key = loadClientKey()

--- Heartbeat ---
local function buildHeartbeat(extra)
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

	if extra then
		for k, v in pairs(extra) do
			payload[k] = v
		end
	end

	return payload
end

local function sendHeartbeat(extra)
	return http.post(
		SERVER,
		textutils.serializeJSON(buildHeartbeat(extra)),
		{ ["Content-Type"] = "application/json" }
	)
end

--- Actions ---
local function handleActions(actions)
	for _, cmd in ipairs(actions) do
		State.commandStarted(cmd)

		local actionType = cmd.type or cmd.action
		local handler = Actions[actionType]
		or (Device.actions and Device.actions[actionType])

		local ok, err = pcall(handler or function()
		end, cmd)
		State.commandFinished(cmd, ok, err)

		local res = sendHeartbeat()
		if res then
			res.close()
		end
	end

	if #actions == 0 and current_job then
		sendHeartbeat({
			job_done = current_job.id,
			status = "idle"
		})
		current_job = nil
	end
end

--- Main loop ---
while true do
	local res = sendHeartbeat()

	if res then
		local content = res.readAll()
		res.close()

		local ok, reply = pcall(textutils.unserializeJSON, content)
		if ok and reply then

		-- 🔑 REGISTRATION (single-object reply)
			if reply.id and reply.key then
				client_id = tostring(reply.id)
				client_key = reply.key
				saveClientKey(client_id, client_key)

				-- ⭐ FIX: reload immediately so next heartbeat uses correct values
				client_id, client_key = loadClientKey()

				os.setComputerLabel("Turtle " .. string.sub(client_id, 1, 4))
			end

			-- 🧭 Stage sync (legacy)
			if reply.stage then
				State.stage = reply.stage
			end

			-- 🛠 Legacy actions
			if reply.actions then
				handleActions(reply.actions)
			end

			-- 🧱 New job/task model (array reply)
			if type(reply) == "table" and reply[1] then
				for _, item in ipairs(reply) do
					if item.type == "job" then
						current_job = item.job
					elseif item.type == "task" then
						handleActions({ item.task })
					end
				end
			end
		end
	end

	sleep(config.heartbeat_interval)
end
