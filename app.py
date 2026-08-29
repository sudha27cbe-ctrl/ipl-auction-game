import streamlit as st
import requests
import random
import string
import time

# ============================================================
# SETTINGS
# ============================================================

st.set_page_config(
    page_title="IPL Multiplayer Auction",
    page_icon="🏏",
    layout="wide"
)

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

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

    ("Rishabh Pant", "Wicketkeeper", 8, 92, "India"),
    ("KL Rahul", "Wicketkeeper", 6, 88, "India"),
    ("Sanju Samson", "Wicketkeeper", 5, 88, "India"),
    ("Jitesh Sharma", "Wicketkeeper", 2, 80, "India"),
    ("Jos Buttler", "Wicketkeeper", 7, 94, "England"),
    ("Heinrich Klaasen", "Wicketkeeper", 7, 93, "South Africa"),
    ("Nicholas Pooran", "Wicketkeeper", 6, 91, "West Indies"),

    ("Ravindra Jadeja", "All Rounder", 7, 94, "India"),
    ("Hardik Pandya", "All Rounder", 7, 90, "India"),
    ("Axar Patel", "All Rounder", 5, 88, "India"),
    ("Shivam Dube", "All Rounder", 2, 84, "India"),
    ("Washington Sundar", "All Rounder", 2, 82, "India"),
    ("Riyan Parag", "All Rounder", 2, 84, "India"),
    ("Liam Livingstone", "All Rounder", 4, 87, "England"),
    ("Glenn Maxwell", "All Rounder", 4, 88, "Australia"),
    ("Marcus Stoinis", "All Rounder", 3, 85, "Australia"),
    ("Cameron Green", "All Rounder", 5, 89, "Australia"),
    ("Sam Curran", "All Rounder", 5, 87, "England"),
    ("Andre Russell", "All Rounder", 5, 91, "West Indies"),
    ("Sunil Narine", "All Rounder", 4, 90, "West Indies"),

    ("Jasprit Bumrah", "Bowler", 10, 97, "India"),
    ("Mohammed Shami", "Bowler", 5, 89, "India"),
    ("Arshdeep Singh", "Bowler", 4, 86, "India"),
    ("Kuldeep Yadav", "Bowler", 4, 87, "India"),
    ("Mohammed Siraj", "Bowler", 4, 86, "India"),
    ("Yuzvendra Chahal", "Bowler", 3, 85, "India"),
    ("Varun Chakravarthy", "Bowler", 3, 87, "India"),
    ("Avesh Khan", "Bowler", 2, 81, "India"),
    ("Mayank Yadav", "Bowler", 2, 86, "India"),
    ("Ravi Bishnoi", "Bowler", 2, 83, "India"),

    ("Rashid Khan", "Bowler", 8, 96, "Afghanistan"),
    ("Pat Cummins", "Bowler", 8, 93, "Australia"),
    ("Mitchell Starc", "Bowler", 8, 94, "Australia"),
    ("Travis Head", "Batsman", 6, 92, "Australia"),
    ("David Warner", "Batsman", 4, 88, "Australia"),
    ("David Miller", "Batsman", 3, 86, "South Africa"),
    ("Kane Williamson", "Batsman", 2, 84, "New Zealand"),
    ("Faf du Plessis", "Batsman", 3, 87, "South Africa"),
    ("Trent Boult", "Bowler", 3, 89, "New Zealand"),
    ("Kagiso Rabada", "Bowler", 4, 91, "South Africa"),

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
]

# ============================================================
# SUPABASE FUNCTIONS
# ============================================================

def api(table, params=None):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    r = requests.get(url, headers=HEADERS, params=params, timeout=10)
    if not r.ok:
        st.error(f"Database error: {r.text}")
        return []
    return r.json()


def insert(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = {**HEADERS, "Prefer": "return=representation"}
    r = requests.post(url, headers=headers, json=data, timeout=10)

    if not r.ok:
        st.error(f"Database error: {r.text}")
        return None

    return r.json()


def update(table, data, params):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = {**HEADERS, "Prefer": "return=representation"}
    r = requests.patch(
        url,
        headers=headers,
        params=params,
        json=data,
        timeout=10
    )

    if not r.ok:
        st.error(f"Database error: {r.text}")
        return None

    return r.json()


def get_room(code):
    rows = api(
        "auction_rooms",
        {"room_code": f"eq.{code}", "limit": "1"}
    )
    return rows[0] if rows else None


def get_teams(code):
    return api(
        "auction_teams",
        {
            "room_code": f"eq.{code}",
            "order": "team_name.asc"
        }
    )


def get_team(code, team_name):
    rows = api(
        "auction_teams",
        {
            "room_code": f"eq.{code}",
            "team_name": f"eq.{team_name}",
            "limit": "1"
        }
    )
    return rows[0] if rows else None


def update_room(code, data):
    return update(
        "auction_rooms",
        data,
        {"room_code": f"eq.{code}"}
    )


def update_team(team_id, data):
    return update(
        "auction_teams",
        data,
        {"id": f"eq.{team_id}"}
    )


# ============================================================
# ROOM CREATION
# ============================================================

def generate_room():
    chars = string.ascii_uppercase + string.digits

    for _ in range(100):
        code = "".join(random.choice(chars) for _ in range(5))

        if not get_room(code):
            return code

    return None


def create_room(host):
    code = generate_room()

    if not code:
        return None

    players = PLAYERS.copy()
    random.shuffle(players)

    room_data = {
        "room_code": code,
        "host_name": host,
        "status": "waiting",
        "current_player": None,
        "current_bid": 0,
        "highest_bidder": "",
        "players": players
    }

    result = insert("auction_rooms", room_data)

    if not result:
        return None

    team_data = []

    for team in TEAMS:
        team_data.append({
            "room_code": code,
            "team_name": team,
            "owner_name": "",
            "purse": STARTING_PURSE,
            "squad": []
        })

    result = insert("auction_teams", team_data)

    if result is None:
        return None

    return code


# ============================================================
# TEAM FUNCTIONS
# ============================================================

def join_team(room_code, team_name, username):

    teams = get_teams(room_code)

    for team in teams:
        if (
            team["owner_name"] == username
            and team["team_name"] != team_name
        ):
            return "❌ You already selected another team."

    team = get_team(room_code, team_name)

    if not team:
        return "❌ Team not found."

    if team["owner_name"]:
        return "❌ This team is already taken."

    result = update_team(
        team["id"],
        {"owner_name": username}
    )

    if result:
        return f"✅ You selected {team_name}."

    return "❌ Could not select team."


def user_team(room_code, username):

    teams = get_teams(room_code)

    for team in teams:
        if team["owner_name"] == username:
            return team

    return None


# ============================================================
# AUCTION FUNCTIONS
# ============================================================

def start_auction(room_code):

    room = get_room(room_code)

    if not room:
        return

    players = room["players"]

    if not players:
        return

    player = players[0]
    remaining = players[1:]

    update_room(
        room_code,
        {
            "status": "auction",
            "current_player": player,
            "current_bid": player[2],
            "highest_bidder": "",
            "players": remaining
        }
    )


def next_player(room_code):

    room = get_room(room_code)

    if not room:
        return

    players = room["players"]

    if not players:
        update_room(
            room_code,
            {
                "status": "finished",
                "current_player": None,
                "current_bid": 0,
                "highest_bidder": "",
            }
        )
        return

    player = players[0]

    update_room(
        room_code,
        {
            "current_player": player,
            "current_bid": player[2],
            "highest_bidder": "",
            "players": players[1:]
        }
    )


def overseas_count(squad):
    return sum(
        1 for p in squad
        if p["country"] != "India"
    )


def can_buy(team, player):
    squad = team["squad"] or []

    if len(squad) >= MAX_SQUAD:
        return False

    if isinstance(player, list):
        country = player[4]
        base_price = float(player[2])
    else:
        country = player.get("country", "India")
        base_price = float(player.get("base", 0))

    if country != "India" and overseas_count(squad) >= MAX_OVERSEAS:
        return False

    return float(team["purse"]) >= base_price

    squad = team["squad"] or []

    if len(squad) >= MAX_SQUAD:
        return False

    if (
        player["country"] != "India"
        and overseas_count(squad) >= MAX_OVERSEAS
    ):
        return False

    return team["purse"] >= player["base"]


def place_bid(room_code, username):

    room = get_room(room_code)
    team = user_team(room_code, username)

    if not room or not team:
        return

    player = room["current_player"]

    if not player:
        return

    if room["highest_bidder"] == team["team_name"]:
        return

    if not can_buy(team, player):
        update_room(
            room_code,
            {
                "message": "❌ Your team cannot bid for this player."
            }
        )
        return

    current = float(room["current_bid"])

    if current < 10:
        increment = 1
    else:
        increment = 2

    new_bid = current + increment

    if new_bid > float(team["purse"]):
        update_room(
            room_code,
            {
                "message": "❌ Not enough purse."
            }
        )
        return

    update_room(
        room_code,
        {
            "current_bid": new_bid,
            "highest_bidder": team["team_name"],
            "message": f"🔥 {team['team_name']} bids ₹{new_bid} Cr!"
        }
    )


def sell_player(room_code):

    room = get_room(room_code)

    if not room:
        return

    player = room["current_player"]
    winner = room["highest_bidder"]

    if not player:
        return

    if not winner:
        update_room(
            room_code,
            {
                "message": f"❌ {player[0]} went UNSOLD."
            }
        )
        next_player(room_code)
        return

    team = get_team(room_code, winner)

    if not team:
        return

    squad = team["squad"] or []

    player_data = {
        "name": player[0],
        "role": player[1],
        "base": player[2],
        "rating": player[3],
        "country": player[4]
    }

    squad.append(player_data)

    new_purse = float(team["purse"]) - float(room["current_bid"])

    update_team(
        team["id"],
        {
            "purse": new_purse,
            "squad": squad
        }
    )

    update_room(
        room_code,
        {
            "message":
                f"🔨 SOLD! {player[0]} → "
                f"{winner} for ₹{room['current_bid']} Cr"
        }
    )

    time.sleep(0.5)

    next_player(room_code)


# ============================================================
# SESSION
# ============================================================

if "username" not in st.session_state:
    st.session_state.username = ""

if "room" not in st.session_state:
    st.session_state.room = ""


# ============================================================
# HOME
# ============================================================

if not st.session_state.room:

    st.title("🏏 IPL MULTIPLAYER AUCTION")

    st.subheader("👤 Enter your name")

    username = st.text_input(
        "Player name",
        placeholder="Example: Harish"
    )

    st.divider()

    col1, col2 = st.columns(2)

    # CREATE
    with col1:

        st.header("🎮 Create Room")

        if st.button(
            "CREATE NEW ROOM",
            use_container_width=True
        ):

            if not username.strip():
                st.error("Enter your name.")

            else:

                with st.spinner("Creating room..."):

                    code = create_room(
                        username.strip()
                    )

                if code:

                    st.session_state.username = username.strip()
                    st.session_state.room = code

                    st.rerun()

    # JOIN
    with col2:

        st.header("🚪 Join Room")

        room_code = st.text_input(
            "Room code",
            placeholder="Example: A7K2P"
        )

        if st.button(
            "JOIN ROOM",
            use_container_width=True
        ):

            if not username.strip():

                st.error("Enter your name.")

            elif not room_code.strip():

                st.error("Enter room code.")

            else:

                code = room_code.strip().upper()

                if get_room(code):

                    st.session_state.username = username.strip()
                    st.session_state.room = code

                    st.rerun()

                else:

                    st.error("❌ Room not found.")

    st.stop()


# ============================================================
# LOAD ROOM
# ============================================================

room_code = st.session_state.room
username = st.session_state.username

room = get_room(room_code)

if not room:

    st.error("❌ Room not found.")

    if st.button("Return Home"):

        st.session_state.room = ""
        st.session_state.username = ""

        st.rerun()

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

teams = get_teams(room_code)

with st.sidebar:

    st.title("🏏 IPL AUCTION")

    st.write("### Room Code")

    st.code(room_code)

    st.write(f"👤 **{username}**")

    if st.button(
        "🚪 Leave Room",
        use_container_width=True
    ):

        st.session_state.room = ""
        st.session_state.username = ""

        st.rerun()

    st.divider()

    st.write("### 🏏 Teams")

    for team in teams:

        if team["owner_name"]:

            st.write(
                f"🔒 **{team['team_name']}** "
                f"— {team['owner_name']}"
            )

        else:

            st.write(
                f"🟢 **{team['team_name']}** "
                f"— Available"
            )


# ============================================================
# WAITING ROOM
# ============================================================

if room["status"] == "waiting":

    st.title("🎮 Waiting Room")

    st.success(
        f"ROOM CODE: **{room_code}**"
    )

    st.info(
        "Send your Streamlit game link and this "
        "room code to your friends."
    )

    st.code(room_code)

    st.divider()

    st.subheader("🏏 Choose Your Team")

    available = [
        t["team_name"]
        for t in teams
        if not t["owner_name"]
    ]

    current_team = user_team(
        room_code,
        username
    )

    if current_team:

        st.success(
            f"You are controlling "
            f"**{current_team['team_name']}**"
        )

    elif available:

        selected = st.selectbox(
            "Available teams",
            available
        )

        if st.button(
            "✅ JOIN TEAM",
            use_container_width=True
        ):

            result = join_team(
                room_code,
                selected,
                username
            )

            if result.startswith("❌"):
                st.error(result)
            else:
                st.success(result)

            time.sleep(0.5)
            st.rerun()

    st.divider()

    joined = [
        t for t in teams
        if t["owner_name"]
    ]

    st.subheader(
        f"👥 Players: {len(joined)}"
    )

    for team in joined:

        st.write(
            f"🏏 {team['team_name']} "
            f"— {team['owner_name']}"
        )

    # HOST
    if room["host_name"] == username:

        st.divider()

        st.subheader("👑 HOST CONTROLS")

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

    time.sleep(2)
    st.rerun()


# ============================================================
# FINISHED
# ============================================================

if room["status"] == "finished":

    st.title("🏆 AUCTION FINISHED!")

    teams = get_teams(room_code)

    for team in teams:

        squad = team["squad"] or []

        with st.expander(
            f"🏏 {team['team_name']} "
            f"— {len(squad)}/25 players "
            f"— ₹{team['purse']} Cr"
        ):

            if team["owner_name"]:
                st.write(
                    f"👤 Owner: {team['owner_name']}"
                )

            for player in squad:

                st.write(
                    f"• {player['name']} — "
                    f"{player['role']} — "
                    f"{player['country']}"
                )

    st.stop()


# ============================================================
# AUCTION SCREEN
# ============================================================

room = get_room(room_code)
teams = get_teams(room_code)

player = room["current_player"]

if not player:

    st.warning("Preparing player...")
    time.sleep(1)
    st.rerun()


player_name = player[0]
role = player[1]
base = player[2]
rating = player[3]
country = player[4]


st.title("🔥 LIVE IPL AUCTION")

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

    st.metric(
        "📦 Players Remaining",
        len(room["players"])
    )


st.divider()

st.header(f"🏏 {player_name}")

c1, c2 = st.columns(2)

with c1:

    st.write(f"**Role:** {role}")
    st.write(f"**Country:** {country}")
    st.write(f"**Base Price:** ₹{base} Cr")

with c2:

    st.metric(
        "⭐ Rating",
        f"{rating}/100"
    )


if room.get("message"):

    st.info(room["message"])


# ============================================================
# YOUR TEAM
# ============================================================

my_team = user_team(
    room_code,
    username
)

if my_team:

    squad = my_team["squad"] or []

    st.divider()

    st.subheader(
        f"🏏 YOUR TEAM — {my_team['team_name']}"
    )

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "💰 Purse",
            f"₹{my_team['purse']} Cr"
        )

    with b:
        st.metric(
            "👥 Squad",
            f"{len(squad)}/25"
        )

    with c:
        st.metric(
            "🌍 Overseas",
            f"{overseas_count(squad)}/8"
        )

    st.divider()

    if room["highest_bidder"] == my_team["team_name"]:

        st.success(
            "🔥 YOU ARE CURRENTLY WINNING!"
        )

        st.button(
            "💰 BID",
            disabled=True,
            use_container_width=True
        )

    else:

        allowed = can_buy(my_team, {
            "name": player_name,
            "role": role,
            "base": base,
            "rating": rating,
            "country": country
        })

        if st.button(
            "💰 BID",
            disabled=not allowed,
            use_container_width=True
        ):

            place_bid(
                room_code,
                username
            )

            st.rerun()

        if not allowed:

            st.warning(
                "You cannot bid: check purse, "
                "squad size or overseas limit."
            )

else:

    st.warning(
        "⚠️ You have not selected a team."
    )


# ============================================================
# HOST CONTROLS
# ============================================================

if room["host_name"] == username:

    st.divider()

    st.subheader("👑 HOST CONTROLS")

    if room["highest_bidder"]:

        st.write(
            f"Winning team: "
            f"**{room['highest_bidder']}**"
        )

        if st.button(
            "🔨 HAMMER — SELL PLAYER",
            use_container_width=True
        ):

            sell_player(room_code)

            st.rerun()

    else:

        if st.button(
            "❌ UNSOLD / NEXT PLAYER",
            use_container_width=True
        ):

            next_player(room_code)

            st.rerun()


# ============================================================
# LIVE TEAMS
# ============================================================

st.divider()

st.header("📊 LIVE TEAM STATUS")

for team in teams:

    squad = team["squad"] or []

    with st.expander(
        f"{team['team_name']} — "
        f"₹{team['purse']} Cr — "
        f"{len(squad)}/25"
    ):

        if team["owner_name"]:

            st.write(
                f"👤 Owner: {team['owner_name']}"
            )

        else:

            st.write("🟢 Available")

        st.write(
            f"🌍 Overseas: "
            f"{overseas_count(squad)}/8"
        )

        for p in squad:

            st.write(
                f"• {p['name']} — {p['role']}"
            )


# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(2)
st.rerun()
