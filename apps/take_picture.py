import streamlit as st
import cv2
from _deepface import DeepFace
import os

def app():
    #st.session_state["filename"] = ""
    name = st.text_input(label="Customer:",value='patrick')
    
    col_btn, col_video, col_analyse = st.columns([1, 2, 1])
    video_space= col_video.empty()
    btn_space = col_btn.container()
    analyse_space = col_analyse.container()
    
    btn_record = btn_space.button(label="Record", key= "btn_record")
    btn_photo = btn_space.button(label="Photo", key="btn_photo")
    btn_analyse = btn_space.button(label="Analyse", key="btn_analyse")
    btn_reset = btn_space.button(label="Reset", key="btn_reset")
    btn_recommed = btn_space.button(label="Recommendation", key="btn_recommand")
    
    if btn_record: 
        if st.session_state.get("__video", None): return
        
        if name.strip()=="": 
            st.error(body="Please set a customer name")
            return   
        video = cv2.VideoCapture(4)#0-4
        video.set(cv2.CAP_PROP_FPS, 25)
        if not video.isOpened(): 
            video_space.write("Unable to start video")
            return
        st.session_state["__video"] = video
        
        while True:
            succes, image = video.read()
            if not succes: 
                video_space.write("Unable to start video")
                break
            image = cv2.flip(image,1)
            video_space.image(image, channels="BGR", use_column_width='auto', clamp = True)
            st.session_state["__photo"] = image.copy()
        
    if btn_photo:
        if name.strip()=="": return
        kill_video()
        st.session_state["filename"] = save_photo(name=name.strip())        
        set_data(component_video=video_space, component_analyse=analyse_space)
        kill_photo()
        
    if btn_analyse:     
        set_data(component_video=video_space, component_analyse=analyse_space)
        ch_rep = analyse(path_image=st.session_state["filename"] , component=analyse_space)
        if ch_rep :
            st.error(body=ch_rep)
        else: st.success(f"Finished")
        
    if btn_reset:
        try:
            del st.session_state["__photo"]
            del st.session_state["filename"]
            video_space.empty()
            analyse_space.empty()
        except: return
        
    if btn_recommed:
        try:
            set_data(component_video=video_space, component_analyse=analyse_space)        
            affiche_analyse(component=analyse_space, analysis=st.session_state["analyse"])
            rg = recognition(path_img=st.session_state["filename"], dir_db="./image_client")
            affiche_recognition(recognition = rg,component=st)
        except: return
        
def save_photo(name):
    filename = f"./image_client/{name}.jpg"
    cv2.imwrite(filename, st.session_state["__photo"])
    return filename
    
    
def kill_video(key = "__video"):
    _video = st.session_state.get(key)
    if _video: 
        _video.release()
        cv2.destroyAllWindows()
        _video = None
        del st.session_state[key]       
    
        
def kill_photo(key = "__photo"):
    pass
    
def analyse(path_image, component=None):
    if not os.path.isfile(path=path_image): return f"File doesn't Exist. Retry later!!!"
    '''try:
        analysis = DeepFace.analyze(img_path = path_image, actions = ["age", "gender", "emotion", "race"])        
        st.session_state["analyse"] = analysis
        if component:
            affiche_analyse(component=component, analysis=analysis)
        else:
            return get_analyse(analysis=analysis)
        return ""
    except: return f"Face can't be detected"'''
    analysis = DeepFace.analyze(img_path = path_image, actions = ["age", "gender", "emotion", "race"], detector_backend='mtcnn')        
    st.session_state["analyse"] = analysis
    if component:
        affiche_analyse(component=component, analysis=analysis)
    else:
        return get_analyse(analysis=analysis)
    return ""
    

def affiche_analyse(component, analysis):    
    component.write(f"Age: {analysis['age']}")
    component.write(f"Gender: {analysis['gender']}")
    component.write(f"Emotion: {analysis['dominant_emotion']}")
    component.write(f"Race: {analysis['dominant_race']}")

def get_analyse(analysis):
    return {
        "Age": analysis['age'],
        "Gender": analysis['gender'],
        "Emotion": analysis['dominant_emotion'],
        "Race": analysis['dominant_race']
        }
    
    
def set_data(component_video, component_analyse):
    component_video.image(st.session_state["__photo"], channels="BGR", use_column_width='auto', clamp = True)
    
def recognition(path_img, dir_db):
    #os.remove(os.path.join(dir_db,"representations_vgg_face.pkl"))
    _recognition = DeepFace.find(img_path = path_img, db_path = dir_db, detector_backend="mtcnn") # mtcnn retinaface
    if _recognition.shape[0]>5: _recognition = _recognition.head(5)
          
    #st.write(_recognition)
    #print(_recognition)
    os.remove(os.path.join(dir_db,"representations_vgg_face.pkl"))   
    return _recognition
    
def affiche_recognition(recognition,component):    
    shape = recognition.shape
    for i in range(shape[0]):
        #print(recognition.iloc[i,1])
        col_photo, col_dist = component.columns([1,3])
        img = recognition.iloc[i,0]
        col_photo.image(img)        
        col_dist.write(recognition.iloc[i,1])
        col_dist.write(analyse(path_image=img))