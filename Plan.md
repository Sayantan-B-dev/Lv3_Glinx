# Glinx – Very, Very, Very Detailed Implementation Plan (One‑Man Army, 3 Weeks)

This plan breaks down every single task into **sub‑day chunks**, with terminal commands, file paths, code snippets, and testing steps.  
Follow it exactly. Do not skip anything.

---

## Week 1 – Core CRUD + Auth + CSS Foundation

### Day 1 – Project Setup & Database (6–8 hours)

#### 1.1 Create project folders (10 min)
```bash
mkdir Glinx && cd Glinx
mkdir backend frontend database
cd backend
npm init -y
```

#### 1.2 Install backend dependencies (5 min)
```bash
npm install express pg bcrypt jsonwebtoken dotenv cors cookie-parser socket.io cheerio node-fetch node-cron
npm install -D nodemon
```

#### 1.3 Create backend file structure (15 min)
```bash
mkdir -p src/{config,controllers,middleware,models,services,sockets,routes,utils}
touch src/app.js server.js .env
```

#### 1.4 Setup PostgreSQL (30 min)
- Create free database on [neon.tech](https://neon.tech) (or install locally)
- Copy connection string (starts with `postgresql://...`)
- Save to `.env`:
```env
PORT=5000
DATABASE_URL=your_neon_connection_string
JWT_SECRET=super_secret_change_this
CLIENT_URL=http://localhost:5173
```

#### 1.5 Write database schema (1 hour)
Create `database/init.sql` – copy the full schema from section 4 of the SRS.  
Run it:
```bash
psql $DATABASE_URL < database/init.sql
```
(Or use neon's SQL editor)

#### 1.6 Create database connection pool (30 min)
`backend/src/config/db.js`:
```javascript
const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
module.exports = { query: (text, params) => pool.query(text, params) };
```

#### 1.7 Create Express server skeleton (1 hour)
`backend/src/app.js`:
```javascript
const express = require('express');
const cors = require('cors');
const cookieParser = require('cookie-parser');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cookieParser());
app.use(cors({ origin: process.env.CLIENT_URL, credentials: true }));

// Health check
app.get('/health', (req, res) => res.send('OK'));

module.exports = app;
```
`backend/server.js`:
```javascript
const app = require('./src/app');
const http = require('http');
const server = http.createServer(app);
const PORT = process.env.PORT || 5000;
server.listen(PORT, () => console.log(`Server on ${PORT}`));
```

#### 1.8 Test server (10 min)
```bash
nodemon server.js
# Visit http://localhost:5000/health → should see "OK"
```

#### 1.9 Frontend setup with Vite (30 min)
```bash
cd ../frontend
npm create vite@latest . -- --template react
npm install axios react-router-dom socket.io-client
npm install -D @vitejs/plugin-react (already there)
```

#### 1.10 Clean up frontend and create CSS structure (1 hour)
Delete `src/App.css`, `src/index.css` (we'll replace).  
Create `src/styles/` with all global CSS files (see section 3.1 of SRS).  
`src/styles/index.css`:
```css
@import './variables.css';
@import './typography.css';
@import './utilities.css';
@import './animations.css';
@import './themes/light.css';
```
`src/main.jsx` – import `./styles/index.css` (not `./index.css`).  
`src/index.css` should just `@import './styles/index.css';`

**Test frontend:** `npm run dev` → see Vite default page.

---

### Day 2 – Authentication Backend (6 hours)

#### 2.1 Create user model (1 hour)
`backend/src/models/user.model.js`:
```javascript
const db = require('../config/db');

class User {
  static async create({ username, email, passwordHash, interests }) {
    const result = await db.query(
      `INSERT INTO users (username, email, password_hash, interests) 
       VALUES ($1, $2, $3, $4) RETURNING id, username, email`,
      [username, email, passwordHash, interests]
    );
    return result.rows[0];
  }
  static async findByEmail(email) {
    const result = await db.query(`SELECT * FROM users WHERE email = $1`, [email]);
    return result.rows[0];
  }
  static async findById(id) {
    const result = await db.query(`SELECT id, username, email, bio, avatar_url, interests, karma, is_admin FROM users WHERE id = $1`, [id]);
    return result.rows[0];
  }
}
module.exports = User;
```

#### 2.2 Create utilities (30 min)
`backend/src/utils/hash.util.js`:
```javascript
const bcrypt = require('bcrypt');
const hashPassword = (password) => bcrypt.hash(password, 10);
const comparePassword = (password, hash) => bcrypt.compare(password, hash);
module.exports = { hashPassword, comparePassword };
```
`backend/src/utils/jwt.util.js`:
```javascript
const jwt = require('jsonwebtoken');
const signToken = (userId) => jwt.sign({ userId }, process.env.JWT_SECRET, { expiresIn: '7d' });
const verifyToken = (token) => jwt.verify(token, process.env.JWT_SECRET);
module.exports = { signToken, verifyToken };
```

#### 2.3 Create auth controller (2 hours)
`backend/src/controllers/auth.controller.js`:
```javascript
const User = require('../models/user.model');
const { hashPassword, comparePassword } = require('../utils/hash.util');
const { signToken } = require('../utils/jwt.util');

exports.register = async (req, res) => {
  const { username, email, password, interests } = req.body;
  const passwordHash = await hashPassword(password);
  const user = await User.create({ username, email, passwordHash, interests });
  const token = signToken(user.id);
  res.cookie('token', token, { httpOnly: true, sameSite: 'lax', maxAge: 7*24*60*60*1000 });
  res.json({ user });
};

exports.login = async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findByEmail(email);
  if (!user || !(await comparePassword(password, user.password_hash))) 
    return res.status(401).json({ error: 'Invalid credentials' });
  const token = signToken(user.id);
  res.cookie('token', token, { httpOnly: true, sameSite: 'lax', maxAge: 7*24*60*60*1000 });
  res.json({ user: { id: user.id, username: user.username, email: user.email } });
};

exports.logout = (req, res) => {
  res.clearCookie('token');
  res.json({ message: 'Logged out' });
};

exports.me = async (req, res) => {
  const user = await User.findById(req.userId);
  res.json({ user });
};
```

#### 2.4 Create auth middleware (30 min)
`backend/src/middleware/auth.middleware.js`:
```javascript
const { verifyToken } = require('../utils/jwt.util');

module.exports = (req, res, next) => {
  const token = req.cookies.token;
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  try {
    const decoded = verifyToken(token);
    req.userId = decoded.userId;
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
};
```

#### 2.5 Create auth routes (30 min)
`backend/src/routes/auth.route.js`:
```javascript
const router = require('express').Router();
const authController = require('../controllers/auth.controller');
const authMiddleware = require('../middleware/auth.middleware');

router.post('/register', authController.register);
router.post('/login', authController.login);
router.post('/logout', authController.logout);
router.get('/me', authMiddleware, authController.me);
module.exports = router;
```

#### 2.6 Mount routes in `app.js` (5 min)
```javascript
app.use('/api/v1/auth', require('./routes/auth.route'));
```

#### 2.7 Test with Postman (1 hour)
- POST `http://localhost:5000/api/v1/auth/register` (body: username, email, password, interests array)
- POST `/login` – should set cookie
- GET `/me` with cookie – returns user

---

### Day 3 – CSS Foundation & Navbar (6 hours)

#### 3.1 Create all global CSS files (2 hours)
Fill `variables.css`, `typography.css`, `utilities.css`, `animations.css`, `themes/light.css` with the content from SRS section 3.

#### 3.2 Create Navbar component (2 hours)
`frontend/src/components/common/Navbar.jsx`:
```jsx
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import styles from './Navbar.module.css';

export default function Navbar() {
  const { user, logout } = useAuth();
  return (
    <nav className={styles.navbar}>
      <div className={styles.container}>
        <Link to="/" className={styles.logo}>Glinx</Link>
        <div className={styles.navLinks}>
          {user ? (
            <>
              <Link to="/submit">Submit</Link>
              <Link to={`/profile/${user.username}`}>Profile</Link>
              <button onClick={logout}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
```
`Navbar.module.css` – style with flex, background, spacing using CSS variables.

#### 3.3 Create AuthContext and useAuth hook (2 hours)
`frontend/src/contexts/AuthContext.jsx`:
```jsx
import { createContext, useReducer, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext();
const authReducer = (state, action) => {
  switch(action.type) {
    case 'SET_USER': return { ...state, user: action.payload, loading: false };
    case 'LOGOUT': return { ...state, user: null, loading: false };
    default: return state;
  }
};
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, { user: null, loading: true });
  useEffect(() => {
    api.get('/auth/me').then(res => dispatch({ type: 'SET_USER', payload: res.data.user })).catch(() => dispatch({ type: 'SET_USER', payload: null }));
  }, []);
  const login = async (email, password) => { /* call api, set user */ };
  const logout = async () => { await api.post('/auth/logout'); dispatch({ type: 'LOGOUT' }); };
  return <AuthContext.Provider value={{ ...state, login, logout }}>{children}</AuthContext.Provider>;
};
export const useAuth = () => useContext(AuthContext);
```

`frontend/src/services/api.js`:
```javascript
import axios from 'axios';
const api = axios.create({ baseURL: import.meta.env.VITE_API_URL + '/api/v1', withCredentials: true });
export default api;
```

#### 3.4 Create LoginPage and RegisterPage (1 hour)
Basic forms with CSS modules. Register includes multiple checkboxes for interests (predefined tags like "javascript", "react", "python").

---

### Day 4-5 – Link CRUD Backend (12 hours)

#### 4.1 Link model (2 hours)
`backend/src/models/link.model.js`:
```javascript
const db = require('../config/db');
class Link {
  static async create({ userId, url, title, description, tags, shortCode, isPrivate, allowedUsers }) {
    const result = await db.query(
      `INSERT INTO links (user_id, original_url, title, description, short_code, is_private, private_allowed_users) 
       VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING *`,
      [userId, url, title, description, shortCode, isPrivate, allowedUsers]
    );
    // handle tags: for each tag, insert into tags (if new) and link_tags
    return result.rows[0];
  }
  static async findById(id) { /* SELECT */ }
  static async update(id, fields) { /* UPDATE */ }
  static async delete(id) { /* DELETE */ }
  static async getFeed({ userId, type, tag, page, limit }) { /* complex join for following feed */ }
}
module.exports = Link;
```

#### 4.2 Link parser service (2 hours)
`backend/src/services/linkParser.service.js`:
```javascript
const fetch = require('node-fetch');
const cheerio = require('cheerio');

async function parseUrl(url) {
  const response = await fetch(url);
  const html = await response.text();
  const $ = cheerio.load(html);
  const title = $('meta[property="og:title"]').attr('content') || $('title').text();
  const description = $('meta[property="og:description"]').attr('content') || $('meta[name="description"]').attr('content');
  const image = $('meta[property="og:image"]').attr('content');
  return { title, description, image };
}

async function autoTag(title, description) {
  const text = title + ' ' + description;
  const words = text.toLowerCase().split(/\W+/);
  const stopwords = new Set(['the','a','an','and','or','but','in','on','at','to','for','of','with','by']);
  const freq = {};
  for (let w of words) if (!stopwords.has(w) && w.length > 2) freq[w] = (freq[w]||0)+1;
  const sorted = Object.entries(freq).sort((a,b)=>b[1]-a[1]);
  return sorted.slice(0,3).map(kv => kv[0]);
}
module.exports = { parseUrl, autoTag };
```

#### 4.3 Short code generator (30 min)
`backend/src/services/shortCode.service.js`:
```javascript
const { customAlphabet } = require('nanoid'); // npm install nanoid
const alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
const nanoid = customAlphabet(alphabet, 6);
module.exports = () => nanoid();
```

#### 4.4 Link controller (3 hours)
`backend/src/controllers/link.controller.js` – implement create, getFeed, getOne, update, delete, vote, addReaction, removeReaction, random, recommendations.  
- `create`: use `parseUrl` if title missing, generate short code, auto-tag.
- `vote`: check existing, update vote count in links table.
- `recommendations`: join link_tags with user interests.

#### 4.5 Link routes (1 hour)
`backend/src/routes/link.route.js` – all endpoints, protected by authMiddleware.

#### 4.6 Test with Postman (2 hours)
Create link, fetch feed, vote, etc.

---

### Day 6-7 – Frontend Link CRUD (12 hours)

#### 6.1 SubmitLinkPage (4 hours)
`frontend/src/pages/SubmitLinkPage.jsx`:
- Form: URL, title, description, tags input (comma separated), private checkbox, allowed users (username autocomplete later).
- On submit: call `api.post('/links', formData)`
- Use `LinkForm` component with CSS modules.

#### 6.2 LinkCard component (2 hours)
`frontend/src/components/links/LinkCard.jsx`:
- Display title, description, short link, vote buttons, reaction buttons.
- Fetch preview image if available.

#### 6.3 HomePage feed (3 hours)
`HomePage.jsx`:
- Fetch `GET /links?type=following` (if logged in) or global.
- Infinite scroll using `useInfiniteScroll` hook.
- Map LinkCard components.

#### 6.4 LinkDetailPage (3 hours)
- Fetch single link by ID.
- Display full link, vote, reactions.
- Embed CommentThread component (to be built in Week 2).

**Test**: You can now register, login, post a link, see it on home page, view detail.

---

## Week 2 – Social, Comments, Chat, Shortener

### Day 8-9 – Follow System & Profile (8 hours)

#### 8.1 Follow model & controller (2 hours)
`backend/src/models/user.model.js` add methods: `follow`, `unfollow`, `getFollowers`, `getFollowing`.  
`backend/src/controllers/user.controller.js` – implement follow, unfollow, followers, following.

#### 8.2 ProfilePage frontend (3 hours)
- Fetch user data from `GET /users/:username`.
- Show user info, list of user's links (use LinkCard).
- Follow/unfollow button.

#### 8.3 Feed logic (2 hours)
Modify `link.controller.js` `getFeed` to accept `type=following` and join follows.

#### 8.4 Styling (1 hour)
Profile page CSS: avatar, stats, link grid.

---

### Day 10-11 – Infinite Nested Comments (8 hours)

#### 10.1 Comment model & controller (3 hours)
`backend/src/models/comment.model.js` – create, getTree (recursive CTE), update, delete, vote.  
`comment.controller.js` – handlers.

#### 10.2 Comment routes (1 hour)
`comment.route.js` – all endpoints.

#### 10.3 Frontend CommentThread component (3 hours)
`CommentThread.jsx` – recursive render.  
`CommentItem.jsx` – display content, vote button, reply button.  
`CommentForm.jsx` – form to post new comment or reply.

#### 10.4 Integrate into LinkDetailPage (1 hour)
Load comments using `GET /comments/link/:linkId`, pass to CommentThread.

---

### Day 12-13 – Real‑time Chat Rooms (12 hours)

#### 12.1 Room model & controller (3 hours)
`room.model.js` – create, addMember, removeMember, getRoomsForUser, deleteRoomIfEmpty.  
`room.controller.js` – list, create, invite, join, leave, delete, getMessages.

#### 12.2 Chat socket server (3 hours)
`backend/src/sockets/chat.socket.js` – handle join-room, leave-room, send-message, typing.  
Update `server.js` to attach Socket.io.

#### 12.3 Room cleanup cron (1 hour)
`roomCleanup.service.js` – node-cron every minute to delete rooms with no members and last_activity > 5 min.

#### 12.4 Frontend RoomsPage (2 hours)
List global rooms, button to create private room (name only). Show user's private rooms.

#### 12.5 ChatRoomPage (3 hours)
- Join room via Socket.io.
- Message list, input, typing indicator.
- Fetch old messages via REST.

#### 12.6 Styling (1 hour)
Chat bubbles, room list, invite modal.

---

### Day 14 – Link Shortener & Tools Page (6 hours)

#### 14.1 Backend shortener endpoints (2 hours)
`tools.controller.js` – `shorten` (standalone), `parse` (metadata), `redirect`.  
`tools.route.js`.  
Add redirect route `GET /s/:code` outside /api/v1.

#### 14.2 ToolsPage frontend (3 hours)
Two tabs using React state.  
Shortener tab: input URL, call `POST /shorten`, display short link with copy button.  
Parser tab: input URL, call `POST /parse`, display title, description, image.

#### 14.3 Styling (1 hour)
Tabs, copy button, loading states.

---

## Week 3 – Advanced Features, Graph, Polish

### Day 15-16 – Recommendations & Leaderboard (8 hours)

#### 15.1 Recommendations backend (2 hours)
`link.controller.js` – `recommendations`: query links where tags overlap with user.interests, order by upvote_count.

#### 15.2 Slider component frontend (3 hours)
`Slider.jsx` – horizontal scroll using CSS grid + overflow auto, fetch recommendations from API.

#### 15.3 Leaderboard backend & frontend (3 hours)
`leaderboard.controller.js` – rank users by sum of upvotes on their links, filter by period (week/month/all).  
`LeaderboardPage.jsx` – tabs for period, table with rank, username, karma.

---

### Day 17 – Graph Visualization (D3.js) (6 hours)

#### 17.1 Graph data endpoint (1 hour)
`graph.controller.js` – for a given tag, find all links with that tag, then find all links that share any tag with them, build nodes and edges.

#### 17.2 ForceGraph component (4 hours)
`ForceGraph.jsx` – use D3 force simulation, draw canvas, add hover tooltip (bubble) using mouse events, click to navigate.

#### 17.3 GraphPage (1 hour)
Input tag, fetch data, render ForceGraph.

---

### Day 18 – Gamification & Moderation (6 hours)

#### 18.1 Gamification service (2 hours)
`gamification.service.js` – cron daily: update streaks, award badges (update user profile with badge flags). No separate table, just compute on profile page.

#### 18.2 Moderation (2 hours)
- Add flag button on LinkCard: POST `/links/:id/flag` (increment flagged_count).
- Create admin middleware (check `is_admin`).
- Admin page: list links with flagged_count > 0, delete button.

#### 18.3 Frontend badges (1 hour)
Show badge icons on ProfilePage (e.g., 🔥 for streak > 7).

#### 18.4 Styling (1 hour)
Flag button, admin panel.

---

### Day 19 – PWA & Notifications (6 hours)

#### 19.1 PWA setup (2 hours)
`public/manifest.json` – name, icons, start_url.  
`public/sw.js` – simple cache for static assets.  
Register service worker in `main.jsx`.

#### 19.2 Notifications backend (2 hours)
`notification.model.js` – create, fetch unread, mark as read.  
Trigger when: someone replies to your comment, follows you, invites to room.

#### 19.3 Frontend notification bell (2 hours)
`NotificationBell.jsx` – dropdown list, mark as read, show count.

---

### Day 20 – Random Link, Auto‑tagging, Final Integration (6 hours)

#### 20.1 Random link endpoint (30 min)
`link.controller.js` – `random`: `SELECT id FROM links ORDER BY RANDOM() LIMIT 1` → redirect to `/link/:id`.

#### 20.2 Auto‑tagging (already in linkParser.service) – ensure it runs after link creation. (1 hour)

#### 20.3 Anonymous posting (1 hour)
Add checkbox in SubmitLinkPage; if true, set `userId` to a system user (create a user with username "anonymous" in DB).

#### 20.4 Promoted links (30 min)
Add `is_promoted` checkbox for admin; adjust feed query.

#### 20.5 Welcome message (1 hour)
In `link.controller.js` after insert, if user's total link count === 1, auto‑comment: "Welcome to Glinx!".

#### 20.6 Final testing of all 12 features (2 hours)

---

### Day 21 – Testing, Responsive Fixes, Deployment (8 hours)

#### 21.1 Cross‑browser & responsive testing (2 hours)
Test on Chrome, Firefox, Safari (or BrowserStack).  
Use devtools to check 320px, 768px, 1024px. Fix CSS.

#### 21.2 Performance optimizations (1 hour)
- Enable compression middleware on backend.
- Add `gzip` to frontend build.

#### 21.3 Environment variables (30 min)
Create `.env.production` for frontend with production API URL.

#### 21.4 Deploy backend to Render (2 hours)
- Push code to GitHub.
- On Render: New Web Service, connect repo, root directory `backend`, build command `npm install`, start command `node server.js`.
- Add environment variables (DATABASE_URL, JWT_SECRET, CLIENT_URL).
- Create free PostgreSQL on Render, copy internal URL.

#### 21.5 Deploy frontend to Netlify (1 hour)
- `npm run build` in frontend.
- Drag `dist` folder to Netlify drop zone.
- Set environment variable `VITE_API_URL` = Render backend URL.

#### 21.6 Final smoke test (1.5 hours)
- Register a new user.
- Post a link.
- Comment, upvote.
- Create a chat room, send message.
- Visit graph page for a tag.
- Test shortener tool.
- Confirm notifications appear.
- Check mobile layout.

---

## Daily Reminders for the One‑Man Army

- **Commit to Git** after every meaningful step (at least 3 times per day).
- **Write meaningful commit messages**.
- **Test each endpoint with Postman** before writing frontend.
- **Use console.log** liberally, then remove.
- **If stuck >30 minutes**, take a break or search Stack Overflow.
- **Keep the SRS open** in a separate tab.

You have everything. Go build Glinx.