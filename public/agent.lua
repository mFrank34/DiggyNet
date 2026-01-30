local config = dofile("client.lua")

local SERVER = config.server_url .. "/heartbeat"
local turtle_id = nil

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
        local reply = textutils.unserializeJSON(res.readAll())
        res.close()

        if not turtle_id and reply.id then
            turtle_id = reply.id
            os.setComputerLabel(turtle_id)
        end

        print("heartbeat sent")
    else
        print("server unreachable")
    end

    sleep(config.heartbeat_interval)
end
