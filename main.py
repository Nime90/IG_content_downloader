from utils.download_content import download_content
from utils.coach_ig_info import coach_ig_info
from utils.mp4_to_jpg import mp4_to_jpg
from utils.img_interpreter import img_interpreter
import os, shutil,base64
from datetime import datetime

# Get the current date
current_date = datetime.now().date()

#clean results
if os.path.exists('results'): shutil.rmtree('results')
#specify the video url
coach_urls = ['https://www.instagram.com/emmafituk_/?hl=en',
              'https://www.instagram.com/fitwithyvannia/?hl=en',
              'https://www.instagram.com/jamiemiichele/?hl=en']

for coach_url in coach_urls:
  posts_info = coach_ig_info(coach_url.split('/')[-2])

  url_list=[l for l in posts_info.perma_link]
  url_list = url_list[:5]
  print('urls captured')
  print(url_list)

  Full_coach_content = 'Coach: '+str(coach_url.split('/')[-2])+'\n\n'

  #download in results folder
  for i,url in enumerate(url_list):
    #get the name of the downloaded files
    file_names = download_content(url)
    
    #if i download a video i will split it into frames
    if 'mp4' in file_names[0]:
      directory= mp4_to_jpg(file_names[0])
      #remove the video file
      os.remove('results/'+str(file_names[0]))
    
    #otherwise i will collect the downloads in a single folder
    else:
      directory='results/frames_'+file_names[0][:-6]
      if not os.path.exists(directory): os.makedirs(directory)
      for f in file_names:
        if f[-4:] == '.jpg': shutil.move('results/'+f, directory+'/'+f)

    #transform the images in base64 to make it ready for openai
    images=[file for file in os.listdir(directory) if file.endswith(".jpg")]
    images_description = 'Summaries of the descriptions of the images in '+str(url.split('/')[-2])+' content:\n\n'
    for i,ip in enumerate(images):
      image_path=directory+'/'+ip
      with open(image_path, "rb") as image_file: base64_string = base64.b64encode(image_file.read()).decode('utf-8')
      img_description = img_interpreter(base64_string)
      images_description = images_description + 'Image_'+str(i)+ ':' +img_description+'\n\n'
      #delete the image
      os.remove(image_path)

    info_txt = 'Caption: ' + posts_info.text[i] + '\n\nAdditional info at the '+str(current_date)+': Content Posted on ' + str(posts_info._date[i]) + ' - views: '+str(posts_info.lifetime_video_views[i])+ ' - reactions: '+str(posts_info.lifetime_reactions[i])+' - likes: '+str(posts_info.lifetime_likes[i])+ ' - shares: '+str(posts_info.lifetime_shares_count[i])+' - comments_count: '+str(posts_info.lifetime_comments_count[i])
    Full_coach_content = Full_coach_content + '\n\n' + images_description + '\n\n' + info_txt
    
    #clean results
    print('deleting',directory)
    if os.path.exists(directory): shutil.rmtree(directory)

  with open('results/Full_info_on_'+str(coach_url.split('/')[-2])+".txt", "w") as file: file.write(Full_coach_content)
