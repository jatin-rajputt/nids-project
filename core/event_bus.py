import queue

event_queue =queue.Queue()

def publish(event_type, data):
    
    event_queue.put({
        "type": event_type,
        "data": data
    })
    
    
def consume():
    
    if not event_queue.empty():
        return event_queue.get()
    
    return None