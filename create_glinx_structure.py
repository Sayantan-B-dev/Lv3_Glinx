import os

PROJECT_ROOT = "Glinqx"

# ------------------------------------------------------------
# Backend structure (all paths are relative to PROJECT_ROOT)
# ------------------------------------------------------------
backend_dirs = [
    "backend/src/config",
    "backend/src/controllers",
    "backend/src/middleware",
    "backend/src/models",
    "backend/src/services",
    "backend/src/sockets",
    "backend/src/routes",
    "backend/src/utils",
]

backend_files = [
    "backend/server.js",
    "backend/package.json",
    "backend/.env",
    "backend/src/app.js",
    "backend/src/config/db.js",
    "backend/src/controllers/auth.controller.js",
    "backend/src/controllers/link.controller.js",
    "backend/src/controllers/comment.controller.js",
    "backend/src/controllers/user.controller.js",
    "backend/src/controllers/room.controller.js",
    "backend/src/controllers/tag.controller.js",
    "backend/src/controllers/tools.controller.js",
    "backend/src/controllers/leaderboard.controller.js",
    "backend/src/controllers/graph.controller.js",
    "backend/src/middleware/auth.middleware.js",
    "backend/src/middleware/rateLimiter.middleware.js",
    "backend/src/middleware/errorHandler.middleware.js",
    "backend/src/models/user.model.js",
    "backend/src/models/link.model.js",
    "backend/src/models/comment.model.js",
    "backend/src/models/room.model.js",
    "backend/src/models/tag.model.js",
    "backend/src/models/shortlink.model.js",
    "backend/src/services/linkParser.service.js",
    "backend/src/services/gamification.service.js",
    "backend/src/services/notification.service.js",
    "backend/src/services/shortCode.service.js",
    "backend/src/services/roomCleanup.service.js",
    "backend/src/sockets/chat.socket.js",
    "backend/src/routes/auth.route.js",
    "backend/src/routes/link.route.js",
    "backend/src/routes/comment.route.js",
    "backend/src/routes/user.route.js",
    "backend/src/routes/room.route.js",
    "backend/src/routes/tag.route.js",
    "backend/src/routes/tools.route.js",
    "backend/src/routes/leaderboard.route.js",
    "backend/src/routes/graph.route.js",
    "backend/src/utils/jwt.util.js",
    "backend/src/utils/hash.util.js",
    "backend/src/utils/validators.util.js",
]

# ------------------------------------------------------------
# Frontend structure
# ------------------------------------------------------------
frontend_dirs = [
    "frontend/public",
    "frontend/src/components/common",
    "frontend/src/components/links",
    "frontend/src/components/comments",
    "frontend/src/components/rooms",
    "frontend/src/components/graph",
    "frontend/src/components/recommendations",
    "frontend/src/pages",
    "frontend/src/styles/themes",
    "frontend/src/contexts",
    "frontend/src/hooks",
    "frontend/src/services",
    "frontend/src/utils",
]

frontend_files = [
    "frontend/public/manifest.json",
    "frontend/public/sw.js",
    "frontend/src/components/common/Navbar.jsx",
    "frontend/src/components/common/Navbar.module.css",
    "frontend/src/components/common/Footer.jsx",
    "frontend/src/components/common/Footer.module.css",
    "frontend/src/components/common/LoadingSpinner.jsx",
    "frontend/src/components/common/LoadingSpinner.module.css",
    "frontend/src/components/common/ErrorMessage.jsx",
    "frontend/src/components/common/ErrorMessage.module.css",
    "frontend/src/components/links/LinkCard.jsx",
    "frontend/src/components/links/LinkCard.module.css",
    "frontend/src/components/links/LinkForm.jsx",
    "frontend/src/components/links/LinkForm.module.css",
    "frontend/src/components/links/ReactionButtons.jsx",
    "frontend/src/components/links/ReactionButtons.module.css",
    "frontend/src/components/links/VoteButtons.jsx",
    "frontend/src/components/links/VoteButtons.module.css",
    "frontend/src/components/comments/CommentThread.jsx",
    "frontend/src/components/comments/CommentThread.module.css",
    "frontend/src/components/comments/CommentItem.jsx",
    "frontend/src/components/comments/CommentItem.module.css",
    "frontend/src/components/comments/CommentForm.jsx",
    "frontend/src/components/comments/CommentForm.module.css",
    "frontend/src/components/rooms/ChatRoom.jsx",
    "frontend/src/components/rooms/ChatRoom.module.css",
    "frontend/src/components/rooms/MessageList.jsx",
    "frontend/src/components/rooms/MessageList.module.css",
    "frontend/src/components/rooms/MessageInput.jsx",
    "frontend/src/components/rooms/MessageInput.module.css",
    "frontend/src/components/graph/ForceGraph.jsx",
    "frontend/src/components/graph/ForceGraph.module.css",
    "frontend/src/components/recommendations/Slider.jsx",
    "frontend/src/components/recommendations/Slider.module.css",
    "frontend/src/pages/HomePage.jsx",
    "frontend/src/pages/HomePage.module.css",
    "frontend/src/pages/LoginPage.jsx",
    "frontend/src/pages/LoginPage.module.css",
    "frontend/src/pages/RegisterPage.jsx",
    "frontend/src/pages/RegisterPage.module.css",
    "frontend/src/pages/ProfilePage.jsx",
    "frontend/src/pages/ProfilePage.module.css",
    "frontend/src/pages/LinkDetailPage.jsx",
    "frontend/src/pages/LinkDetailPage.module.css",
    "frontend/src/pages/SubmitLinkPage.jsx",
    "frontend/src/pages/SubmitLinkPage.module.css",
    "frontend/src/pages/ExplorePage.jsx",
    "frontend/src/pages/ExplorePage.module.css",
    "frontend/src/pages/GraphPage.jsx",
    "frontend/src/pages/GraphPage.module.css",
    "frontend/src/pages/RoomsPage.jsx",
    "frontend/src/pages/RoomsPage.module.css",
    "frontend/src/pages/ChatRoomPage.jsx",
    "frontend/src/pages/ChatRoomPage.module.css",
    "frontend/src/pages/ToolsPage.jsx",
    "frontend/src/pages/ToolsPage.module.css",
    "frontend/src/pages/LeaderboardPage.jsx",
    "frontend/src/pages/LeaderboardPage.module.css",
    "frontend/src/pages/RandomLinkPage.jsx",
    "frontend/src/pages/RandomLinkPage.module.css",
    "frontend/src/styles/index.css",
    "frontend/src/styles/variables.css",
    "frontend/src/styles/typography.css",
    "frontend/src/styles/utilities.css",
    "frontend/src/styles/animations.css",
    "frontend/src/styles/themes/light.css",
    "frontend/src/contexts/AuthContext.jsx",
    "frontend/src/contexts/SocketContext.jsx",
    "frontend/src/hooks/useAuth.js",
    "frontend/src/hooks/useSocket.js",
    "frontend/src/hooks/useInfiniteScroll.js",
    "frontend/src/services/api.js",
    "frontend/src/services/socket.js",
    "frontend/src/utils/formatDate.js",
    "frontend/src/App.jsx",
    "frontend/src/main.jsx",
    "frontend/src/index.css",
    "frontend/index.html",
    "frontend/vite.config.js",
    "frontend/package.json",
]

# ------------------------------------------------------------
# Root files (no subdirectory, placed directly under PROJECT_ROOT)
# ------------------------------------------------------------
root_files = [
    "database/init.sql",
    ".gitignore",
    "README.md",
    "docker-compose.yml",
]

def create_structure():
    # Create the main project folder
    os.makedirs(PROJECT_ROOT, exist_ok=True)
    original_dir = os.getcwd()
    os.chdir(PROJECT_ROOT)

    # Helper to create directories and empty files
    def touch_file(filepath):
        parent = os.path.dirname(filepath)
        if parent:  # only create parent dir if it's not empty
            os.makedirs(parent, exist_ok=True)
        with open(filepath, 'w') as f:
            pass  # create empty file

    # Create backend directories
    for d in backend_dirs:
        os.makedirs(d, exist_ok=True)

    # Create backend files
    for f in backend_files:
        touch_file(f)

    # Create frontend directories
    for d in frontend_dirs:
        os.makedirs(d, exist_ok=True)

    # Create frontend files
    for f in frontend_files:
        touch_file(f)

    # Create root files (including database/init.sql)
    for f in root_files:
        touch_file(f)

    # Change back to original directory
    os.chdir(original_dir)
    print(f"✅ Project structure created successfully inside '{PROJECT_ROOT}' folder.")

if __name__ == "__main__":
    create_structure()