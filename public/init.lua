local SERVER = "http://localhost:8000"

local function download(name)
    if fs.exists(name) then return end

    local res = http.get(SERVER .. "/" .. name)
    if not res then error("Failed to download " .. name) end

    local f = fs.open(name, "w")
    f.write(res.readAll())
    f.close()
    res.close()
end

download("boot.lua")        -- Boot strap
download("client.lua")      -- Config
download("movement.lua")    -- Movement system
download("agent.lua")       -- Runtime

shell.run("agent.lua")
