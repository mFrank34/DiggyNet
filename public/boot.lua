-- boot.lua
if fs.exists("agent.lua") then
    shell.run("agent.lua")
else
    print("agent.lua missing")
end
