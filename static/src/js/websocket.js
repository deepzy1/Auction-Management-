const http = require('http');
const socketIo = require('socket.io');

const server = http.createServer();
const io = socketIo(server, {
  cors: {
    origin: "http://localhost:8068", // Allow connections from your Odoo frontend
    methods: ["GET", "POST"], // Allow GET and POST methods
    allowedHeaders: ["my-custom-header"], // Allow any custom headers if needed
    credentials: true // Allow cookies or credentials (optional)
  }
});

// Handle WebSocket connections
io.on('connection', (socket) => {
  console.log('A user connected');

  // Listen for disconnection
  socket.on('disconnect', () => {
    console.log('User disconnected');
  });
});

server.listen(3000, () => {
  console.log('WebSocket server running on port 3000');
});
