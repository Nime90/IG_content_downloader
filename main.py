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
from utils.assign_category import assign_category
from utils.coach_ig_info import coach_handles_all
from utils.mp4_to_jpg import mp4_to_jpg
from utils.img_interpreter import img_interpreter
import os, shutil,base64, json, pandas as pd
from datetime import datetime

#select the openaimodel to use
model = "gpt-4o"

# Get the current date
current_date = datetime.now().date()

#prepare overall summary Table
Coaches_overall_summary = pd.DataFrame()

#clean past results
if os.path.exists('results'): shutil.rmtree('results')

#collect all needed handle
coach_handles_all_l=coach_handles_all(market='Denmark')
#specify the video url
coach_urls = coach_urls = ['https://www.instagram.com/'+str(h)+'/?hl=en' for h in coach_handles_all_l.handle] #['https://www.instagram.com/emmafituk_/?hl=en', 'https://www.instagram.com/fitwithyvannia/?hl=en','https://www.instagram.com/jamiemiichele/?hl=en']

for coach_idx, coach_url in enumerate(coach_urls):
  posts_info = coach_ig_info(coach_url.split('/')[-2])
  coach_handel = coach_url.split('/')[-2]
  url_list=[l for l in posts_info.perma_link]
  #Getting last post from coach. Modify to adapt to the needs
  url_list = url_list[:1]
  print('urls captured')
  print(url_list)

  Full_coach_content = 'Coach: '+str(coach_handel)+'\n\n'

  #download in results folder
  for i,url in enumerate(url_list):
    #get the name of the downloaded files
    for _ in range(10):
      file_names = download_content(url, coach_handel)
      if len(file_names)>0:
         break
      
    print('file downloaded: ', file_names)
    #if i download a video i will split it into frames
    if len(file_names)>0: 
      if 'mp4' in file_names[0]:
        directory= mp4_to_jpg(file_names[0])
        #remove the video file
        os.remove(str(file_names[0]))

      #otherwise i will collect the downloads in a single folder
      else:
        directory=''
        for e,f in enumerate(file_names[0].split('/')):
            if e != len(file_names[0].split('/'))-1:
                directory=directory+f+'/'
        directory=directory[:-1]

      #transform the images in base64 to make it ready for openai
      images=[file for file in os.listdir(directory) if file.endswith(".jpg")]
      images_description = 'Summaries of the descriptions of the images in '+str(url.split('/')[-2])+' content:\n\n'
      #initiate cost computation
      Total_cost=0.0
      for y,ip in enumerate(images):
        image_path=directory+'/'+ip
        with open(image_path, "rb") as image_file: base64_string = base64.b64encode(image_file.read()).decode('utf-8')
        img_description,cost_img = img_interpreter(base64_string, model=model)
        print(f"Total estimated cost for img description: ${cost_img:.4f}")
        Total_cost = Total_cost + float(cost_img)
        images_description = images_description + 'Image_'+str(y)+ ':' +img_description+'\n\n'
        #delete the image
        os.remove(image_path)
    
    else:
       images_description = 'No SOME content downloaded on this coach.'

    info_txt = 'Caption: ' + posts_info.text[i] + '\n\nAdditional info at the '+str(current_date)+': Content Posted on ' + str(posts_info._date[i]) + ' - views: '+str(posts_info.lifetime_video_views[i])+ ' - reactions: '+str(posts_info.lifetime_reactions[i])+' - likes: '+str(posts_info.lifetime_likes[i])+ ' - shares: '+str(posts_info.lifetime_shares_count[i])+' - comments_count: '+str(posts_info.lifetime_comments_count[i])
    Full_coach_content = Full_coach_content + '\n\n' + images_description + '\n\n' + info_txt

    #finding content type
    category_assigned, cost_cat = assign_category(Full_coach_content,model=model)
    print(f"Total estimated cost for categorization: ${cost_cat:.4f}")
    category_assigned=category_assigned.replace("```json","").replace("```","")
    Total_cost = Total_cost + float(cost_cat)
    try:
      Content_type = json.loads(category_assigned)
      Full_coach_content = Full_coach_content + '\n\n' + 'Post Type:' +str(Content_type['Post Type'])+ '\n' + 'Post Type Accuracy:' +str(Content_type['Accuracy Post Type'])

      #adding results to the overall table
      table_t=pd.DataFrame(Content_type,index=[coach_idx])
      table_t['url'] = url
      table_t['Total_GPT_cost'] = Total_cost
      Coaches_overall_summary = pd.concat([Coaches_overall_summary ,table_t])
    except:
       print('error finding the category of ',url)
       Full_coach_content = Full_coach_content + '\n\n' + str(category_assigned )

    #saving checkpoint
    if colab == 0:
      with open('results/Full_info_on_'+str(coach_url.split('/')[-2])+".txt", "w") as file:
          file.write(Full_coach_content)
    else :
      with open('/content/results/Full_info_on_'+str(coach_url.split('/')[-2])+".txt", "w") as file:
          file.write(Full_coach_content)
    
    #clean results
    if os.path.exists(directory): shutil.rmtree(directory)

  #clean results
  coach_directory= os.getcwd()+'/results/'+str(coach_handel)
  if os.path.exists(coach_directory): shutil.rmtree(coach_directory)

#Saving overall results
if colab == 0: Coaches_overall_summary.to_excel('results/Coaches_overall_summary.xlsx',index=False)
else: Coaches_overall_summary.to_excel('/content/results/Coaches_overall_summary.xlsx',index=False)