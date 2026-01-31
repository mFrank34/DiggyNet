-- installer.lua
local SERVER = "http://192.168.10.5:8000"
local MAX_RETRIES = 3

if not http then
	error("HTTP API is disabled. Enable it in CC:Tweaked config (enableHttp=true).")
end

-- Dependency-safe download order
local FILES = {
	"device.lua",
	"stats.lua",
	"location.lua",
	"state.lua",
	"actions.lua",
	"turtle.lua",
	"client.lua",
	"boot.lua",
	"agent.lua"
}

-- Helper to download a single file with retries
local function download(name)
	for attempt = 1, MAX_RETRIES do
		print(string.format("Downloading %s (attempt %d)...", name, attempt))
		local ok, res = pcall(http.get, SERVER .. "/" .. name)

		if ok and res and res.getResponseCode() == 200 then
			local f = fs.open(name, "w")
			f.write(res.readAll())
			f.close()
			res.close()
			print(name .. " downloaded successfully.")
			return true
		else
			if res then
				res.close()
			end
			print("Failed to download " .. name .. " (HTTP or connection error). Retrying...")
			sleep(1)
		end
	end
	error("Failed to download " .. name .. " after " .. MAX_RETRIES .. " attempts.")
end

-- Download all files
for _, file in ipairs(FILES) do
	download(file)
end

print("All files downloaded successfully. Starting agent.lua...")
shell.run("agent.lua")
