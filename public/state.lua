local State = {
	status = "idle",
	stage = "none",
	last_command = nil
}

function State.commandStarted(cmd)
	State.last_command = {
		type = cmd.type,
		result = "running"
	}
	State.status = "busy"
end

function State.commandFinished(cmd, ok, err)
	State.last_command = {
		type = cmd.type,
		result = ok and "ok" or "error",
		error = err
	}
	State.status = ok and "idle" or "error"
end

return State
