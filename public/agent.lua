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

-- Track the currently assigned job
local current_job = nil

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

-- Build heartbeat payload
local function buildHeartbeat(extra)
	local payload = {
		id = client_id,
		key = client_key,
		status = State.status,
		location = Location.get(),
		stats = Stats.collect(),
		vision = {
			front = Device.inspect(),
			up = Device.inspectUp(),
			down = Device.inspectDown()
		}
	}

	-- Merge in any extra fields (job_progress, job_done, etc.)
	if extra then
		for k, v in pairs(extra) do
			payload[k] = v
		end
	end

	-- Registration case
	if not client_id or not client_key then
		payload.server_key = config.server_key
	end

	return payload
end

-- Send heartbeat (supports extra fields)
local function sendHeartbeat(extra)
	return http.post(
		SERVER,
		textutils.serializeJSON(buildHeartbeat(extra)),
		{ ["Content-Type"] = "application/json" }
	)
end

-- Execute actions from server
local function handleActions(actions)
	for _, cmd in ipairs(actions) do
		State.commandStarted(cmd)

		-- Support both formats: {type="move"} or {action="move_left"}
		local actionType = cmd.type or cmd.action

		-- Safely resolve handler
		local handler = Actions[actionType]
		if not handler and Device.actions then
			handler = Device.actions[actionType]
		end

		-- Execute the action
		local ok, err = pcall(handler or function()
		end, cmd)

		State.commandFinished(cmd, ok, err)

		-- Heartbeat after each action
		local res = sendHeartbeat()
		if res then
			res.close()
		end
	end

	-- If no more actions AND we have a current job, mark it complete
	if #actions == 0 and current_job then
		sendHeartbeat({
			job_done = current_job.id,
			status = "idle"
		})
		current_job = nil
	end
end

-- Main loop
while true do
	local res = sendHeartbeat()

	if res then
		local content = res.readAll()
		res.close()

		local ok, reply = pcall(textutils.unserializeJSON, content)
		if ok and reply then

		-- Server returns a LIST of items (job, task, etc.)
			if type(reply) == "table" then
				for _, item in ipairs(reply) do

				-- Registration and credential update
					if item.id and item.key then
						client_id = tostring(item.id)
						client_key = item.key
						saveClientKey(client_id, client_key)
						os.setComputerLabel("Turtle " .. string.sub(client_id, 1, 4))
					end

					-- Job assignment
					if item.type == "job" then
						current_job = item.job
					end

					-- Task execution
					if item.type == "task" then
						handleActions({ item.task })
					end
				end
			end
		end
	end

	sleep(config.heartbeat_interval)
end
