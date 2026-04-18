bind = "0.0.0.0:10002"
workers = 2

def on_starting(server):
    print("✅ Server started successfully on port 10002", flush=True)
