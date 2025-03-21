import streamlit as st
import streamlit.components.v1 as components
import cv2
import numpy as np
from PIL import Image
import pytesseract
from imutils.object_detection import non_max_suppression
from gcp_config import set_gcp_credentials
from utils.data_fetcher import fetch_nutritional_data
from utils.nutrition_calculator import calculate_daily_calories, calculate_bmi
from utils.ai_recommendation import get_ai_meal_recommendation
from utils.design import set_page_style
from openai import OpenAI

# ✅ Set page design
set_page_style()

# ✅ Set Google Cloud Vision credentials
set_gcp_credentials()

# ✅ Set OpenAI API key from secrets
client = OpenAI(api_key=st.secrets["openai_api_key"])

# ✅ Load the EAST text detection model
EAST_MODEL = "F:\\testing\\frozen_east_text_detection.pb"

# ✅ Display main title and subtitle
st.title("🥗 AI-Powered Personalized Nutrition and Meal Planning")
st.subheader("Get personalized dietary recommendations based on your details!")

# ✅ Easter egg trigger
name = st.text_input("Enter your name")

# 🔥 Easter Egg Trigger - Squid Game
if name.lower() == "redlightgreenlight":
    st.success("🔥 You unlocked the Squid Game Easter Egg!")

    # Embed the game as an iframe
    components.html(
        """
        <iframe srcdoc="
        <!DOCTYPE html>
        <html lang='en'>
        <head>
            <meta charset='UTF-8'>
            <title>Red Light, Green Light</title>
            <style>
                body { margin: 0; overflow: hidden; }
                canvas { display: block; background: #87CEEB; }
                #exit-btn {
                    position: fixed;
                    top: 10px;
                    left: 10px;
                    padding: 10px 20px;
                    font-size: 16px;
                    color: #fff;
                    background: #ff0000;
                    border: none;
                    cursor: pointer;
                    z-index: 10;
                }
            </style>
        </head>
        <body>
            <button id='exit-btn' onclick='window.location.reload()'>Exit</button>
            <canvas id='gameCanvas'></canvas>
            <script>
                const canvas = document.getElementById('gameCanvas');
                const ctx = canvas.getContext('2d');

                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;

                const player = { x: 100, y: canvas.height - 60, size: 40, speed: 5, dx: 0, dy: 0 };
                let gameOver = false;

                function drawPlayer() {
                    ctx.fillStyle = '#ff5733';
                    ctx.fillRect(player.x, player.y, player.size, player.size);
                }

                function updatePosition() {
                    player.x += player.dx;
                    player.y += player.dy;

                    if (player.x < 0) player.x = 0;
                    if (player.x + player.size > canvas.width) player.x = canvas.width - player.size;
                }

                function showMessage(message, color) {
                    ctx.fillStyle = color;
                    ctx.font = '40px Arial';
                    ctx.fillText(message, canvas.width / 2 - 150, canvas.height / 2);
                }

                function checkWin() {
                    if (player.x >= canvas.width - 100) {
                        showMessage('🏅 You Win!', 'green');
                        gameOver = true;
                    }
                }

                function checkLose() {
                    if (Math.random() < 0.01) {
                        showMessage('💀 You Lose!', 'red');
                        gameOver = true;
                    }
                }

                function animate() {
                    if (!gameOver) {
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        drawPlayer();
                        updatePosition();
                        checkWin();
                        checkLose();
                        requestAnimationFrame(animate);
                    }
                }

                window.addEventListener('keydown', (e) => {
                    if (e.key === 'ArrowRight') player.dx = player.speed;
                    if (e.key === 'ArrowLeft') player.dx = -player.speed;
                });

                window.addEventListener('keyup', () => {
                    player.dx = 0;
                });

                animate();
            </script>
        </body>
        </html>
        " width="100%" height="800px" style="border:none;"></iframe>
        """,
        height=800
    )

else:
    # ✅ Regular Nutrition App Interface
    age = st.number_input("Age", min_value=1, max_value=120)
    weight = st.number_input("Weight (kg)", min_value=1.0)
    height = st.number_input("Height (cm)", min_value=50.0)
    gender = st.radio("Gender", ('Male', 'Female'))
    diet_pref = st.selectbox("Diet Preference", ['None', 'Vegetarian', 'Non-Vegetarian'])

    # ✅ Calculate daily calorie needs and BMI
    if st.button("Calculate My Plan"):
        daily_calories = calculate_daily_calories(weight, height, age, gender)
        bmi = calculate_bmi(weight, height)

        st.write(f"🔥 Your daily intake needs to be: {daily_calories:.1f} calories")
        st.write(f"💪 Your BMI: {bmi:.2f} ({'Normal' if 18.5 <= bmi < 25 else 'Abnormal'})")

        # Fetch nutritional data
        nutritional_data = fetch_nutritional_data(diet_pref)

        # Display nutritional information
        st.subheader(f"🍎 Nutritional Recommendations ({diet_pref})")
        st.dataframe(nutritional_data)

        # Display AI meal plan
        meal_plan = get_ai_meal_recommendation(name, daily_calories, diet_pref)
        st.subheader("🥗 Your AI-Powered Meal Plan")
        st.write(meal_plan)

    # ✅ AI-Powered Chatbot
    st.subheader("🤖 Need More Help? Chat with our AI!")
    components.html(
        """
        <iframe
            src="https://www.chatbase.co/chatbot-iframe/e8ZOdBqJAJa0GTNJ06cIS"
            width="100%"
            style="height: 100%; min-height: 700px"
            frameborder="0"
        ></iframe>
        """,
        height=700
    )

    # ✅ OCR Ingredient Scanner with EAST Detection
    st.subheader("📷 Scan Ingredients with Your Camera")
    st.write("Click 'Capture' to scan the ingredient list")

    # ✅ Camera Section
    camera = st.camera_input("Take a picture")

    if camera:
        # Convert image to OpenCV format
        img = Image.open(camera)
        img_array = np.array(img)

        # Display the captured image
        st.image(img_array, caption="Captured Image", use_column_width=True)

        # Convert to OpenCV format for EAST detection
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        orig = img_cv.copy()
        (H, W) = img_cv.shape[:2]

        # Resize for EAST model
        (newW, newH) = (320, 320)
        rW = W / float(newW)
        rH = H / float(newH)
        img_resized = cv2.resize(img_cv, (newW, newH))

        # Load EAST model
        net = cv2.dnn.readNet(EAST_MODEL)

        # Prepare blob
        blob = cv2.dnn.blobFromImage(img_resized, 1.0, (newW, newH),
                                    (123.68, 116.78, 103.94), swapRB=True, crop=False)
        net.setInput(blob)
        (scores, geometry) = net.forward(["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"])

        # Text detection and OCR process
        extracted_text = pytesseract.image_to_string(img_cv, config='--psm 6').strip()

        if extracted_text:
            st.subheader("📝 Extracted Ingredients")
            st.write(extracted_text)
        else:
            st.warning("⚠️ No text detected. Please try again with clearer ingredients.")
