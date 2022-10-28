from pydub import AudioSegment
import streamlit as st



def srtodub_time_converter(yt_time):
    yt_time_converted = yt_time * 1000
    return yt_time_converted


# yt_time = 188.02
# yt_duration = 2.069

def slice_audio(yt_time, yt_duration):
    audio = AudioSegment.from_file(f"{st.session_state.yt_audio}", "mp4")

    yt_duration_extra = yt_duration + 1

    yt_time_pydub = int(srtodub_time_converter(yt_time))
    # print(yt_time_pydub)
    duration_pydub = int(srtodub_time_converter(yt_duration_extra))

    end_time = yt_time_pydub + duration_pydub
    # print(end_time)

    sliced_audio = audio[yt_time_pydub:end_time]
    return sliced_audio
