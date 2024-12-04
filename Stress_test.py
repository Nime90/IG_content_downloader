try:
    import google.colab
    colab=1
    print("Running in Google Colab")
except ImportError:
    print("Not running in Google Colab")
    colab=0
if colab==0:
   from utils.download_content import download_content
   from utils.coach_ig_info import coach_ig_info
else: 
   from utils.download_content import download_content_gc as download_content
   from utils.coach_ig_info import coach_ig_info_gc as coach_ig_info

from utils.mp4_to_jpg import mp4_to_jpg
from utils.img_interpreter import img_interpreter
import os, shutil,base64
from datetime import datetime

# Get the current date
current_date = datetime.now().date()

#clean results

#specify the video url
coach_urls = ['https://www.instagram.com/emmafituk_/?hl=en',
              'https://www.instagram.com/fitwithyvannia/?hl=en',
              'https://www.instagram.com/jamiemiichele/?hl=en']

for coach_url in coach_urls:
  posts_info = coach_ig_info(coach_url.split('/')[-2])
  coach_handel = coach_url.split('/')[-2]
  url_list=[l for l in posts_info.perma_link]
  url_list = url_list[:5]
  print('urls captured')
  print(url_list)

  Full_coach_content = 'Coach: '+str(coach_handel)+'\n\n'

  #download in results folder
  for i,url in enumerate(url_list):
    #get the name of the downloaded files
    file_names = download_content(url, coach_handel)
    

  


