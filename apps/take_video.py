import streamlit as st
import cv2

def app():
    name = st.text_input(label="Client:")
    
    col_btn, col_video = st.columns([1, 3])
    video_space= col_video.empty()
    btn_space = col_btn.container()
    
    btn_record = btn_space.button(label="Record", key= "btn_record")
    btn_stop = btn_space.button(label="stop", key="btn_stop")
    
    if btn_record:
        if name.strip()=="": return
        _name= name.strip()
        video = cv2.VideoCapture(0)
        video.set(cv2.CAP_PROP_FPS, 25)
        if not video.isOpened(): return
        st.session_state["_video"] = video
        
        # We need to set resolutions. so, convert them from float to integer.
        width= int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height= int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))        
        size = (width, height)
        #size = (640,480)
        writer= cv2.VideoWriter(f'./video_client/{_name}.mp4', cv2.VideoWriter_fourcc(*'FMP4'), 10.0, size)
        
        while True:
            succes, image = video.read()
            if not succes: break
            image = cv2.flip(image,1)
            video_space.image(image, channels="BGR", use_column_width='auto', clamp = True)
            writer.write(image)
    
    if btn_stop:
        kill_video()
    
def kill_video(key = "_video"):
    _video = st.session_state.get(key)
    if _video: 
        _video.release()
        cv2.destroyAllWindows()
        _video = None
        del st.session_state[key]