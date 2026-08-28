import streamlit as st
import sqlite3
import json
import random
import string
import time

# ============================================================
# IPL MULTIPLAYER AUCTION
# ============================================================

st.set_page_config(
    page_title="IPL Multiplayer Auction",
    page_icon="🏏",
    layout="wide"
)

DB_FILE = "ipl_auction.db"

STARTING_PURSE = 120
MAX_SQUAD = 25
MAX_OVERSEAS = 8

TEAMS = [
    "CSK", "MI", "RCB", "KKR", "SRH",
    "RR", "PBKS", "DC", "GT", "LSG"
]

# ============================================================
# PLAYERS
# ============================================================

PLAYERS = [
    ("Virat Kohli", "Batsman", 8, 95, "India"),
    ("Rohit Sharma", "Batsman", 6, 91, "India"),
    ("Shubman Gill", "Batsman", 7, 91, "India"),
    ("Suryakumar Yadav", "Batsman", 8, 93, "India"),
    ("Yashasvi Jaiswal", "Batsman", 5, 90, "India"),
    ("Ruturaj Gaikwad", "Batsman", 5, 89, "India"),
    ("Rinku Singh", "Batsman", 2, 85, "India"),
    ("Shreyas Iyer", "Batsman", 4, 87, "India"),
    ("Tilak Varma", "Batsman", 2, 84, "India"),
    ("Abhishek Sharma", "Batsman", 2, 86, "India"),
    ("Devdutt Padikkal", "Batsman", 1, 78, "India"),
    ("Prithvi Shaw", "Batsman", 1, 76, "India"),
    ("Rajat Patidar", "Batsman", 2, 83, "India"),
    ("Sarfaraz Khan", "Batsman", 1, 78, "India"),
    ("Rahul Tripathi", "Batsman", 1, 80, "India"),
    ("Ayush Badoni", "Batsman", 1, 79, "India"),
    ("Sai Sudharsan", "Batsman", 2, 86, "India"),
    ("Rishabh Pant", "Wicketkeeper", 8, 92, "India"),
    ("KL Rahul", "Wicketkeeper", 6, 88, "India"),
    ("Sanju Samson", "Wicketkeeper", 5, 88, "India"),
    ("Jitesh Sharma", "Wicketkeeper", 2, 80, "India"),
    ("Dhruv Jurel", "Wicketkeeper", 2, 82, "India"),
    ("Phil Salt", "Wicketkeeper", 4, 89, "England"),
    ("Jos Buttler", "Wicketkeeper", 7, 94, "England"),
    ("Heinrich Klaasen", "Wicketkeeper", 7, 93, "South Africa"),
    ("Nicholas Pooran", "Wicketkeeper", 6, 91, "West Indies"),
    ("Quinton de Kock", "Wicketkeeper", 3, 87, "South Africa"),

    ("Ravindra Jadeja", "All Rounder", 7, 94, "India"),
    ("Hardik Pandya", "All Rounder", 7, 90, "India"),
    ("Axar Patel", "All Rounder", 5, 88, "India"),
    ("Shivam Dube", "All Rounder", 2, 84, "India"),
    ("Washington Sundar", "All Rounder", 2, 82, "India"),
    ("Nitish Kumar Reddy", "All Rounder", 2, 83, "India"),
    ("Rahul Tewatia", "All Rounder", 1, 80, "India"),
    ("Venkatesh Iyer", "All Rounder", 2, 82, "India"),
    ("Riyan Parag", "All Rounder", 2, 84, "India"),
    ("Liam Livingstone", "All Rounder", 4, 87, "England"),
    ("Glenn Maxwell", "All Rounder", 4, 88, "Australia"),
    ("Marcus Stoinis", "All Rounder", 3, 85, "Australia"),
    ("Cameron Green", "All Rounder", 5, 89, "Australia"),
    ("Sam Curran", "All Rounder", 5, 87, "England"),
    ("Andre Russell", "All Rounder", 5, 91, "West Indies"),
    ("Sunil Narine", "All Rounder", 4, 90, "West Indies"),
    ("Marco Jansen", "All Rounder", 3, 87, "South Africa"),

    ("Jasprit Bumrah", "Bowler", 10, 97, "India"),
    ("Mohammed Shami", "Bowler", 5, 89, "India"),
    ("Arshdeep Singh", "Bowler", 4, 86, "India"),
    ("Kuldeep Yadav", "Bowler", 4, 87, "India"),
    ("Mohammed Siraj", "Bowler", 4, 86, "India"),
    ("Yuzvendra Chahal", "Bowler", 3, 85, "India"),
    ("Varun Chakravarthy", "Bowler", 3, 87, "India"),
    ("Avesh Khan", "Bowler", 2, 81, "India"),
    ("Mukesh Kumar", "Bowler", 1, 78, "India"),
    ("T Natarajan", "Bowler", 2, 82, "India"),
    ("Mayank Yadav", "Bowler", 2, 86, "India"),
    ("Harshit Rana", "Bowler", 1, 80, "India"),
    ("Umran Malik", "Bowler", 1, 78, "India"),
    ("Ravi Bishnoi", "Bowler", 2, 83, "India"),
    ("Yash Dayal", "Bowler", 1, 80, "India"),
    ("Akash Madhwal", "Bowler", 1, 79, "India"),
    ("Suyash Sharma", "Bowler", 1, 76, "India"),

    ("Rashid Khan", "Bowler", 8, 96, "Afghanistan"),
    ("Pat Cummins", "Bowler", 8, 93, "Australia"),
    ("Mitchell Starc", "Bowler", 8, 94, "Australia"),
    ("Travis Head", "Batsman", 6, 92, "Australia"),
    ("David Warner", "Batsman", 4, 88, "Australia"),
    ("David Miller", "Batsman", 3, 86, "South Africa"),
    ("Kane Williamson", "Batsman", 2, 84, "New Zealand"),
    ("Faf du Plessis", "Batsman", 3, 87, "South Africa"),
    ("Jonny Bairstow", "Wicketkeeper", 2, 83, "England"),
    ("Devon Conway", "Wicketkeeper", 3, 86, "New Zealand"),
    ("Trent Boult", "Bowler", 3, 89, "New Zealand"),
    ("Lockie Ferguson", "Bowler", 2, 83, "New Zealand"),
    ("Kagiso Rabada", "Bowler", 4, 91, "South Africa"),
    ("Anrich Nortje", "Bowler", 3, 87, "South Africa"),
    ("Adam Zampa", "Bowler", 2, 84, "Australia"),

    ("Arjun Tendulkar", "Bowler", 1, 72, "India"),
    ("Sameer Rizvi", "Batsman", 1, 75, "India"),
    ("Shaik Rasheed", "Batsman", 1, 73, "India"),
    ("Manav Suthar", "Bowler", 1, 72, "India"),
    ("Kumar Kushagra", "Wicketkeeper", 1, 74, "India"),
    ("Nehal Wadhera", "Batsman", 1, 78, "India"),
    ("Shahrukh Khan", "All Rounder", 1, 77, "India"),
    ("Naman Dhir", "All Rounder", 1, 76, "India"),
    ("Angkrish Raghuvanshi", "Batsman", 1, 79, "India"),
    ("Tanush Kotian", "All Rounder", 1, 76, "India"),
    ("Vijaykumar Vyshak", "Bowler", 1, 75, "India"),
]

# ============================================================
# DATABASE
# ============================================================

def db():
    con = sqlite3.connect(DB_FILE, timeout=10)
    con.row_factory = sqlite3.Row
    return con


def setup_database():
    con = db()

    con.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            room TEXT PRIMARY KEY,
            host TEXT,
            started INTEGER DEFAULT 0,
            player_index INTEGER DEFAULT 0,
            current_player TEXT,
            current_bid REAL DEFAULT 0,
            highest_bidder TEXT,
            status TEXT DEFAULT 'waiting',
            message TEXT DEFAULT ''
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            room TEXT,
            team TEXT,
            owner TEXT,
            purse REAL DEFAULT 120,
            squad TEXT DEFAULT '[]',
            PRIMARY KEY(room, team)
        )
    """)

    con.commit()
    con.close()


setup_database()

# ============================================================
# HELPERS
# ============================================================

def make_room():
    chars = string.ascii_uppercase + string.digits
    while True:
        code = "".join(random.choice(chars) for _ in range(5))
        con = db()
        found = con.execute(
            "SELECT room FROM rooms WHERE room=?",
            (code,)
        ).fetchone()
        con.close()

        if not found:
            return code


def get_room(room):
    con = db()
    row = con.execute(
        "SELECT * FROM rooms WHERE room=?",
        (room,)
    ).fetchone()
    con.close()
    return row


def get_teams(room):
    con = db()
    rows = con.execute(
        "SELECT * FROM teams WHERE room=? ORDER BY team",
        (room,)
    ).fetchall()
    con.close()
    return rows


def get_team(room, team):
    con = db()
    row = con.execute(
        "SELECT * FROM teams WHERE room=? AND team=?",
        (room, team)
    ).fetchone()
    con.close()
    return row


def get_squad(team_row):
    return json.loads(team_row["squad"])


def overseas_count(squad):
    return sum(
        1 for p in squad
        if p["country"] != "India"
    )


def can_buy(team_row, player):
    squad = get_squad(team_row)

    if len(squad) >= MAX_SQUAD:
        return False

    if player["country"] != "India":
        if overseas_count(squad) >= MAX_OVERSEAS:
            return False

    return team_row["purse"] >= player["base"]


def player_from_json(value):
    if not value:
        return None
    return json.loads(value)


def player_to_json(player):
    return json.dumps(player)


def update_room(room, **values):
    if not values:
        return

    con = db()

    fields = []
    params = []

    for key, value in values.items():
        fields.append(f"{key}=?")
        params.append(value)

    params.append(room)

    con.execute(
        f"UPDATE rooms SET {', '.join(fields)} WHERE room=?",
        params
    )

    con.commit()
    con.close()


def update_team(room, team, purse=None, squad=None, owner=None):
    con = db()

    if purse is not None:
        con.execute(
            "UPDATE teams SET purse=? WHERE room=? AND team=?",
            (purse, room, team)
        )

    if squad is not None:
        con.execute(
            "UPDATE teams SET squad=? WHERE room=? AND team=?",
            (json.dumps(squad), room, team)
        )

    if owner is not None:
        con.execute(
            "UPDATE teams SET owner=? WHERE room=? AND team=?",
            (owner, room, team)
        )

    con.commit()
    con.close()


# ============================================================
# ROOM CREATION
# ============================================================

def create_room(host_name):
    room = make_room()

    shuffled = PLAYERS.copy()
    random.shuffle(shuffled)

    con = db()

    con.execute(
        """
        INSERT INTO rooms
        (room, host, started, player_index, current_player,
         current_bid, highest_bidder, status, message)
        VALUES (?, ?, 0, 0, ?, 0, '', 'waiting', '')
        """,
        (room, host_name, json.dumps(shuffled))
    )

    for team in TEAMS:
        con.execute(
            """
            INSERT INTO teams
            (room, team, owner, purse, squad)
            VALUES (?, ?, '', 120, '[]')
            """,
            (room, team)
        )

    con.commit()
    con.close()

    return room


# ============================================================
# START AUCTION
# ============================================================

def start_auction(room):
    row = get_room(room)

    if not row:
        return

    players = json.loads(row["current_player"])

    if len(players) == 0:
        return

    player = players[0]
    remaining = players[1:]

    update_room(
        room,
        started=1,
        player_index=1,
        current_player=json.dumps(player),
        current_bid=player[2],
        highest_bidder="",
        status="auction",
        message="Auction started!"
    )

    # Save remaining players in current_player temporarily
    # using player_index is enough to determine order.
    con = db()

    # Store player pool separately if not already available.
    con.execute("""
        CREATE TABLE IF NOT EXISTS pools (
            room TEXT PRIMARY KEY,
            players TEXT
        )
    """)

    con.execute(
        """
        INSERT OR REPLACE INTO pools(room, players)
        VALUES (?, ?)
        """,
        (room, json.dumps(remaining))
    )

    con.commit()
    con.close()


# ============================================================
# POOL
# ============================================================

def get_pool(room):
    con = db()
    con.execute("""
        CREATE TABLE IF NOT EXISTS pools (
            room TEXT PRIMARY KEY,
            players TEXT
        )
    """)

    row = con.execute(
        "SELECT players FROM pools WHERE room=?",
        (room,)
    ).fetchone()

    con.close()

    if not row:
        return []

    return json.loads(row["players"])


def save_pool(room, players):
    con = db()

    con.execute("""
        CREATE TABLE IF NOT EXISTS pools (
            room TEXT PRIMARY KEY,
            players TEXT
        )
    """)

    con.execute(
        """
        INSERT OR REPLACE INTO pools(room, players)
        VALUES (?, ?)
        """,
        (room, json.dumps(players))
    )

    con.commit()
    con.close()


# ============================================================
# NEXT PLAYER
# ============================================================

def next_player(room):

    pool = get_pool(room)

    if not pool:
        update_room(
            room,
            current_player="",
            current_bid=0,
            highest_bidder="",
            status="finished",
            message="🎉 AUCTION FINISHED!"
        )
        return

    player = pool.pop(0)
    save_pool(room, pool)

    update_room(
        room,
        current_player=json.dumps(player),
        current_bid=player[2],
        highest_bidder="",
        status="auction",
        message=f"Next player: {player[0]}"
    )


# ============================================================
# JOIN TEAM
# ============================================================

def join_team(room, team, username):

    existing = get_team(room, team)

    if not existing:
        return "Team does not exist."

    if existing["owner"] and existing["owner"] != username:
        return "❌ This team is already taken."

    # Check whether user already owns another team
    con = db()

    other = con.execute(
        """
        SELECT team FROM teams
        WHERE room=? AND owner=? AND team!=?
        """,
        (room, username, team)
    ).fetchone()

    con.close()

    if other:
        return "❌ You already selected a team."

    update_team(
        room,
        team,
        owner=username
    )

    return f"✅ You are now controlling {team}."


# ============================================================
# BID
# ============================================================

def place_bid(room, username):

    room_row = get_room(room)

    if not room_row:
        return

    player = player_from_json(room_row["current_player"])

    if not player:
        return

    team_row = get_team(room, room_row["highest_bidder"])

    # Find user's team
    con = db()

    user_team = con.execute(
        """
        SELECT * FROM teams
        WHERE room=? AND owner=?
        """,
        (room, username)
    ).fetchone()

    con.close()

    if not user_team:
        update_room(
            room,
            message="❌ Choose a team first."
        )
        return

    if not can_buy(user_team, {
        "name": player[0],
        "role": player[1],
        "base": player[2],
        "rating": player[3],
        "country": player[4]
    }):
        update_room(
            room,
            message="❌ Your team cannot bid on this player."
        )
        return

    current_bid = room_row["current_bid"]

    # Bid increment
    if current_bid < 5:
        increment = 1
    elif current_bid < 10:
        increment = 1
    else:
        increment = 2

    new_bid = current_bid + increment

    if new_bid > user_team["purse"]:
        update_room(
            room,
            message="❌ Not enough money in your purse."
        )
        return

    update_room(
        room,
        current_bid=new_bid,
        highest_bidder=user_team["team"],
        message=f"🔥 {user_team['team']} bids ₹{new_bid} Cr!"
    )


# ============================================================
# SELL
# ============================================================

def sell_player(room, username):

    room_row = get_room(room)

    if not room_row:
        return

    player_data = player_from_json(
        room_row["current_player"]
    )

    if not player_data:
        return

    player = {
        "name": player_data[0],
        "role": player_data[1],
        "base": player_data[2],
        "rating": player_data[3],
        "country": player_data[4]
    }

    winner = room_row["highest_bidder"]

    if not winner:
        update_room(
            room,
            message=f"❌ {player['name']} went UNSOLD."
        )
        time.sleep(0.3)
        next_player(room)
        return

    team_row = get_team(room, winner)

    if not team_row:
        return

    squad = get_squad(team_row)

    if not can_buy(team_row, player):
        update_room(
            room,
            message="❌ Winning team cannot complete this purchase."
        )
        return

    new_purse = team_row["purse"] - room_row["current_bid"]

    squad.append(player)

    update_team(
        room,
        winner,
        purse=new_purse,
        squad=squad
    )

    update_room(
        room,
        message=(
            f"🔨 SOLD! {player['name']} → "
            f"{winner} for ₹{room_row['current_bid']} Cr"
        )
    )

    time.sleep(0.4)

    next_player(room)


# ============================================================
# HOST CHECK
# ============================================================

def is_host(room, username):
    row = get_room(room)

    return row and row["host"] == username


# ============================================================
# SESSION
# ============================================================

if "username" not in st.session_state:
    st.session_state.username = ""

if "room" not in st.session_state:
    st.session_state.room = ""

# ============================================================
# HEADER
# ============================================================

st.title("🏏 IPL MULTIPLAYER AUCTION")
st.caption(
    "₹120 Cr Purse • 25 Players • 8 Overseas • Live Room"
)

# ============================================================
# HOME
# ============================================================

if not st.session_state.room:

    st.subheader("👤 Enter your name")

    username = st.text_input(
        "Player name",
        placeholder="Example: Harish"
    )

    st.divider()

    left, right = st.columns(2)

    # --------------------------------------------------------
    # CREATE ROOM
    # --------------------------------------------------------

    with left:

        st.header("🎮 Create Room")

        if st.button(
            "CREATE NEW ROOM",
            use_container_width=True
        ):

            if not username.strip():
                st.error("Enter your name first.")
            else:
                room = create_room(username.strip())

                st.session_state.username = username.strip()
                st.session_state.room = room

                st.rerun()

    # --------------------------------------------------------
    # JOIN ROOM
    # --------------------------------------------------------

    with right:

        st.header("🚪 Join Room")

        room_code = st.text_input(
            "Room code",
            placeholder="Example: A7K2P"
        )

        if st.button(
            "JOIN ROOM",
            use_container_width=True
        ):

            room_code = room_code.strip().upper()

            if not username.strip():
                st.error("Enter your name first.")

            elif not room_code:
                st.error("Enter a room code.")

            elif not get_room(room_code):
                st.error("❌ Room not found.")

            else:
                st.session_state.username = username.strip()
                st.session_state.room = room_code

                st.rerun()

    st.stop()

# ============================================================
# ROOM
# ============================================================

room_code = st.session_state.room
username = st.session_state.username

room = get_room(room_code)

if not room:

    st.error("❌ This room no longer exists.")

    if st.button("Return Home"):
        st.session_state.room = ""
        st.rerun()

    st.stop()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🎮 ROOM")

    st.code(room_code)

    st.write(f"👤 **{username}**")

    if st.button("🚪 Leave Room"):
        st.session_state.room = ""
        st.session_state.username = ""
        st.rerun()

    st.divider()

    st.header("🏏 Teams")

    teams = get_teams(room_code)

    for team in teams:

        owner = team["owner"]

        if owner:
            st.write(
                f"🔒 **{team['team']}** — {owner}"
            )
        else:
            st.write(
                f"🟢 **{team['team']}** — Available"
            )

# ============================================================
# WAITING ROOM
# ============================================================

if room["status"] == "waiting":

    st.header("🎮 Waiting Room")

    st.success(
        f"Your room code is **{room_code}**"
    )

    st.markdown(
        "### 📱 Send this room code to your friends"
    )

    st.code(room_code)

    st.info(
        "Everyone should open the same Streamlit link, "
        "enter their name, and join this room."
    )

    st.divider()

    st.subheader("🏏 Choose your IPL team")

    available_teams = [
        t["team"]
        for t in teams
        if not t["owner"]
    ]

    if available_teams:

        selected_team = st.selectbox(
            "Available teams",
            available_teams
        )

        if st.button(
            "✅ JOIN SELECTED TEAM",
            use_container_width=True
        ):

            message = join_team(
                room_code,
                selected_team,
                username
            )

            if message.startswith("❌"):
                st.error(message)
            else:
                st.success(message)

            st.rerun()

    else:
        st.warning("All teams are currently taken.")

    st.divider()

    st.subheader("👥 Players in room")

    for team in teams:

        if team["owner"]:

            st.write(
                f"🏏 **{team['team']}** — "
                f"{team['owner']}"
            )

    # Host controls
    if is_host(room_code, username):

        st.divider()

        st.subheader("👑 HOST")

        joined = [
            t for t in teams
            if t["owner"]
        ]

        st.write(
            f"{len(joined)}/10 teams selected"
        )

        if len(joined) >= 1:

            if st.button(
                "🚀 START AUCTION",
                use_container_width=True
            ):

                start_auction(room_code)
                st.rerun()

    # Auto refresh
    time.sleep(2)
    st.rerun()

# ============================================================
# FINISHED
# ============================================================

if room["status"] == "finished":

    st.success("🏆 AUCTION FINISHED!")

    st.header("📊 FINAL TEAMS")

    teams = get_teams(room_code)

    for team in teams:

        squad = get_squad(team)

        with st.expander(
            f"🏏 {team['team']} — "
            f"{len(squad)} players — "
            f"₹{team['purse']} Cr remaining"
        ):

            if not squad:
                st.write("No players.")

            for p in squad:

                st.write(
                    f"• **{p['name']}** — "
                    f"{p['role']} — "
                    f"{p['country']}"
                )

    st.stop()

# ============================================================
# AUCTION
# ============================================================

room = get_room(room_code)

player_data = player_from_json(
    room["current_player"]
)

if not player_data:

    st.warning("Preparing next player...")
    time.sleep(1)
    st.rerun()

player = {
    "name": player_data[0],
    "role": player_data[1],
    "base": player_data[2],
    "rating": player_data[3],
    "country": player_data[4]
}

# ============================================================
# PLAYER DISPLAY
# ============================================================

st.header("🔥 LIVE AUCTION")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Current Bid",
        f"₹{room['current_bid']} Cr"
    )

with col2:
    bidder = room["highest_bidder"]

    st.metric(
        "👑 Highest Bidder",
        bidder if bidder else "No bids"
    )

with col3:
    pool = get_pool(room_code)

    st.metric(
        "📦 Players Remaining",
        len(pool)
    )

st.divider()

# ============================================================
# PLAYER CARD
# ============================================================

st.subheader("🏏 CURRENT PLAYER")

p1, p2 = st.columns([2, 1])

with p1:

    st.markdown(
        f"# {player['name']}"
    )

    st.write(
        f"**Role:** {player['role']}"
    )

    st.write(
        f"**Country:** {player['country']}"
    )

with p2:

    st.metric(
        "⭐ Rating",
        f"{player['rating']}/100"
    )

    st.metric(
        "💵 Base Price",
        f"₹{player['base']} Cr"
    )

# ============================================================
# MESSAGE
# ============================================================

if room["message"]:

    st.info(room["message"])

# ============================================================
# USER TEAM
# ============================================================

user_team = None

for team in get_teams(room_code):

    if team["owner"] == username:
        user_team = team
        break

# ============================================================
# USER TEAM INFORMATION
# ============================================================

if user_team:

    squad = get_squad(user_team)

    st.divider()

    st.subheader(
        f"🏏 YOUR TEAM — {user_team['team']}"
    )

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "💰 Purse",
            f"₹{user_team['purse']} Cr"
        )

    with b:
        st.metric(
            "👥 Squad",
            f"{len(squad)}/{MAX_SQUAD}"
        )

    with c:
        st.metric(
            "🌍 Overseas",
            f"{overseas_count(squad)}/{MAX_OVERSEAS}"
        )

# ============================================================
# BIDDING
# ============================================================

st.divider()

if user_team:

    current_winner = room["highest_bidder"]

    if current_winner == user_team["team"]:

        st.success(
            "🔥 YOU ARE THE HIGHEST BIDDER!"
        )

    bid_disabled = (
        current_winner == user_team["team"]
        or not can_buy(user_team, player)
    )

    if st.button(
        "💰 BID",
        disabled=bid_disabled,
        use_container_width=True
    ):

        place_bid(
            room_code,
            username
        )

        st.rerun()

    if current_winner == user_team["team"]:

        st.warning(
            "You are currently winning. "
            "Wait for another player to bid."
        )

    if not can_buy(user_team, player):

        st.error(
            "Your team cannot bid on this player "
            "(purse, squad or overseas limit)."
        )

else:

    st.warning(
        "You have not selected a team."
    )

# ============================================================
# HOST SELL BUTTON
# ============================================================

if is_host(room_code, username):

    st.divider()

    st.subheader("👑 HOST CONTROLS")

    if room["highest_bidder"]:

        st.write(
            f"Highest bidder: **{room['highest_bidder']}**"
        )

        if st.button(
            "🔨 HAMMER — SELL PLAYER",
            use_container_width=True
        ):

            sell_player(
                room_code,
                username
            )

            st.rerun()

    else:

        if st.button(
            "❌ UNSOLD / NEXT PLAYER",
            use_container_width=True
        ):

            next_player(room_code)
            st.rerun()

# ============================================================
# ALL TEAMS
# ============================================================

st.divider()

st.header("📊 LIVE TEAM STATUS")

teams = get_teams(room_code)

for team in teams:

    squad = get_squad(team)

    with st.expander(
        f"{team['team']} — "
        f"₹{team['purse']} Cr — "
        f"{len(squad)}/25 players"
    ):

        if team["owner"]:
            st.write(
                f"👤 Owner: **{team['owner']}**"
            )
        else:
            st.write("🟢 Computer / available")

        st.write(
            f"🌍 Overseas: "
            f"{overseas_count(squad)}/8"
        )

        if squad:

            for p in squad:

                st.write(
                    f"• {p['name']} — "
                    f"{p['role']}"
                )

# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(2)
st.rerun()
