import streamlit as st
from utils.download_content import download_content_gc as download_content
from utils.coach_ig_info import coach_ig_info_gc as coach_ig_info
from utils.mp4_to_jpg import mp4_to_jpg_gc as mp4_to_jpg
from utils.img_interpreter import img_interpreter
import zipfile
import os,shutil, base64

# Streamlit App Title
st.title("Instagram Content Downloader")

st.write("""
This application allows you to download multiple videos or carousel items from Instagram.
Enter the URLs and download all content as a single ZIP file.
""")

# User input for the video URL
url_p = st.text_input("Enter the Instagram profile link yo uwant to analyze:")

# Button to download the content
if st.button("Download"):
    try:
        #clean the old results if any
        if os.path.exists('results'): shutil.rmtree('results')
        
        # Call the download_content function
        #url_list = [line.strip() for line in url_p.splitlines() if line.strip()]#coach_urls_finder(url_p)
        posts_info = coach_ig_info(url_p.split('/')[-2])
        #url_list = [line.strip() for line in url_p.splitlines() if line.strip()]#coach_urls_finder(url_p)#coach_urls_finder(url_p)
        url_list=[l for l in posts_info.perma_link]
        url_list = url_list[:50]

        captions = []
        additional_info_lists = []
        for i,url in enumerate(url_list):
          #get the name of the downloaded files
          file_names = download_content(url)
          
          #if i download a video i will split it into frames
          if 'mp4' in file_names[0]:
            directory= mp4_to_jpg(file_names[0])
            #remove the video file
            os.remove('/content/results/'+str(file_names[0]))
          
          #otherwise i will collect the downloads in a single folder
          else:
            directory='/content/results/frames_'+file_names[0][:-6]
            if not os.path.exists(directory): os.makedirs(directory)
            for f in file_names:
              if f[-4:] == '.jpg': shutil.move('results/'+f, directory+'/'+f)

          #transform the images in base64 to make it ready for openai
          images=[file for file in os.listdir(directory) if file.endswith(".jpg")]
          images_description = 'Summaries of the descriptions of the images content:\n\n'
          for i,ip in enumerate(images):
            image_path=directory+'/'+ip
            with open(image_path, "rb") as image_file: base64_string = base64.b64encode(image_file.read()).decode('utf-8')
            img_description = img_interpreter(base64_string)
            images_description = images_description + 'Image_'+str(i)+ ':' +img_description+'\n\n'
            #delete the image
            os.remove(image_path)

          info_txt = 'Caption: ' + posts_info.text[i] + '\n\nAdditional info: ' + 'views: '+str(posts_info.lifetime_video_views[i])+ ' - reactions: '+str(posts_info.lifetime_reactions[i])+' - likes: '+str(posts_info.lifetime_likes[i])+ ' - shares: '+str(posts_info.lifetime_shares_count[i])+' - comments_count: '+str(posts_info.lifetime_comments_count[i])
          info_txt = images_description + '\n\n' + info_txt
          with open('/content/results/Full_info_on_'+str(url.split('/')[-2])+".txt", "w") as file: file.write(info_txt)
          
          #clean results
          print('deleting',directory)
          if os.path.exists(directory): shutil.rmtree(directory)
        
        # Create a ZIP file to bundle all downloaded files
        files_for_zip = [f for f in os.listdir('results') if os.path.isfile(os.path.join('results', f))]
        zip_path = "results/downloaded_files.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_name in files_for_zip:
                file_path = os.path.join("results", file_name)
                zipf.write(file_path, arcname=file_name)
        
        #check amount of downloads:
        if len(file_names) < 2: file_name_dwnld=file_names[0]
        else: file_name_dwnld="downloaded_files.zip"
        # Provide a single download button for the ZIP file
        with open(zip_path, "rb") as zip_file:
            st.download_button(
                label="Click here to download all files",
                data=zip_file,
                file_name=file_name_dwnld,
                mime="application/zip"
            )
        
        st.success("File(s) correctly downloaded and zipped!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

