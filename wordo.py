import streamlit as st
import streamlit_ext as ste
import random
import pytube
from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi
from annotated_text import annotated_text

from librosaplayground import slice_audio

st.title("Express Tube")
st.subheader("Find a Youtube video, grab its link, and enter it below!")
st.text("You can:\n- search the video by text\n- download the audio or video\n- listen/download audio")
yt_link = st.text_input("Please enter a Youtube link:")

if yt_link:
    with st.spinner("Working it...💃"):
        try:
            yt_video = pytube.YouTube(yt_link)
            yt_video_name = yt_video.title
            yt_audio_stream = yt_video.streams.get_by_itag(140).download()
            st.session_state.yt_audio = yt_audio_stream
            audio_download = open(f'{yt_audio_stream}', 'rb')
            audio_bytes = audio_download.read()
            with st.expander("Watch video | Listen/Download Audio"):
                with st.spinner("Fetching video:"):
                    st.video(yt_link)
                    st.audio(yt_audio_stream)
                    ste.download_button("Download audio", audio_bytes, f"{yt_video_name} - audio only.mp4")
            video_id = extract.video_id(yt_link)

            srt = YouTubeTranscriptApi.get_transcript(video_id)

            # st.write(srt)
            with st.expander("Search and chop audio by text"):
                search = st.text_input("Enter a word or phrase to search the video:")


                filtered_search = []

                for i in srt:
                    if search.lower() in i["text"].lower():
                        filtered_search.append(i)

                if search:
                    with st.spinner("Chop chop...✂︎✂︎✂︎"):
                        for i in filtered_search:
                            r = lambda: random.randint(150, 255)
                            g = lambda: random.randint(150, 255)
                            b = lambda: random.randint(136, 255)
                            randcolor = ("#%02X%02X%02X" % (r(), g(), b()))
                            annotated_tuple = (i["text"], str(i["start"]), randcolor)
                            annotated_text(annotated_tuple)
                            tab1, tab2 = st.tabs(["Listen/Download Audio", "Watch video from this point"])
                            sliced_audio = slice_audio(i["start"], i["duration"])
                            with tab1:
                                st_audio_thang = st.audio(sliced_audio.export().read())
                                ste.download_button("Download segment", sliced_audio.export(format='mp4').read(), f"{i['text']} - {i['start']}.mp4")
                            with tab2:
                                st.video(yt_link, start_time=int(i["start"]))

            with st.expander("SHOW ALL TEXT"):
                with st.spinner("All shall be revealed..."):
                    for i in srt:
                        r = lambda: random.randint(150, 255)
                        g = lambda: random.randint(150, 255)
                        b = lambda: random.randint(136, 255)
                        randcolor = ("#%02X%02X%02X" % (r(), g(), b()))
                        annotated_tuple = (i["text"], str(i["start"]), randcolor)
                        annotated_text(annotated_tuple)
        except:
            st.warning("Hmm...check the song has subtitles or that you have entered a valid Youtube link and try again! 🤔")

