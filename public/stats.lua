local Stats = {}

Stats.collect = function()
  return {
    fuel = turtle.getFuelLevel(),
    slot = turtle.getSelectedSlot(),
    label = os.getComputerLabel()
  }
end

return Stats
