import streamlit as st
import requests
import random
import string
import time
import json

# ============================================================
# IPL MULTIPLAYER AUCTION
# ============================================================

st.set_page_config(
    page_title="IPL Multiplayer Auction",
    page_icon="🏏",
    layout="wide"
)

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

RAW_PLAYERS = [
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
    ("Ishan Kishan", "Wicketkeeper", 4, 86, "India"),
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

def player_dict(p):
    return {
        "name": p[0],
        "role": p[1],
        "base": p[2],
        "rating": p[3],
        "country": p[4]
    }

# ============================================================
# SUPABASE CONNECTION
# ============================================================

try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    st.error("Supabase secrets are missing.")
    st.info("Go to Streamlit → App Settings → Secrets.")
    st.stop()

API_URL = SUPABASE_URL.rstrip("/") + "/rest/v1/auction_rooms"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": "Bearer " + SUPABASE_KEY,
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def get_room(room_code):
    try:
        response = requests.get(
            API_URL,
            headers=HEADERS,
            params={"room_code": f"eq.{room_code}"},
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if not data:
            return None

        return data[0]

    except Exception:
        return None


def create_room_in_db(room_code, host_name, state):
    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={
                "room_code": room_code,
                "host_name": host_name,
                "game_state": state
            },
            timeout=10
        )

        return response.status_code in [200, 201]

    except Exception:
        return False


def save_state(room_code, state):
    try:
        response = requests.patch(
            API_URL,
            headers=HEADERS,
            params={"room_code": f"eq.{room_code}"},
            json={
                "game_state": state,
                "updated_at": "now()"
            },
            timeout=10
        )

        return response.status_code in [200, 204]

    except Exception:
        return False


def new_room_code():
    chars = string.ascii_uppercase + string.digits

    for _ in range(100):
        code = "".join(random.choice(chars) for _ in range(5))

        if not get_room(code):
            return code

    return "".join(random.choice(chars) for _ in range(5))


# ============================================================
# GAME STATE
# ============================================================

def create_game_state():
    players = [player_dict(p) for p in RAW_PLAYERS]
    random.shuffle(players)

    teams = {}

    for team in TEAMS:
        teams[team] = {
            "owner": "",
            "purse": STARTING_PURSE,
            "squad": []
        }

    return {
        "status": "waiting",
        "players": players,
        "current_player": None,
        "current_bid": 0,
        "highest_bidder": "",
        "teams": teams,
        "message": "Waiting for players..."
    }


# ============================================================
# SESSION
# ============================================================

if "username" not in st.session_state:
    st.session_state.username = ""

if "room_code" not in st.session_state:
    st.session_state.room_code = ""

# ============================================================
# HOME
# ============================================================

if not st.session_state.room_code:

    st.title("🏏 IPL MULTIPLAYER AUCTION")

    st.markdown(
        "### ₹120 Cr Purse • 25 Player Squad • Maximum 8 Overseas"
    )

    username = st.text_input(
        "👤 Your name",
        placeholder="Enter your name"
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("🎮 Create Room")

        if st.button(
            "CREATE NEW ROOM",
            use_container_width=True
        ):

            if not username.strip():
                st.error("Enter your name first.")
            else:

                room_code = new_room_code()
                state = create_game_state()

                success = create_room_in_db(
                    room_code,
                    username.strip(),
                    state
                )

                if success:

                    st.session_state.username = username.strip()
                    st.session_state.room_code = room_code

                    st.rerun()

                else:
                    st.error(
                        "Could not create room. Check Supabase settings."
                    )

    with right:

        st.subheader("🚪 Join Room")

        room_code_input = st.text_input(
            "Room code",
            placeholder="Example: A7K2P"
        )

        if st.button(
            "JOIN ROOM",
            use_container_width=True
        ):

            if not username.strip():
                st.error("Enter your name first.")

            elif not room_code_input.strip():
                st.error("Enter the room code.")

            else:

                code = room_code_input.strip().upper()
                room = get_room(code)

                if not room:
                    st.error(
                        "❌ Room not found. Check the room code."
                    )
                else:

                    st.session_state.username = username.strip()
                    st.session_state.room_code = code

                    st.rerun()

    st.stop()

# ============================================================
# LOAD ROOM
# ============================================================

ROOM = get_room(st.session_state.room_code)

if not ROOM:

    st.error("❌ Room not found.")

    if st.button("Return Home"):
        st.session_state.room_code = ""
        st.session_state.username = ""
        st.rerun()

    st.stop()

room_code = st.session_state.room_code
username = st.session_state.username
state = ROOM["game_state"]

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🏏 IPL AUCTION")

    st.write("Room Code")

    st.code(room_code)

    st.write(
        f"👤 **{username}**"
    )

    st.divider()

    st.subheader("👥 Teams")

    for team in TEAMS:

        owner = state["teams"][team]["owner"]

        if owner:
            st.write(
                f"🔒 {team} — {owner}"
            )
        else:
            st.write(
                f"🟢 {team} — Available"
            )

    st.divider()

    if st.button("🚪 Leave Room"):

        st.session_state.room_code = ""
        st.session_state.username = ""

        st.rerun()

# ============================================================
# WAITING ROOM
# ============================================================

if state["status"] == "waiting":

    st.title("🎮 Waiting Room")

    st.success(
        f"ROOM CODE: **{room_code}**"
    )

    st.info(
        "Send the room code to your friends. "
        "They must open the same game link and enter this code."
    )

    st.divider()

    st.subheader("🏏 Select Your Team")

    my_team = None

    for team in TEAMS:

        if state["teams"][team]["owner"] == username:
            my_team = team

    if my_team:

        st.success(
            f"You control **{my_team}**"
        )

    else:

        available = [
            team for team in TEAMS
            if not state["teams"][team]["owner"]
        ]

        if available:

            selected = st.selectbox(
                "Choose a team",
                available
            )

            if st.button(
                "✅ JOIN SELECTED TEAM",
                use_container_width=True
            ):

                # Make sure the latest state is loaded
                latest = get_room(room_code)

                if latest:

                    latest_state = latest["game_state"]

                    if latest_state["teams"][selected]["owner"]:
                        st.error(
                            "❌ Someone already selected that team."
                        )
                    else:

                        # Prevent one person from owning two teams
                        already = False

                        for t in TEAMS:
                            if latest_state["teams"][t]["owner"] == username:
                                already = True

                        if already:
                            st.error(
                                "❌ You already selected a team."
                            )
                        else:

                            latest_state["teams"][selected]["owner"] = username

                            save_state(
                                room_code,
                                latest_state
                            )

                            st.success(
                                f"You joined {selected}!"
                            )

                            time.sleep(0.5)
                            st.rerun()

    st.divider()

    st.subheader("👥 Players")

    for team in TEAMS:

        owner = state["teams"][team]["owner"]

        if owner:
            st.write(
                f"🏏 **{team}** → {owner}"
            )

    # ========================================================
    # HOST
    # ========================================================

    if ROOM["host_name"] == username:

        st.divider()

        st.subheader("👑 HOST")

        joined = sum(
            1 for team in TEAMS
            if state["teams"][team]["owner"]
        )

        st.write(
            f"Teams joined: **{joined}/10**"
        )

        if joined >= 1:

            if st.button(
                "🚀 START AUCTION",
                use_container_width=True
            ):

                latest = get_room(room_code)

                if latest:

                    latest_state = latest["game_state"]

                    if latest_state["players"]:

                        player = latest_state["players"].pop(0)

                        latest_state["current_player"] = player
                        latest_state["current_bid"] = player["base"]
                        latest_state["highest_bidder"] = ""
                        latest_state["status"] = "auction"
                        latest_state["message"] = (
                            f"Auction started: {player['name']}"
                        )

                        save_state(
                            room_code,
                            latest_state
                        )

                        st.rerun()

    time.sleep(2)
    st.rerun()

# ============================================================
# FINISHED
# ============================================================

if state["status"] == "finished":

    st.title("🏆 AUCTION FINISHED!")

    for team in TEAMS:

        data = state["teams"][team]
        squad = data["squad"]

        with st.expander(
            f"🏏 {team} | ₹{data['purse']} Cr | "
            f"{len(squad)}/25 players"
        ):

            st.write(
                f"Owner: {data['owner'] or 'No player'}"
            )

            st.write(
                f"Overseas: "
                f"{sum(1 for p in squad if p['country'] != 'India')}/8"
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

player = state["current_player"]

if not player:

    st.warning("Preparing auction...")
    time.sleep(1)
    st.rerun()

st.title("🔥 LIVE AUCTION")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Current Bid",
        f"₹{state['current_bid']} Cr"
    )

with col2:
    st.metric(
        "👑 Highest Bidder",
        state["highest_bidder"] or "No bids"
    )

with col3:
    st.metric(
        "📦 Players Remaining",
        len(state["players"])
    )

st.divider()

# ============================================================
# CURRENT PLAYER
# ============================================================

st.header(f"🏏 {player['name']}")

a, b, c, d = st.columns(4)

with a:
    st.metric("Role", player["role"])

with b:
    st.metric("Country", player["country"])

with c:
    st.metric("⭐ Rating", player["rating"])

with d:
    st.metric(
        "💵 Base Price",
        f"₹{player['base']} Cr"
    )

if state["message"]:
    st.info(state["message"])

# ============================================================
# FIND USER TEAM
# ============================================================

my_team = None

for team in TEAMS:

    if state["teams"][team]["owner"] == username:
        my_team = team

# ============================================================
# BIDDING
# ============================================================

if my_team:

    team_data = state["teams"][my_team]
    squad = team_data["squad"]

    st.divider()

    x, y, z = st.columns(3)

    with x:
        st.metric(
            "💰 Your Purse",
            f"₹{team_data['purse']} Cr"
        )

    with y:
        st.metric(
            "👥 Squad",
            f"{len(squad)}/{MAX_SQUAD}"
        )

    with z:
        overseas = sum(
            1 for p in squad
            if p["country"] != "India"
        )

        st.metric(
            "🌍 Overseas",
            f"{overseas}/{MAX_OVERSEAS}"
        )

    overseas_limit = (
        player["country"] != "India"
        and overseas >= MAX_OVERSEAS
    )

    squad_limit = len(squad) >= MAX_SQUAD

    if state["current_bid"] < 5:
        increment = 1
    elif state["current_bid"] < 10:
        increment = 1
    else:
        increment = 2

    next_bid = state["current_bid"] + increment

    cannot_bid = (
        state["highest_bidder"] == my_team
        or team_data["purse"] < next_bid
        or overseas_limit
        or squad_limit
    )

    if state["highest_bidder"] == my_team:

        st.success(
            "🔥 YOU ARE CURRENTLY THE HIGHEST BIDDER!"
        )

    if st.button(
        f"💰 BID ₹{next_bid} Cr",
        disabled=cannot_bid,
        use_container_width=True
    ):

        latest = get_room(room_code)

        if latest:

            latest_state = latest["game_state"]

            latest_player = latest_state["current_player"]

            if latest_player and latest_player["name"] == player["name"]:

                latest_team = latest_state["teams"][my_team]

                if latest_state["current_bid"] < 5:
                    inc = 1
                elif latest_state["current_bid"] < 10:
                    inc = 1
                else:
                    inc = 2

                new_bid = latest_state["current_bid"] + inc

                if latest_team["purse"] >= new_bid:

                    latest_state["current_bid"] = new_bid
                    latest_state["highest_bidder"] = my_team
                    latest_state["message"] = (
                        f"🔥 {my_team} bids ₹{new_bid} Cr!"
                    )

                    save_state(
                        room_code,
                        latest_state
                    )

                    st.rerun()

else:

    st.warning(
        "You have not selected a team."
    )

# ============================================================
# HOST CONTROLS
# ============================================================

if ROOM["host_name"] == username:

    st.divider()

    st.header("👑 HOST CONTROLS")

    if state["highest_bidder"]:

        winner = state["highest_bidder"]

        st.write(
            f"Highest bidder: **{winner}**"
        )

        if st.button(
            "🔨 HAMMER — SELL PLAYER",
            use_container_width=True
        ):

            latest = get_room(room_code)

            if latest:

                s = latest["game_state"]

                winning_team = s["highest_bidder"]

                if winning_team:

                    team = s["teams"][winning_team]
                    sold_price = s["current_bid"]
                    sold_player = s["current_player"]

                    overseas = sum(
                        1 for p in team["squad"]
                        if p["country"] != "India"
                    )

                    if (
                        len(team["squad"]) < MAX_SQUAD
                        and team["purse"] >= sold_price
                        and (
                            sold_player["country"] == "India"
                            or overseas < MAX_OVERSEAS
                        )
                    ):

                        team["purse"] -= sold_price

                        team["squad"].append(
                            sold_player
                        )

                        if s["players"]:

                            next_p = s["players"].pop(0)

                            s["current_player"] = next_p
                            s["current_bid"] = next_p["base"]
                            s["highest_bidder"] = ""
                            s["message"] = (
                                f"🔨 SOLD! "
                                f"{sold_player['name']} → "
                                f"{winning_team} for "
                                f"₹{sold_price} Cr"
                            )

                        else:

                            s["current_player"] = None
                            s["status"] = "finished"
                            s["message"] = (
                                "🏆 AUCTION FINISHED!"
                            )

                        save_state(
                            room_code,
                            s
                        )

                        st.rerun()

    else:

        if st.button(
            "❌ UNSOLD / NEXT PLAYER",
            use_container_width=True
        ):

            latest = get_room(room_code)

            if latest:

                s = latest["game_state"]

                if s["players"]:

                    next_p = s["players"].pop(0)

                    s["current_player"] = next_p
                    s["current_bid"] = next_p["base"]
                    s["highest_bidder"] = ""
                    s["message"] = (
                        f"{s['current_player']['name']} is up for auction."
                    )

                else:

                    s["current_player"] = None
                    s["status"] = "finished"
                    s["message"] = "🏆 AUCTION FINISHED!"

                save_state(
                    room_code,
                    s
                )

                st.rerun()

# ============================================================
# LIVE TEAM STATUS
# ============================================================

st.divider()

st.header("📊 LIVE TEAM STATUS")

for team_name in TEAMS:

    team = state["teams"][team_name]
    squad = team["squad"]

    with st.expander(
        f"🏏 {team_name} | "
        f"₹{team['purse']} Cr | "
        f"{len(squad)}/25"
    ):

        st.write(
            f"Owner: {team['owner'] or 'Available'}"
        )

        overseas = sum(
            1 for p in squad
            if p["country"] != "India"
        )

        st.write(
            f"🌍 Overseas: {overseas}/8"
        )

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
