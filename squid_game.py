import streamlit as st
import time
import random

# ✅ Add Squid Game Easter Egg button
if 'game_started' not in st.session_state:
    st.session_state['game_started'] = False
    st.session_state['light'] = 'Green'
    st.session_state['click_time'] = None
    st.session_state['eliminated'] = False

# ✅ Easter Egg trigger button
if st.button("🔴🟢 Play Red Light, Green Light"):
    st.session_state['game_started'] = True

# ✅ Start the game
if st.session_state['game_started']:
    st.subheader("🔥 Red Light, Green Light Challenge!")

    # ✅ Randomize Red or Green light every 3-5 seconds
    if random.choice([True, False]):
        st.session_state['light'] = 'Green'
    else:
        st.session_state['light'] = 'Red'

    # ✅ Display the current light color
    if st.session_state['light'] == 'Green':
        st.success("🟢 Green Light – You can click!")
    else:
        st.error("🔴 Red Light – Don't click!")

    # ✅ Click button during the game
    if st.button("Click during Green Light!"):
        # ✅ If Red Light and clicked, ELIMINATED!
        if st.session_state['light'] == 'Red':
            st.session_state['eliminated'] = True
            st.error("🚫 You clicked during Red Light. Eliminated!")
            st.image("https://static.wikia.nocookie.net/squid-game/images/3/3c/Masked_soldier.png", 
                    width=200, caption="Game Over 😵")
        else:
            st.success("✅ You survived!")
            st.balloons()

    # ✅ Reset button
    if st.session_state['eliminated']:
        if st.button("Try Again"):
            st.session_state['game_started'] = False
            st.session_state['eliminated'] = False

