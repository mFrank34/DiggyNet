local SERVER_URL = "http://localhost:8000/hello"

local data = {
  id = os.getComputerLabel() or "turtle_unknown"
}

local res = http.post(
  SERVER_URL,
  textutils.serializeJSON(data),
  { ["Content-Type"] = "application/json" }
)

if not res then
  print("❌ no response from server")
  return
end

local body = res.readAll()
res.close()

local reply = textutils.unserializeJSON(body)

print(reply.message)
print("job:", reply.job)
