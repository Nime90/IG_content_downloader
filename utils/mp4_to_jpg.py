#saving one frame
def mp4_to_jpg(video_name = 'DDDEwC4pVWm_0.mp4'):
  from moviepy.editor import VideoFileClip
  import subprocess, os, shutil

  #clean old results
  directory="results/frames_"+video_name[:-6]
  if os.path.exists(directory): shutil.rmtree(directory)
  os.mkdir(directory)

  video_filename = 'results/'+video_name

  #compute video duration
  video = VideoFileClip(video_filename)
  duration = video.duration
  #compute the frames seconds based on the video length
  seconds = [f"00:00:{x:02}" for x in [round(1 + i * (duration - 1) / 5) for i in range(6)]]

  for x,second in enumerate(seconds):
      command = 'ffmpeg -y -ss '+str(second)+' -i  '+video_filename +' -frames:v 1 '+directory+'/frame_'+str(x)+'.jpg'
      subprocess.run(command, shell=True, executable="/bin/bash",stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
      
  return directory

def mp4_to_jpg_gc(video_name = 'DDDEwC4pVWm_0.mp4'):
  from moviepy.editor import VideoFileClip
  import subprocess, os, shutil

  #clean old results
  directory="results/frames_"+video_name[:-4]
  if os.path.exists(directory): shutil.rmtree(directory)
  os.mkdir(directory)

  video_filename = '/content/results/'+video_name

  #compute video duration
  video = VideoFileClip(video_filename)
  duration = video.duration
  #compute the frames seconds based on the video length
  seconds = [f"00:00:{x:02}" for x in [round(1 + i * (duration - 1) / 5) for i in range(6)]]

  for x,second in enumerate(seconds):
      command = 'ffmpeg -y -ss '+str(second)+' -i  '+video_filename +' -frames:v 1 '+directory+'/frame_'+str(x)+'.jpg'
      subprocess.run(command, shell=True, executable="/bin/bash",stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  return directory
  