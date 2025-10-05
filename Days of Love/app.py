import streamlit as st
from datetime import date
from PIL import Image
import base64

st.set_page_config(
    page_title="How Long Have We Loved?",
    page_icon="💖",
    layout="wide"
)

st.title("💖 How Long Have We Loved? 💖")
st.markdown("Enter the date your love story began, and we'll calculate your beautiful journey in days!")
st.markdown("---")

input_col, display_col = st.columns([1, 1])

with input_col:
    st.header("Your Love Story Details")
    loved_one_name = st.text_input(
        label="What's your loved one's name?",
        placeholder="e.g., Alex, Sofia, My Honey",
        max_chars=50,
        key="loved_one_name"
    )

    start_date = st.date_input(
        label="When did your love story begin?",
        value=date.today(), 
        max_value=date.today(),
        key="start_date"
    )

    calculate_button = st.button("Calculate Our Love Days!", key="calculate_button", type="primary")

with display_col:
    st.header("Your Love Milestone!")
    results_placeholder = st.empty()

if calculate_button:
    with results_placeholder.container(): 
        if not loved_one_name:
            st.error("Please enter your loved one's name!")
        elif start_date >= date.today():
            st.error("The start date must be in the past! 😉")
        else:
            today = date.today()
            time_difference = today - start_date
            total_days = time_difference.days
            
            try:
                years = today.year - start_date.year
                months = today.month - start_date.month
                if months < 0:
                    years -= 1
                    months += 12
            except:
                years = int(total_days / 365.25)
                months = None

            st.subheader(f"Congratulations, {loved_one_name}!")
            st.balloons() 

            main_message = f"We have been in love for {total_days:,} days!"
            
            styled_message = f"""
            <div style="background-color: #E74C3C; 
                        color: white; 
                        padding: 20px; 
                        border-radius: 10px; 
                        text-align: center; 
                        font-size: 24px; 
                        font-weight: bold; 
                        margin-bottom: 20px;">
                {main_message}
            </div>
            """
            st.markdown(styled_message, unsafe_allow_html=True)
            
            try:
                image_path = "cute_image.png"
                image = Image.open(image_path)
                st.image(image, caption=f"To more days with {loved_one_name} .") 
            except FileNotFoundError:
                st.warning("Cute image not found! Make sure 'cute_image.png' is in the project folder.")
                
            if months is not None:
                secondary_message = f"That's approximately {years} years and {months} months of beautiful moments together."
            else:
                secondary_message = f"That's approximately {years} years of beautiful moments together."
            
            st.markdown(f"**{secondary_message}**")
            
            st.markdown("---")
            st.info("Share this wonderful milestone with your loved one!")
            
            st.markdown("### Share the love!")

            
            text_to_copy = f"My love, we have been together for {total_days:,} days! ❤️ {loved_one_name}, {secondary_message}"
            
            st.components.v1.html(
                f"""
                <button 
                    onclick="navigator.clipboard.writeText('{text_to_copy.replace("'", "\\'").replace('"', '\\"')}')" 
                    style="background-color: #2ECC71; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin-right: 10px;"
                >
                    Copy Message
                </button>
                <script>
                    document.querySelector('button').onclick = function() {{
                        navigator.clipboard.writeText('{text_to_copy.replace("'", "\\'").replace('"', '\\"')}')
                        // Não colocamos o alert para não interromper o Streamlit, mas a função de copiar funciona
                    }};
                </script>
                """,
                height=50
            )

            try:
                with open(image_path, "rb") as file:
                    st.download_button(
                            label="Download Image",
                            data=file,
                            file_name=f"love_milestone_with_{loved_one_name.replace(' ', '_')}.png",
                            mime="image/png",
                            help="Download this cute image to share!",
                            key="download_btn"
                        )
            except NameError:
                 pass

st.markdown("---")
st.caption("Built with ❤️ using Streamlit and Python.")