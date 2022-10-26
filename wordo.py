import streamlit as st
import random
from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi
from annotated_text import annotated_text

st.header("SUP")

yt_link = st.text_input("Please enter a Youtube link:")

if yt_link:
    video_id = extract.video_id(yt_link)

    srt = YouTubeTranscriptApi.get_transcript(video_id)

    # st.write(srt)

    search = st.text_input("Enter a word or phrase to search the video:")

    filtered_search = []

    for i in srt:
        if search in i["text"]:
            filtered_search.append(i)

    if search:
        for i in filtered_search:
            r = lambda: random.randint(0, 255)
            randcolor = ("#%02X%02X%02X" % (r(), r(), r()))
            annotated_tuple = (i["text"], str(i["start"]), randcolor)
            annotated_text(annotated_tuple)
            watch_button = st.button(i["text"])
            if watch_button:
                st.video(yt_link, start_time=int(i["start"]))

    show_all_button = st.button("Show all")
    if show_all_button:
        for i in srt:
            r_all = lambda: random.randint(0, 255)
            randcolor = ("#%02X%02X%02X" % (r_all(), r_all(), r_all()))
            annotated_tuple = (i["text"], str(i["start"]), randcolor)
            annotated_text(annotated_tuple)
