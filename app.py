import streamlit as st
import random
import time

# ============================================================
# IPL AUCTION GAME
# ============================================================

st.set_page_config(
    page_title="IPL Mega Auction",
    page_icon="🏏",
    layout="wide"
)

# ============================================================
# SETTINGS
# ============================================================

STARTING_PURSE = 120
MAX_SQUAD = 25
MAX_OVERSEAS = 8

# ============================================================
# TEAMS
# ============================================================

TEAMS = [
    "CSK",
    "MI",
    "RCB",
    "KKR",
    "SRH",
    "RR",
    "PBKS",
    "DC",
    "GT",
    "LSG"
]

# ============================================================
# PLAYER DATABASE
# name, role, base price, rating, nationality
# ============================================================

players = [

    # =========================
    # INDIAN BATSMEN
    # =========================

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
    ("Ishan Kishan", "Batsman", 4, 86, "India"),

    # =========================
    # WICKETKEEPERS
    # =========================

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

    # =========================
    # ALL ROUNDERS
    # =========================

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

    # =========================
    # INDIAN BOWLERS
    # =========================

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

    # =========================
    # OVERSEAS
    # =========================

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
    ("Marco Jansen", "All Rounder", 3, 87, "South Africa"),
    ("Trent Boult", "Bowler", 3, 89, "New Zealand"),
    ("Lockie Ferguson", "Bowler", 2, 83, "New Zealand"),
    ("Kagiso Rabada", "Bowler", 4, 91, "South Africa"),
    ("Anrich Nortje", "Bowler", 3, 87, "South Africa"),
    ("Adam Zampa", "Bowler", 2, 84, "Australia"),

    # =========================
    # CHEAP PLAYERS
    # =========================

    ("Arjun Tendulkar", "Bowler", 1, 72, "India"),
    ("Sameer Rizvi", "Batsman", 1, 75, "India"),
    ("Shaik Rasheed", "Batsman", 1, 73, "India"),
    ("Manav Suthar", "Bowler", 1, 72, "India"),
    ("Kumar Kushagra", "Wicketkeeper", 1, 74, "India"),
    ("Nehal Wadhera", "Batsman", 1, 78, "India"),
    ("Shahrukh Khan", "All Rounder", 1, 77, "India"),
    ("Naman Dhir", "All Rounder", 1, 76, "India"),
    ("Suyash Prabhakar", "Batsman", 1, 74, "India"),
    ("Angkrish Raghuvanshi", "Batsman", 1, 79, "India"),
    ("Harnoor Singh", "Batsman", 1, 72, "India"),
    ("Tanush Kotian", "All Rounder", 1, 76, "India"),
    ("Vijaykumar Vyshak", "Bowler", 1, 75, "India"),
]

# ============================================================
# CONVERT PLAYERS TO DICTIONARIES
# ============================================================

player_data = []

for p in players:
    player_data.append({
        "name": p[0],
        "role": p[1],
        "base": p[2],
        "rating": p[3],
        "country": p[4]
    })

# ============================================================
# SESSION STATE
# ============================================================

if "started" not in st.session_state:
    st.session_state.started = False

if "team" not in st.session_state:
    st.session_state.team = "CSK"

if "purse" not in st.session_state:
    st.session_state.purse = STARTING_PURSE

if "squad" not in st.session_state:
    st.session_state.squad = []

if "available" not in st.session_state:
    st.session_state.available = player_data.copy()
    random.shuffle(st.session_state.available)

if "current_player" not in st.session_state:
    st.session_state.current_player = None

if "current_bid" not in st.session_state:
    st.session_state.current_bid = 0

if "highest_bidder" not in st.session_state:
    st.session_state.highest_bidder = None

if "message" not in st.session_state:
    st.session_state.message = ""

if "auction_finished" not in st.session_state:
    st.session_state.auction_finished = False

# Computer team data

if "computer_teams" not in st.session_state:
    st.session_state.computer_teams = {}

    for team in TEAMS:
        if team != st.session_state.team:
            st.session_state.computer_teams[team] = {
                "purse": STARTING_PURSE,
                "squad": []
            }

# ============================================================
# FUNCTIONS
# ============================================================

def overseas_count(squad):
    return sum(1 for p in squad if p["country"] != "India")


def can_buy(team_squad, player):
    if len(team_squad) >= MAX_SQUAD:
        return False

    if player["country"] != "India":
        if overseas_count(team_squad) >= MAX_OVERSEAS:
            return False

    return True


def computer_bid(player):
    possible = []

    for team, data in st.session_state.computer_teams.items():

        if not can_buy(data["squad"], player):
            continue

        if data["purse"] < player["base"]:
            continue

        # Stronger players get more attention
        chance = player["rating"] - 60

        if random.randint(1, 100) <= chance:
            possible.append(team)

    if not possible:
        return None

    return random.choice(possible)


def reset_game():
    st.session_state.purse = STARTING_PURSE
    st.session_state.squad = []
    st.session_state.available = player_data.copy()
    random.shuffle(st.session_state.available)
    st.session_state.current_player = None
    st.session_state.current_bid = 0
    st.session_state.highest_bidder = None
    st.session_state.message = ""
    st.session_state.auction_finished = False

    for team in TEAMS:
        if team != st.session_state.team:
            st.session_state.computer_teams[team] = {
                "purse": STARTING_PURSE,
                "squad": []
            }


def next_player():
    if len(st.session_state.available) == 0:
        st.session_state.auction_finished = True
        return

    st.session_state.current_player = st.session_state.available.pop()
    st.session_state.current_bid = st.session_state.current_player["base"]
    st.session_state.highest_bidder = None
    st.session_state.message = ""


def user_bid():
    player = st.session_state.current_player

    if player is None:
        next_player()
        return

    if not can_buy(st.session_state.squad, player):
        st.session_state.message = "❌ You cannot buy this player."
        return

    if st.session_state.purse < st.session_state.current_bid:
        st.session_state.message = "❌ Not enough purse."
        return

    # Increase bid
    increment = 1

    st.session_state.current_bid += increment
    st.session_state.highest_bidder = st.session_state.team

    st.session_state.message = (
        f"🔥 {st.session_state.team} bids ₹"
        f"{st.session_state.current_bid} crore!"
    )

    # Computer response
    cpu = computer_bid(player)

    if cpu:

        cpu_data = st.session_state.computer_teams[cpu]

        if cpu_data["purse"] >= st.session_state.current_bid:

            st.session_state.current_bid += 1
            st.session_state.highest_bidder = cpu

            st.session_state.message += (
                f" 🤖 {cpu} bids ₹"
                f"{st.session_state.current_bid} crore!"
            )


def sell_player():

    player = st.session_state.current_player

    if player is None:
        return

    winner = st.session_state.highest_bidder

    # Nobody bid
    if winner is None:
        st.session_state.message = (
            f"❌ {player['name']} went UNSOLD."
        )
        next_player()
        return

    # User won
    if winner == st.session_state.team:

        if (
            st.session_state.current_bid <= st.session_state.purse
            and can_buy(st.session_state.squad, player)
        ):
            st.session_state.purse -= st.session_state.current_bid
            st.session_state.squad.append(player)

            st.session_state.message = (
                f"✅ {player['name']} sold to "
                f"{st.session_state.team} for "
                f"₹{st.session_state.current_bid} crore!"
            )

    else:

        data = st.session_state.computer_teams[winner]

        if (
            data["purse"] >= st.session_state.current_bid
            and can_buy(data["squad"], player)
        ):
            data["purse"] -= st.session_state.current_bid
            data["squad"].append(player)

            st.session_state.message = (
                f"🤖 {player['name']} sold to "
                f"{winner} for "
                f"₹{st.session_state.current_bid} crore!"
            )

    st.session_state.current_player = None
    st.session_state.current_bid = 0
    st.session_state.highest_bidder = None

# ============================================================
# TITLE
# ============================================================

st.title("🏏 IPL MEGA AUCTION")
st.caption("₹120 Crore Purse • 25 Player Squad • Maximum 8 Overseas")

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Game Settings")

    team_choice = st.selectbox(
        "Choose your team",
        TEAMS
    )

    if not st.session_state.started:

        st.session_state.team = team_choice

    st.divider()

    st.write("💰 Starting Purse")
    st.write("₹120 Crore")

    st.write("👥 Maximum Squad")
    st.write("25 Players")

    st.write("🌍 Overseas Limit")
    st.write("8 Players")

    if st.button("🔄 Reset Auction"):
        reset_game()
        st.rerun()

# ============================================================
# START
# ============================================================

if not st.session_state.started:

    st.info("Choose your team from the sidebar.")

    if st.button("🚀 START AUCTION", use_container_width=True):

        st.session_state.team = team_choice
        st.session_state.started = True
        next_player()
        st.rerun()

    st.stop()

# ============================================================
# TOP INFORMATION
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Purse",
        f"₹{st.session_state.purse} Cr"
    )

with col2:
    st.metric(
        "👥 Squad",
        f"{len(st.session_state.squad)}/{MAX_SQUAD}"
    )

with col3:
    st.metric(
        "🌍 Overseas",
        f"{overseas_count(st.session_state.squad)}/{MAX_OVERSEAS}"
    )

with col4:
    st.metric(
        "📦 Players Left",
        len(st.session_state.available)
    )

st.divider()

# ============================================================
# CURRENT PLAYER
# ============================================================

if st.session_state.auction_finished:

    st.success("🎉 AUCTION FINISHED!")

    st.header(f"🏆 {st.session_state.team} SQUAD")

    for i, player in enumerate(st.session_state.squad, 1):

        st.write(
            f"**{i}. {player['name']}** — "
            f"{player['role']} — "
            f"{player['country']}"
        )

    st.stop()

if st.session_state.current_player is None:

    if st.button(
        "➡️ NEXT PLAYER",
        use_container_width=True
    ):
        next_player()
        st.rerun()

else:

    player = st.session_state.current_player

    st.subheader("🔥 CURRENT PLAYER")

    c1, c2 = st.columns([2, 1])

    with c1:

        st.markdown(
            f"# 🏏 {player['name']}"
        )

        st.write(
            f"**Role:** {player['role']}"
        )

        st.write(
            f"**Country:** {player['country']}"
        )

        st.write(
            f"**Rating:** ⭐ {player['rating']}/100"
        )

        st.write(
            f"**Base Price:** ₹{player['base']} Crore"
        )

    with c2:

        st.metric(
            "🔥 Current Bid",
            f"₹{st.session_state.current_bid} Cr"
        )

        bidder = st.session_state.highest_bidder

        if bidder:
            st.write(
                f"Highest Bidder: **{bidder}**"
            )
        else:
            st.write("No bids yet")

    st.divider()

    # Buttons

    b1, b2, b3 = st.columns(3)

    with b1:

        if st.button(
            "💰 BID + ₹1 Cr",
            use_container_width=True
        ):

            user_bid()
            st.rerun()

    with b2:

        if st.button(
            "🔨 SELL PLAYER",
            use_container_width=True
        ):

            sell_player()
            st.rerun()

    with b3:

        if st.button(
            "❌ SKIP",
            use_container_width=True
        ):

            st.session_state.current_player = None
            st.session_state.current_bid = 0
            st.session_state.highest_bidder = None

            st.rerun()

    if st.session_state.message:

        st.info(st.session_state.message)

# ============================================================
# YOUR SQUAD
# ============================================================

st.divider()

st.header(f"🧢 {st.session_state.team} SQUAD")

if len(st.session_state.squad) == 0:

    st.write("No players bought yet.")

else:

    for i, player in enumerate(
        st.session_state.squad,
        1
    ):

        st.write(
            f"**{i}. {player['name']}** | "
            f"{player['role']} | "
            f"{player['country']}"
        )

# ============================================================
# COMPUTER TEAMS
# ============================================================

st.divider()

st.header("🤖 COMPUTER TEAMS")

for team, data in st.session_state.computer_teams.items():

    with st.expander(team):

        st.write(
            f"💰 Purse: ₹{data['purse']} Cr"
        )

        st.write(
            f"👥 Squad: {len(data['squad'])}/{MAX_SQUAD}"
        )

        st.write(
            f"🌍 Overseas: "
            f"{overseas_count(data['squad'])}/{MAX_OVERSEAS}"
        )

        if data["squad"]:

            for p in data["squad"]:

                st.write(
                    f"• {p['name']} "
                    f"({p['role']})"
                )