const express = require('express');
const cors = require('cors');
const cookieParser = require('cookie-parser');
require('dotenv').config();

const app = express();

// Middleware
app.use(express.json());
app.use(cookieParser());
app.use(cors({
  origin: process.env.CLIENT_URL || 'http://localhost:5173',
  credentials: true,
}));

// Routes
app.use('/api/v1/auth', require('./routes/auth.route'));
app.use('/api/v1/links', require('./routes/link.route'));
app.use('/api/v1/comments', require('./routes/comment.route'));
app.use('/api/v1/users', require('./routes/user.route'));
app.use('/api/v1/rooms', require('./routes/room.route'));
app.use('/api/v1/tags', require('./routes/tag.route'));
app.use('/api/v1/tools', require('./routes/tools.route'));
app.use('/api/v1/leaderboard', require('./routes/leaderboard.route'));
app.use('/api/v1/graph', require('./routes/graph.route'));

// Shortlink redirect (public)
app.get('/s/:code', require('./controllers/tools.controller').redirect);

// Health check
app.get('/health', (req, res) => res.send('OK'));

// Error handler
app.use(require('./middleware/errorHandler.middleware'));

module.exports = app;