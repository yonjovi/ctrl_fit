import streamlit as st
import random
import pytube
from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi
from annotated_text import annotated_text

from librosaplayground import slice_audio

st.title("Express Tube")
st.subheader("Load a Youtube video, filter it by text, download samples, HAVE FUN")
yt_link = st.text_input("Please enter a Youtube link:")

if yt_link:
    video_id = extract.video_id(yt_link)

    srt = YouTubeTranscriptApi.get_transcript(video_id)

    # st.write(srt)

    search = st.text_input("Enter a word or phrase to search the video:")

    filtered_search = []

    for i in srt:
        if search.lower() in i["text"].lower():
            filtered_search.append(i)

    if search:
        with st.spinner("Chop chop..."):
            yt_audio = pytube.YouTube(yt_link).streams.filter(only_audio=True)
            # st.write(yt_audio)

            yt_video = pytube.YouTube(yt_link)
            yt_video_name = yt_video.title
            yt_audio_stream = yt_video.streams.get_by_itag(140).download()
            st.session_state.yt_audio = yt_audio_stream
            for i in filtered_search:
                r = lambda: random.randint(150, 255)
                g = lambda: random.randint(150, 255)
                b = lambda: random.randint(136, 255)
                randcolor = ("#%02X%02X%02X" % (r(), g(), b()))
                annotated_tuple = (i["text"], str(i["start"]), randcolor)
                annotated_text(annotated_tuple)
                watch_button = st.button(f'Watch: {i["text"]}')
                if watch_button:
                    st.video(yt_link, start_time=int(i["start"]))
                # st.write(type(i["duration"]))
                # st.write(st.session_state.yt_audio)
                # audio = AudioSegment.from_file(io.FileIO(yt_audio_stream), "mp4")
                sliced_audio = slice_audio(i["start"], i["duration"])
                # st.write(st.session_state.sliced_audio_file.file)
                # st.write(sliced_audio)
                # sliced_mp4 = sliced_audio.export(st.session_state["sliced_audio"], "mp4")
                st_audio_thang = st.audio(sliced_audio.export().read())

    show_all_button = st.button("Show all")
    if show_all_button:
        with st.spinner("All shall be revealed..."):
            for i in srt:
                r = lambda: random.randint(150, 255)
                g = lambda: random.randint(150, 255)
                b = lambda: random.randint(136, 255)
                randcolor = ("#%02X%02X%02X" % (r(), g(), b()))
                annotated_tuple = (i["text"], str(i["start"]), randcolor)
                annotated_text(annotated_tuple)

