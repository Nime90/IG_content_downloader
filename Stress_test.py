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
from utils.coach_ig_info import coach_handles_all
from datetime import datetime
import os, shutil

# Get the current date
current_date = datetime.now().date()

#clean results

#specify the video url
coach_handles_all_l=coach_handles_all()
coach_imported=['delilahrawfit','emmafituk_','fitbywh','jamiemiichele','jynfits','oj__fit','ownit.sweden','stephby._',]
coach_urls = ['https://www.instagram.com/'+str(h)+'/?hl=en' for h in coach_handles_all_l.handle if h not in coach_imported]

for coach_url in coach_urls:
  posts_info = coach_ig_info(coach_url.split('/')[-2])
  coach_handel = coach_url.split('/')[-2]
  url_list=[l for l in posts_info.perma_link]
  url_list = url_list[:10]
  print('urls captured')
  print(url_list)

  #download in results folder
  for i,url in enumerate(url_list):
    if 'instagram' in str(url):
      #get the name of the downloaded files
      try:
         file_names = download_content(url, coach_handel)
      except:
        print(url,'did not work')
  #clear results for the coach
  if os.path.exists('results/'+str(coach_handel)): shutil.rmtree('results/'+str(coach_handel))
        
      

  


