local State = {
	status = "idle",
	stage = "none",
	last_command = nil
}

function State.commandStarted(cmd)
	State.last_command = {
		type = cmd.type or cmd.action or "unknown",
		result = "running"
	}

	State.status = "busy"

	print("[CMD] start:", State.last_command.type)
end

function State.commandFinished(cmd, ok, err)
	State.last_command = {
		type = cmd.type or cmd.action or "unknown",
		result = ok and "ok" or "error",
		error = err
	}

	State.status = ok and "idle" or "error"

	if ok then
		print("[CMD] done :", State.last_command.type)
	else
		print("[CMD] fail :", State.last_command.type, err)
	end
end

return State
