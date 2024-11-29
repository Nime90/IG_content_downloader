import streamlit as st
from utils.download_content import download_content_gc as download_content
import zipfile
import os,shutil

# Streamlit App Title
st.title("Instagram Content Downloader")

st.write("""
This application allows you to download multiple videos or carousel items from Instagram.
Enter the URLs and download all content as a single ZIP file.
""")

# User input for the video URL
urls = st.text_area("Enter Instagram URLs (one per line):")

# Button to download the content
if st.button("Download"):
    try:
        #clean the old results if any
        if os.path.exists('results'): shutil.rmtree('results')
        
        # Call the download_content function
        url_list = [url.strip() for url in urls.splitlines() if url.strip()]
        captions = []
        additional_info_lists = []
        for url in url_list:
            file_names, caption, additional_info_list = download_content(url)
            captions.append(caption)
            additional_info_lists.append(additional_info_list)
        
        for i,url in enumerate(url_list):
            st.write('Caption for',str(url.split('/'))[-2],': ',captions[i])
            st.write('Additional info for',str(url.split('/'))[-2],': ',additional_info_lists[i])
            
            info_txt='Caption for '+str(url.split('/')[-2])+': '+str(captions[i])+'\n\nAdditional info for '+str(url.split('/')[-2])+': '+str(additional_info_lists[i])
            with open('results/Additional_info_on_'+str(url.split('/')[-2])+".txt", "w") as file: file.write(info_txt)
        
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

