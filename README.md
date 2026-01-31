# DiggyNet

DiggyNet is a cozy CC:Tweaked network where turtles work together, mine resources, and do their own thing — all
connected through a shared system built for fun, automation, and a little chaos.

# PasteBin of Client

https://pastebin.com/45GhSLKf

# client talk
```
{
"id": "<client_id or null>",
"key": "<client_key or null>",
"server_key": "<only when registering>",
"role": "...",
"status": "...",
"task": { "stage": ... },
"location": { ... },
"stats": { ... },
"vision": { ... }
}
``` 

# server response
```
{
"id": "<assigned client id>",
"key": "<assigned client key>",
"stage": "...",
"actions": [ ... ]
}
```