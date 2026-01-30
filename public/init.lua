local SERVER = "http://localhost:8000"

if not http then
	error("HTTP API is disabled. Enable it in CC:Tweaked config.")
end

local FILES = {
	"boot.lua",
	"client.lua",
	"agent.lua",
	"actions.lua",
	"turtle.lua",
	"stats.lua",
	"location.lua",
	"state.lua"
}

local function download(name)
	print("Downloading " .. name .. "...")

	local res = http.get(SERVER .. "/" .. name)
	if not res then
		error("Failed to download " .. name)
	end

	local f = fs.open(name, "w")
	f.write(res.readAll())
	f.close()
	res.close()
end

for _, file in ipairs(FILES) do
	download(file)
end

print("Install complete. Starting agent...")
shell.run("agent.lua")
