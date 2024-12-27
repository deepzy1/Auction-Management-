import socketio
import eventlet

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

def notify_highest_bid(auction_id, highest_bid):
    sio.emit('highest_bid_update', {'auction_id': auction_id, 'highest_bid': highest_bid})
