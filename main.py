from utils.download_content import download_content
from utils.coach_ig_info import coach_ig_info
import os, shutil

#clean results
if os.path.exists('results'): shutil.rmtree('results')
#specify the video url
coach_url = 'https://www.instagram.com/monetzamora_/?hl=en'
posts_info = coach_ig_info(coach_url.split('/')[-2])

url_list=[l for l in posts_info.perma_link]
url_list = url_list[:3]
print('urls captured')
print(url_list)
#download in results folder
captions = []
additional_info_lists = []
for i,url in enumerate(url_list):
    file_names = download_content(url)
    captions.append(posts_info.text[i])
    additional_info_lists.append(
      'video_views: '+str(posts_info.lifetime_video_views[i])+
      ' - reactions: '+str(posts_info.lifetime_reactions[i])+
      ' - likes: '+str(posts_info.lifetime_likes[i])+
      ' - shares: '+str(posts_info.lifetime_shares_count[i])+
      ' - comments_count: '+str(posts_info.lifetime_comments_count[i])
    )


#Show Results
for i,url in enumerate(url_list):
    info_txt='Caption for '+str(url.split('/')[-2])+': '+str(captions[i])+'\n\nAdditional info for '+str(url.split('/')[-2])+': '+str(additional_info_lists[i])
    with open('results/Additional_info_on_'+str(url.split('/')[-2])+".txt", "w") as file: file.write(info_txt)