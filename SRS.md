# Glinqx – ABSOLUTE FINAL SRS (One‑Man Army, Pure CSS, 3 Weeks)

This document is **complete**. Every required feature, every route, every file name, every CSS detail is here. No section is missing.

---

## Table of Contents

- [Glinqx – ABSOLUTE FINAL SRS (One‑Man Army, Pure CSS, 3 Weeks)](#Glinqx--absolute-final-srs-oneman-army-pure-css-3-weeks)
  - [Table of Contents](#table-of-contents)
  - [1. Product Vision \& Core Features](#1-product-vision--core-features)
    - [1.1 Must‑have (no compromise)](#11-musthave-no-compromise)
  - [2. Tech Stack – Pure CSS, Free Tier](#2-tech-stack--pure-css-free-tier)
  - [3. CSS Architecture (Pure CSS, No Frameworks)](#3-css-architecture-pure-css-no-frameworks)
    - [3.1 Global files (`frontend/src/styles/`)](#31-global-files-frontendsrcstyles)
    - [3.2 Component CSS (CSS Modules)](#32-component-css-css-modules)
    - [3.3 Naming Conventions (BEM inside modules – optional but recommended)](#33-naming-conventions-bem-inside-modules--optional-but-recommended)
    - [3.4 Responsive breakpoints (defined in `variables.css`)](#34-responsive-breakpoints-defined-in-variablescss)
  - [4. Database Schema (PostgreSQL)](#4-database-schema-postgresql)
  - [5. API Routes – REST + WebSocket](#5-api-routes--rest--websocket)
    - [5.1 REST Endpoints (`/api/v1`)](#51-rest-endpoints-apiv1)
    - [5.2 WebSocket Events (Socket.io)](#52-websocket-events-socketio)
  - [6. Frontend Pages (React Router)](#6-frontend-pages-react-router)
  - [7. Folder Structure with Naming Conventions](#7-folder-structure-with-naming-conventions)
  - [8. Step‑by‑Week 3‑Week Development Plan](#8-stepbyweek-3week-development-plan)
    - [Week 1 – Core CRUD + Auth + CSS Foundation](#week-1--core-crud--auth--css-foundation)
    - [Week 2 – Social, Comments, Chat, Shortener](#week-2--social-comments-chat-shortener)
    - [Week 3 – Advanced Features, Graph, Polish](#week-3--advanced-features-graph-polish)
  - [9. Real‑time Chat Implementation](#9-realtime-chat-implementation)
    - [Backend (`sockets/chat.socket.js`)](#backend-socketschatsocketjs)
    - [Room auto‑delete (cron)](#room-autodelete-cron)
  - [10. Infinite Nested Comments (Reddit Style)](#10-infinite-nested-comments-reddit-style)
    - [Backend query (recursive CTE)](#backend-query-recursive-cte)
    - [Frontend recursive component](#frontend-recursive-component)
  - [11. Graph Visualization (D3.js)](#11-graph-visualization-d3js)
    - [API endpoint: `GET /graph/:tag`](#api-endpoint-get-graphtag)
    - [Frontend component (`ForceGraph.jsx`)](#frontend-component-forcegraphjsx)
  - [12. Link Shortener \& Tools Page](#12-link-shortener--tools-page)
  - [13. All 12 Advanced Features – Implementation Map](#13-all-12-advanced-features--implementation-map)
  - [14. Frontend Advanced Concepts (Pure CSS)](#14-frontend-advanced-concepts-pure-css)
  - [15. Low‑end PC \& Free Tier Optimizations](#15-lowend-pc--free-tier-optimizations)
  - [16. Environment Variables \& Deployment](#16-environment-variables--deployment)
    - [Backend `.env`](#backend-env)
    - [Frontend `.env`](#frontend-env)
    - [Deployment steps](#deployment-steps)
  - [17. System Design Diagram (Mermaid)](#17-system-design-diagram-mermaid)
  - [18. Documentation \& Learning Resources](#18-documentation--learning-resources)
  - [19. Final Checklist Before Launch](#19-final-checklist-before-launch)

---

## 1. Product Vision & Core Features

**Glinqx** – social bookmarking + real‑time chat + graph discovery.

### 1.1 Must‑have (no compromise)
- User system: register, login (JWT httpOnly), profile, follow/unfollow, block, interests
- Link CRUD: post URL + title + description + tags; edit/delete; upvote/downvote; multiple reactions (❤️ 🔥 💡 😂 🚀)
- Private links (visible only to allowed users by ID)
- Link preview (auto‑fetch title, image, description via scraper)
- Infinite nested comments (Reddit style) with upvotes
- Social feed (followed users), global explore
- Leaderboard (global + per tag)
- Real‑time chat: global rooms + private invite‑only rooms; auto‑delete room when empty for 5 minutes
- Recommendation slider (based on user interests)
- Random link button
- Graph visualization (D3) for related links by tag
- Standalone tools: link shortener, link content parser
- All 12 advanced features (auto‑tagging, streaks, badges, moderation, etc.)

---

## 2. Tech Stack – Pure CSS, Free Tier

| Area | Technology | Version |
|------|------------|---------|
| Frontend | React + Vite | React 18, Vite 4 |
| Styling | **Pure CSS** + CSS Modules + BEM | no frameworks |
| State | React Context + useReducer | – |
| Routing | React Router v6 | – |
| HTTP | Axios | – |
| Real‑time | Socket.io (client & server) | 4.x |
| Backend | Node.js + Express | 18.x |
| Database | PostgreSQL | 14+ (neon.tech free) |
| DB driver | `pg` + raw SQL | – |
| Auth | JWT (httpOnly cookie) + bcrypt | – |
| Scraping | cheerio + node-fetch | – |
| Graph | D3.js | 7.x |
| Cron | node-cron | – |
| Deployment | Render (backend + PG) + Netlify (frontend) | free tier |

No paid services. No Tailwind. No Redis.

---

## 3. CSS Architecture (Pure CSS, No Frameworks)

### 3.1 Global files (`frontend/src/styles/`)

| File | Purpose |
|------|---------|
| `index.css` | entry point (imports all below) |
| `variables.css` | CSS custom properties (colors, spacing, breakpoints) |
| `typography.css` | headings, body, links, fonts |
| `utilities.css` | helper classes (`.flex`, `.mt-2`, `.text-center`) |
| `animations.css` | keyframes, transitions, loaders |
| `themes/light.css` | light theme (default) – can add dark later |

### 3.2 Component CSS (CSS Modules)
Each component `.jsx` has a matching `.module.css` in the same folder.  
Example: `LinkCard.jsx` + `LinkCard.module.css`

### 3.3 Naming Conventions (BEM inside modules – optional but recommended)
```css
.link-card { }
.link-card__title { }
.link-card--featured { }
```

### 3.4 Responsive breakpoints (defined in `variables.css`)
```css
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
```

---

## 4. Database Schema (PostgreSQL)

Execute `database/init.sql` once.

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  bio TEXT,
  avatar_url TEXT,
  interests TEXT[],
  karma INT DEFAULT 0,
  streak INT DEFAULT 0,
  last_post_date DATE,
  is_admin BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Follows
CREATE TABLE follows (
  follower_id UUID REFERENCES users(id) ON DELETE CASCADE,
  followee_id UUID REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (follower_id, followee_id)
);

-- Blocks
CREATE TABLE blocks (
  blocker_id UUID REFERENCES users(id),
  blocked_id UUID REFERENCES users(id),
  PRIMARY KEY (blocker_id, blocked_id)
);

-- Links
CREATE TABLE links (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  original_url TEXT NOT NULL,
  short_code VARCHAR(20) UNIQUE,
  title VARCHAR(500) NOT NULL,
  description TEXT,
  is_private BOOLEAN DEFAULT false,
  private_allowed_users UUID[] DEFAULT '{}',
  is_promoted BOOLEAN DEFAULT false,
  flagged_count INT DEFAULT 0,
  upvote_count INT DEFAULT 0,
  downvote_count INT DEFAULT 0,
  comment_count INT DEFAULT 0,
  view_count INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Tags
CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  normalized_name VARCHAR(100) UNIQUE NOT NULL,
  usage_count INT DEFAULT 0
);

-- Link-Tag
CREATE TABLE link_tags (
  link_id UUID REFERENCES links(id) ON DELETE CASCADE,
  tag_id INT REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (link_id, tag_id)
);

-- Link votes (1 = up, -1 = down)
CREATE TABLE link_votes (
  user_id UUID REFERENCES users(id),
  link_id UUID REFERENCES links(id),
  vote SMALLINT CHECK (vote IN (1, -1)),
  PRIMARY KEY (user_id, link_id)
);

-- Link reactions
CREATE TABLE link_reactions (
  user_id UUID REFERENCES users(id),
  link_id UUID REFERENCES links(id),
  reaction_type VARCHAR(20) CHECK (reaction_type IN ('like','hot','insightful','funny','rocket')),
  PRIMARY KEY (user_id, link_id, reaction_type)
);

-- Comments (infinite nesting)
CREATE TABLE comments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  link_id UUID REFERENCES links(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id),
  parent_id UUID REFERENCES comments(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  upvote_count INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Comment votes (only up)
CREATE TABLE comment_votes (
  user_id UUID REFERENCES users(id),
  comment_id UUID REFERENCES comments(id),
  PRIMARY KEY (user_id, comment_id)
);

-- Chat rooms
CREATE TABLE rooms (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(100) NOT NULL,
  is_global BOOLEAN DEFAULT false,
  owner_id UUID REFERENCES users(id),
  invite_code VARCHAR(20) UNIQUE,
  last_activity TIMESTAMP DEFAULT NOW()
);

-- Room members
CREATE TABLE room_members (
  room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id),
  joined_at TIMESTAMP DEFAULT NOW(),
  left_at TIMESTAMP,
  PRIMARY KEY (room_id, user_id)
);

-- Messages
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id),
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Standalone shortlinks (tool)
CREATE TABLE shortlinks (
  id SERIAL PRIMARY KEY,
  short_code VARCHAR(20) UNIQUE NOT NULL,
  original_url TEXT NOT NULL,
  user_id UUID REFERENCES users(id),
  click_count INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Notifications
CREATE TABLE notifications (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  type VARCHAR(50),
  content TEXT,
  is_read BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_links_user_id ON links(user_id);
CREATE INDEX idx_links_created_at ON links(created_at DESC);
CREATE INDEX idx_links_short_code ON links(short_code);
CREATE INDEX idx_comments_link_id ON comments(link_id);
CREATE INDEX idx_comments_parent_id ON comments(parent_id);
CREATE INDEX idx_rooms_last_activity ON rooms(last_activity);
CREATE INDEX idx_messages_room_id ON messages(room_id);
CREATE INDEX idx_tags_normalized ON tags(normalized_name);
```

---

## 5. API Routes – REST + WebSocket

### 5.1 REST Endpoints (`/api/v1`)

| Method | Route | Controller method |
|--------|-------|-------------------|
| POST | `/auth/register` | auth.register |
| POST | `/auth/login` | auth.login |
| POST | `/auth/logout` | auth.logout |
| GET | `/auth/me` | auth.me |
| GET | `/links` | link.getFeed |
| POST | `/links` | link.create |
| GET | `/links/:id` | link.getOne |
| PUT | `/links/:id` | link.update |
| DELETE | `/links/:id` | link.delete |
| POST | `/links/:id/vote` | link.vote |
| POST | `/links/:id/reaction` | link.addReaction |
| DELETE | `/links/:id/reaction` | link.removeReaction |
| GET | `/comments/link/:linkId` | comment.getTree |
| POST | `/comments` | comment.create |
| PUT | `/comments/:id` | comment.update |
| DELETE | `/comments/:id` | comment.delete |
| POST | `/comments/:id/vote` | comment.vote |
| GET | `/users/:username` | user.getProfile |
| POST | `/users/:id/follow` | user.follow |
| DELETE | `/users/:id/follow` | user.unfollow |
| GET | `/users/:id/followers` | user.followers |
| GET | `/users/:id/following` | user.following |
| GET | `/users/:id/links` | user.links |
| PUT | `/users/me` | user.update |
| GET | `/tags` | tag.list |
| GET | `/tags/:name/links` | tag.links |
| GET | `/rooms` | room.list |
| POST | `/rooms` | room.create |
| POST | `/rooms/:id/invite` | room.invite |
| POST | `/rooms/:id/join` | room.join |
| DELETE | `/rooms/:id/leave` | room.leave |
| DELETE | `/rooms/:id` | room.delete |
| GET | `/rooms/:id/messages` | room.messages |
| POST | `/shorten` | tools.shorten |
| GET | `/s/:code` | tools.redirect |
| POST | `/parse` | tools.parse |
| GET | `/leaderboard` | leaderboard.global |
| GET | `/random-link` | link.random |
| GET | `/recommendations` | link.recommendations |
| GET | `/graph/:tag` | graph.data |

### 5.2 WebSocket Events (Socket.io)

| Client → Server | Payload |
|----------------|---------|
| `join-room` | `{ roomId }` |
| `leave-room` | `{ roomId }` |
| `send-message` | `{ roomId, content }` |
| `typing` | `{ roomId, isTyping }` |

| Server → Client | Payload |
|----------------|---------|
| `new-message` | `{ id, userId, username, content, createdAt }` |
| `user-joined` | `{ userId, username }` |
| `user-left` | `{ userId, username }` |
| `typing` | `{ userId, isTyping }` |

---

## 6. Frontend Pages (React Router)

All pages are lazy‑loaded using `React.lazy()` for code splitting.

| Path | Component | Description |
|------|-----------|-------------|
| `/` | `HomePage` | Feed (followed users + recommendations) |
| `/login` | `LoginPage` | Login form |
| `/register` | `RegisterPage` | Registration with interest selection |
| `/profile/:username` | `ProfilePage` | User profile, links, follow button |
| `/link/:id` | `LinkDetailPage` | Single link with comments & reactions |
| `/submit` | `SubmitLinkPage` | Form to post a new link |
| `/explore` | `ExplorePage` | Global links, tag cloud, popular |
| `/graph/:tag` | `GraphPage` | D3 graph for a specific tag |
| `/rooms` | `RoomsPage` | List global rooms, create private room |
| `/room/:id` | `ChatRoomPage` | Real‑time chat room |
| `/tools` | `ToolsPage` | Link shortener + link parser (two tabs) |
| `/leaderboard` | `LeaderboardPage` | Global leaderboard (week/month/all) |
| `/random` | `RandomLinkPage` | Redirects to a random link |

---

## 7. Folder Structure with Naming Conventions

**Naming rules:**
- Controllers: `resource.controller.js` (e.g., `auth.controller.js`)
- Models: `resource.model.js` (e.g., `user.model.js`)
- Services: `serviceName.service.js` (e.g., `linkParser.service.js`)
- Middleware: `name.middleware.js`
- Routes: `resource.route.js`
- Frontend components: `ComponentName.jsx` + `ComponentName.module.css`
- Frontend pages: `PageName.jsx` + `PageName.module.css`

```
Glinqx/
├── backend/
│   ├── src/
│   │   ├── config/
│   │   │   └── db.js
│   │   ├── controllers/
│   │   │   ├── auth.controller.js
│   │   │   ├── link.controller.js
│   │   │   ├── comment.controller.js
│   │   │   ├── user.controller.js
│   │   │   ├── room.controller.js
│   │   │   ├── tag.controller.js
│   │   │   ├── tools.controller.js
│   │   │   ├── leaderboard.controller.js
│   │   │   └── graph.controller.js
│   │   ├── middleware/
│   │   │   ├── auth.middleware.js
│   │   │   ├── rateLimiter.middleware.js
│   │   │   └── errorHandler.middleware.js
│   │   ├── models/
│   │   │   ├── user.model.js
│   │   │   ├── link.model.js
│   │   │   ├── comment.model.js
│   │   │   ├── room.model.js
│   │   │   ├── tag.model.js
│   │   │   └── shortlink.model.js
│   │   ├── services/
│   │   │   ├── linkParser.service.js
│   │   │   ├── gamification.service.js
│   │   │   ├── notification.service.js
│   │   │   ├── shortCode.service.js
│   │   │   └── roomCleanup.service.js
│   │   ├── sockets/
│   │   │   └── chat.socket.js
│   │   ├── routes/
│   │   │   ├── auth.route.js
│   │   │   ├── link.route.js
│   │   │   ├── comment.route.js
│   │   │   ├── user.route.js
│   │   │   ├── room.route.js
│   │   │   ├── tag.route.js
│   │   │   ├── tools.route.js
│   │   │   ├── leaderboard.route.js
│   │   │   └── graph.route.js
│   │   ├── utils/
│   │   │   ├── jwt.util.js
│   │   │   ├── hash.util.js
│   │   │   └── validators.util.js
│   │   └── app.js
│   ├── server.js
│   ├── package.json
│   └── .env
├── frontend/
│   ├── public/
│   │   ├── manifest.json
│   │   └── sw.js
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Navbar.jsx / Navbar.module.css
│   │   │   │   ├── Footer.jsx / Footer.module.css
│   │   │   │   ├── LoadingSpinner.jsx / LoadingSpinner.module.css
│   │   │   │   └── ErrorMessage.jsx / ErrorMessage.module.css
│   │   │   ├── links/
│   │   │   │   ├── LinkCard.jsx / LinkCard.module.css
│   │   │   │   ├── LinkForm.jsx / LinkForm.module.css
│   │   │   │   ├── ReactionButtons.jsx / ReactionButtons.module.css
│   │   │   │   └── VoteButtons.jsx / VoteButtons.module.css
│   │   │   ├── comments/
│   │   │   │   ├── CommentThread.jsx / CommentThread.module.css
│   │   │   │   ├── CommentItem.jsx / CommentItem.module.css
│   │   │   │   └── CommentForm.jsx / CommentForm.module.css
│   │   │   ├── rooms/
│   │   │   │   ├── ChatRoom.jsx / ChatRoom.module.css
│   │   │   │   ├── MessageList.jsx / MessageList.module.css
│   │   │   │   └── MessageInput.jsx / MessageInput.module.css
│   │   │   ├── graph/
│   │   │   │   ├── ForceGraph.jsx / ForceGraph.module.css
│   │   │   └── recommendations/
│   │   │       ├── Slider.jsx / Slider.module.css
│   │   ├── pages/
│   │   │   ├── HomePage.jsx / HomePage.module.css
│   │   │   ├── LoginPage.jsx / LoginPage.module.css
│   │   │   ├── RegisterPage.jsx / RegisterPage.module.css
│   │   │   ├── ProfilePage.jsx / ProfilePage.module.css
│   │   │   ├── LinkDetailPage.jsx / LinkDetailPage.module.css
│   │   │   ├── SubmitLinkPage.jsx / SubmitLinkPage.module.css
│   │   │   ├── ExplorePage.jsx / ExplorePage.module.css
│   │   │   ├── GraphPage.jsx / GraphPage.module.css
│   │   │   ├── RoomsPage.jsx / RoomsPage.module.css
│   │   │   ├── ChatRoomPage.jsx / ChatRoomPage.module.css
│   │   │   ├── ToolsPage.jsx / ToolsPage.module.css
│   │   │   ├── LeaderboardPage.jsx / LeaderboardPage.module.css
│   │   │   └── RandomLinkPage.jsx / RandomLinkPage.module.css
│   │   ├── styles/
│   │   │   ├── index.css
│   │   │   ├── variables.css
│   │   │   ├── typography.css
│   │   │   ├── utilities.css
│   │   │   ├── animations.css
│   │   │   └── themes/light.css
│   │   ├── contexts/
│   │   │   ├── AuthContext.jsx
│   │   │   └── SocketContext.jsx
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── useSocket.js
│   │   │   └── useInfiniteScroll.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── socket.js
│   │   ├── utils/
│   │   │   └── formatDate.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css   (imports ./styles/index.css)
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── database/
│   └── init.sql
├── .gitignore
├── README.md
└── docker-compose.yml (optional)
```

---

## 8. Step‑by‑Week 3‑Week Development Plan

### Week 1 – Core CRUD + Auth + CSS Foundation

**Day 1-2:** Backend setup + PostgreSQL + `init.sql` + Express server  
**Day 3:** CSS foundation – `styles/` folder, variables, utilities, Navbar styling  
**Day 4-5:** Auth backend + frontend (Login, Register, AuthContext)  
**Day 6-7:** Link CRUD – backend models + controllers, frontend `SubmitLinkPage`, `LinkCard`, link preview scraper, short code generation  

### Week 2 – Social, Comments, Chat, Shortener

**Day 8-9:** Follow system + Profile page + Home feed (following)  
**Day 10-11:** Infinite nested comments – recursive CTE + frontend recursive component  
**Day 12-13:** Real‑time chat – rooms, messages, Socket.io, room auto‑cleanup cron  
**Day 14:** Tools page – standalone shortener + link parser (two tabs)  

### Week 3 – Advanced Features, Graph, Polish

**Day 15-16:** Recommendations slider + Leaderboard (global + period)  
**Day 17:** Graph visualization – D3 force graph for tags  
**Day 18:** Gamification (streaks, badges) + Moderation (flag links, admin page)  
**Day 19:** PWA + Notifications (bell, reply/follow notifications)  
**Day 20:** Random link, auto‑tagging, final integration of all 12 advanced features  
**Day 21:** Testing, responsive fixes, deployment (Render + Netlify)  

---

## 9. Real‑time Chat Implementation

### Backend (`sockets/chat.socket.js`)
```javascript
module.exports = (io, socket) => {
  socket.on('join-room', async ({ roomId }) => {
    socket.join(roomId);
    // add to room_members table if not already (left_at null)
    socket.to(roomId).emit('user-joined', { userId: socket.userId, username: socket.username });
  });
  socket.on('send-message', async ({ roomId, content }) => {
    const message = await saveMessage(roomId, socket.userId, content);
    io.to(roomId).emit('new-message', message);
    // update room.last_activity
  });
  socket.on('typing', ({ roomId, isTyping }) => {
    socket.to(roomId).emit('typing', { userId: socket.userId, isTyping });
  });
};
```

### Room auto‑delete (cron)
```javascript
// services/roomCleanup.service.js
const cron = require('node-cron');
cron.schedule('* * * * *', async () => {
  await db.query(`
    DELETE FROM rooms 
    WHERE id NOT IN (SELECT room_id FROM room_members WHERE left_at IS NULL)
    AND last_activity < NOW() - INTERVAL '5 minutes'
  `);
});
```

---

## 10. Infinite Nested Comments (Reddit Style)

### Backend query (recursive CTE)
```sql
WITH RECURSIVE comment_tree AS (
  SELECT id, parent_id, content, user_id, created_at, upvote_count,
         0 as depth, ARRAY[id] as path
  FROM comments WHERE link_id = $1 AND parent_id IS NULL
  UNION ALL
  SELECT c.id, c.parent_id, c.content, c.user_id, c.created_at, c.upvote_count,
         ct.depth + 1, ct.path || c.id
  FROM comments c JOIN comment_tree ct ON c.parent_id = ct.id
)
SELECT * FROM comment_tree ORDER BY path;
```

### Frontend recursive component
```jsx
function CommentThread({ comments, onReply, onVote }) {
  return comments.map(comment => (
    <div key={comment.id} style={{ marginLeft: comment.depth * 20 }}>
      <CommentItem comment={comment} onReply={onReply} onVote={onVote} />
      {comment.replies?.length > 0 && (
        <CommentThread comments={comment.replies} onReply={onReply} onVote={onVote} />
      )}
    </div>
  ));
}
```

---

## 11. Graph Visualization (D3.js)

### API endpoint: `GET /graph/:tag`
Returns:
```json
{
  "nodes": [
    { "id": "uuid1", "title": "React docs", "url": "/link/uuid1", "tags": ["react","js"] }
  ],
  "links": [
    { "source": "uuid1", "target": "uuid2", "sharedTag": "js" }
  ]
}
```

### Frontend component (`ForceGraph.jsx`)
- Uses `useEffect` + D3 force simulation.
- Hover shows bubble (tooltip) with title.
- Click navigates to link page.

---

## 12. Link Shortener & Tools Page

- **Every link** gets a `short_code` automatically (6 char base62) stored in `links` table.
- **Standalone tool** `POST /shorten` → store in `shortlinks` table.
- **Redirect** `GET /s/:code` → check `links` first, then `shortlinks` → increment click_count → 302 redirect.
- **ToolsPage** has two tabs (CSS‑only or React state):
  - Tab 1: Shortener – input URL, display short link + copy button.
  - Tab 2: Parser – input URL, show title, description, image preview.

---

## 13. All 12 Advanced Features – Implementation Map

| # | Feature | File location | Implementation summary |
|---|---------|---------------|------------------------|
| 1 | Auto‑tagging | `services/linkParser.service.js` | After link creation, extract keywords from title+desc (TF‑IDF lite), create missing tags, associate top 3 |
| 2 | Streaks & Badges | `services/gamification.service.js` (cron daily) | Update `users.streak` if `last_post_date = yesterday`; award badges on profile when karma > 1000 or links > 100 |
| 3 | Moderation | `routes/admin.route.js` + `link.controller.js` | Flag button increments `links.flagged_count`; admin page lists flagged links with delete option |
| 4 | Live cursor | `sockets/liveCursor.socket.js` (optional) | On link detail page, emit `viewing` to room; broadcast to others – skip if time low |
| 5 | Daily digest | `jobs/dailyDigest.service.js` (cron + nodemailer) | Every day at 9am, fetch top 5 links from followed users (last 24h) and send email |
| 6 | 3D graph | Not implemented | Future enhancement (Three.js) |
| 7 | API & extension | All routes RESTful | Browser extension separate repo later |
| 8 | Anonymous posting | `SubmitLinkPage` checkbox | If checked, set `link.user_id` to system anonymous UUID |
| 9 | Promoted links | `links.is_promoted` boolean | In feed queries, `ORDER BY is_promoted DESC, created_at DESC` |
| 10 | PWA | `public/manifest.json`, `sw.js` | Register service worker in `main.jsx`; cache static assets |
| 11 | Click tracking | `shortlinks.click_count`, `links.view_count` | Increment on redirect and on link detail page view |
| 12 | Welcome message | `link.controller.js` after create | If user's total link count == 1, auto‑comment from system user: “Welcome to Glinqx!” |

---

## 14. Frontend Advanced Concepts (Pure CSS)

- **Context + useReducer** – for Auth and Socket.
- **Infinite scroll** – custom hook `useInfiniteScroll` with IntersectionObserver.
- **Debounced search** – for tag input (lodash.debounce).
- **Optimistic UI** – update vote count immediately, revert on error.
- **Code splitting** – `React.lazy()` for GraphPage, ChatRoomPage, LeaderboardPage.
- **Error boundaries** – class component to catch rendering errors.
- **Pure CSS animations** – all micro‑interactions with `transition` and `keyframes`.

---

## 15. Low‑end PC & Free Tier Optimizations

- **Backend:** `pg` pool size 5, enable `compression` middleware, rate limiting (express-rate-limit).
- **Frontend:** Vite builds fast, lazy load routes, no heavy UI libraries.
- **Database:** All indexes from schema, use `EXPLAIN` for slow queries.
- **Deployment:** Render free web service (sleeps after 15 min inactivity, wakes on request). Netlify free hosting.
- **No external APIs** – scraping, shortener self‑hosted.

---

## 16. Environment Variables & Deployment

### Backend `.env`
```
PORT=5000
DATABASE_URL=postgresql://user:pass@host:5432/Glinqx
JWT_SECRET=your_super_secret_key
CLIENT_URL=http://localhost:5173
SMTP_HOST=...
SMTP_USER=...
SMTP_PASS=...
```

### Frontend `.env`
```
VITE_API_URL=http://localhost:5000
VITE_WS_URL=ws://localhost:5000
```

### Deployment steps
1. Push code to GitHub.
2. Backend: on Render.com – new Web Service, connect repo, set build command `npm install`, start command `node server.js`, add environment variables.
3. Database: on Render.com – new PostgreSQL (free), copy internal URL to backend env.
4. Frontend: `npm run build`, drag `dist` folder to Netlify (or connect GitHub).
5. Update `VITE_API_URL` to Render backend URL, rebuild frontend.

---

## 17. System Design Diagram (Mermaid)

```mermaid
graph TB
    Client[Browser Client] -->|HTTP / WS| Backend[Express + Socket.io]
    Backend -->|Raw SQL| PG[(PostgreSQL)]
    Backend -->|Cron| Cleanup[Room Cleanup]
    Backend -->|Cheerio| Scraper[Link Parser]
    Client -->|React| Frontend[Vite + React]
    Frontend -->|CSS Modules| Styles[Pure CSS]
    Frontend -->|Axios| Backend
    Frontend -->|Socket.io| Backend
```

---

## 18. Documentation & Learning Resources

| Topic | Free Resource |
|-------|---------------|
| PostgreSQL recursive queries | [Postgres Tutorial](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-recursive-query/) |
| D3 force graph | [Observable – Force Directed Graph](https://observablehq.com/@d3/force-directed-graph) |
| Socket.io chat | [Official Get Started](https://socket.io/get-started/chat) |
| JWT httpOnly cookie | [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html) |
| CSS Modules in Vite | [Vite CSS Modules](https://vitejs.dev/guide/features.html#css-modules) |
| BEM methodology | [getbem.com](http://getbem.com/) |
| Deploy to Render | [Render Node + Postgres](https://render.com/docs/deploy-node-express-app) |
| Deploy to Netlify | [Netlify React](https://www.netlify.com/blog/2016/07/22/deploy-a-react-app-in-minutes/) |
| Cheerio scraping | [Cheerio docs](https://cheerio.js.org/) |

---

## 19. Final Checklist Before Launch

- [ ] All API endpoints tested with Postman.
- [ ] Frontend builds without errors (`npm run build`).
- [ ] Infinite comments load and display correctly.
- [ ] Real‑time chat works across multiple tabs.
- [ ] Rooms auto‑delete after 5 minutes empty.
- [ ] Link shortener redirects and counts clicks.
- [ ] Graph renders for existing tags.
- [ ] PWA installable on mobile.
- [ ] Notifications appear for replies/follows.
- [ ] Responsive design on 320px, 768px, 1024px.
- [ ] No console errors or warnings.
- [ ] Environment variables set on Render & Netlify.
- [ ] `robots.txt` and `sitemap.xml` (optional but good).

---

**You now have the absolute final SRS. Start building. One man, three weeks, pure CSS, no compromises. Good luck.**