def img_interpreter(base64_image,model="gpt-4o-mini"):
    from openai import OpenAI
    from dotenv import load_dotenv
    from utils.check_cost import check_cost
    load_dotenv('.env')
    import os

    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    prompt='''Please summarize what is in this image. Please be extremely detailed and imagine to explain the entire content of each frame to a blind person. 
                Try to be as discoursive as possible and do not miss any detail of the picture.'''


    response = client.chat.completions.create(model=model, messages=[{ "role": "user","content": [{"type": "text", "text": prompt}, { "type": "image_url", "image_url": { "url": f"data:image/jpeg;base64,{base64_image}"}}]}],temperature=0, max_tokens=500)
    cost = check_cost(response, model)
    frame_description=str(response.choices[0].message.content)
    try: description = frame_description
    except: description = 'Error in interpreting this image'

    return description, cost