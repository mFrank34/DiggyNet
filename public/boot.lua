-- boot.lua
if fs.exists("init.lua") then
    shell.run("init.lua")
else
    print("init.lua missing")
end
