import os
import tempfile
import streamlit as st
import soundfile as sf

# Import your package modules[cite: 1]
from betterdeclipper.engine import process_audio  # Update function name if different in engine.py[cite: 1]

st.set_page_config(page_title="BetterDeClipper", page_icon="🎵")

st.title("🎵 BetterDeClipper")
st.write("Upload a clipped or distorted audio file to restore missing signal peaks.")

uploaded_file = st.file_uploader("Select an audio file", type=["wav", "mp3", "flac", "ogg"])

if uploaded_file is not None:
    st.subheader("Original Audio")
    st.audio(uploaded_file)

    # Method selection or configuration options if applicable
    method = st.selectbox(
        "Declipping Method",
        ["janssen", "spade", "multires", "pnp", "social"]  # Based on betterdeclipper methods[cite: 1]
    )

    if st.button("Process Audio", type="primary"):
        with st.spinner("Declipping in progress..."):
            # Save uploaded file to a temporary location
            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
                tmp_in.write(uploaded_file.getbuffer())
                input_path = tmp_in.name

            output_path = input_path.replace(suffix, f"_cleaned.wav")

            try:
                # Call processing logic from betterdeclipper[cite: 1]
                # Adjust arguments to match your actual engine function signature
                process_audio(input_path, output_path, method=method)

                st.success("Processing complete!")
                st.subheader("Restored Audio")
                st.audio(output_path, format="audio/wav")

                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download Restored File",
                        data=file,
                        file_name=f"restored_{uploaded_file.name}",
                        mime="audio/wav"
                    )

            except Exception as e:
                st.error(f"Error processing audio: {e}")

            finally:
                # Clean up temporary local files
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)