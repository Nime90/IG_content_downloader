from utils.download_content import download_content
from utils.coach_urls_finder import coach_urls_finder
import os, shutil

#clean results
if os.path.exists('results'): shutil.rmtree('results')
#specify the video url
url_list=coach_urls_finder('https://www.instagram.com/emmafituk_/?hl=en')
print('urls captured')
print(url_list)
#download in results folder
captions = []
additional_info_lists = []
for url in url_list:
    file_names, caption, additional_info_list = download_content(url)
    captions.append(caption)
    additional_info_lists.append(additional_info_list)

#Show Results
for i,url in enumerate(url_list):
    info_txt='Caption for '+str(url.split('/')[-2])+': '+str(captions[i])+'\n\nAdditional info for '+str(url.split('/')[-2])+': '+str(additional_info_lists[i])
    with open('results/Additional_info_on_'+str(url.split('/')[-2])+".txt", "w") as file: file.write(info_txt)