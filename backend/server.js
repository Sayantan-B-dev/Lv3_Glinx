const app = require('./src/app');
const http = require('http');
const { Server } = require('socket.io');
const chatSocket = require('./src/sockets/chat.socket');

const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: process.env.CLIENT_URL || 'http://localhost:5173',
    credentials: true,
  },
});

// Attach socket handlers
io.on('connection', (socket) => chatSocket(io, socket));

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});