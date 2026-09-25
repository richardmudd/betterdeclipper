import os
import sys
import tempfile
import streamlit as st
import soundfile as sf

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from betterdeclipper.engine import declip, PRESETS

st.set_page_config(page_title="BetterDeClipper", page_icon="🎵")

st.title("🎵 BetterDeClipper")
st.write("Upload a clipped or distorted audio file to restore missing signal peaks.")

uploaded_file = st.file_uploader("Select an audio file", type=["wav", "mp3", "flac", "ogg"])

if uploaded_file is not None:
    st.subheader("Original Audio")
    st.audio(uploaded_file)

    # Preset selection based on engine.py
    preset = st.selectbox(
        "Declipping Preset",
        options=list(PRESETS.keys()),
        index=1  # Default to "normal"
    )

    if st.button("Process Audio", type="primary"):
        with st.spinner("Declipping in progress..."):
            try:
                # Load audio array and sample rate directly
                y, sr = sf.read(uploaded_file)

                # Process using declip() from engine.py
                out_audio, info = declip(y, sr, preset=preset)

                # Save output to a temporary WAV file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_out:
                    sf.write(tmp_out.name, out_audio, sr)
                    output_path = tmp_out.name

                st.success(f"Processing complete in {info.get('time', 0):.2f} seconds!")
                st.subheader("Restored Audio")
                st.audio(output_path, format="audio/wav")

                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download Restored File",
                        data=file,
                        file_name=f"restored_{uploaded_file.name}.wav",
                        mime="audio/wav"
                    )

                os.remove(output_path)

            except Exception as e:
                st.error(f"Error processing audio: {e}")
