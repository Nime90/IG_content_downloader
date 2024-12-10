def assign_category(frames_description,model="gpt-4o-mini"):
    from openai import OpenAI
    from utils.check_cost import check_cost
    from dotenv import load_dotenv
    import os
    load_dotenv('.env')
    #post categories
    type_description = ''' 
    1. Entertainment: fits if the post seem to be mostly for entertainment purpose and is not directly selling anything nor giving useful tips or the like.
    2. About online coaching: fits if it describes what online coaching is, but is not outright trying to sell it.
    3. Promotion: is for a promotional content where the goal clearly is to try to sell or advertise a product (most likely online coaching or another type of programme).
    4. Educational/Tips: is for content that strives to teach about something be it nutrition, workouts, giving a recipe or other things, without focusing on selling something at the same time.
    5. Testimonials/Social Proof: is for a post that strives to show the effectiveness of something by showing or talking about an example of a person doing that thing - eg. transformation pictures, before and after weight or measurements or quotes from others about how well the thing worked for them.
    6. Mindset/Inspiration: is if the post focuses on one\’s mindset or strives to inspire.
    7. Brand/Personal is for content that is more specific to the sender whether it’s more personal content (eg. about the person writing the post, their friends or family, big events in their life) or very brand specific (eg. presenting an image for the brand, talking about their brand specifically).
    8. Other: is for a post that matches none of the categories listed.
    '''
    #Step5: analyze the video and assign a category
    prompt_video = "Given this definition of content types: " + type_description + '''Please evaluate this Social media content summary and fit it in only one type. 
    it is extremely important that you only answer in the following dictionary format. Do not add or subtract anything to your answer: 
    {
    "Date of evaluation": "[Additional info date]",
    "Post date": "[Content Posted date]",
    "Coach name": "[name of the coach]",
    "Content id": "[content identifier]",
    "Post Type": "[Post Type name]",
    "Accuracy Post Type": "[percentage of accuracy]",
    "Comments count": "[number of comments]",
    "Likes": "[number of Likes]",
    "Views": "[number of views]",
    "Reactions": "[number of reactions]",
    "Shares": "[number of shares]",
    "Content short description": "[short summary of the content and explanation of your decision]"
    }
    '''

    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    message='Content description: '+frames_description
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_video},  # Keep the text prompt as it is
                    {"type": "text", "text": message}  # Include any additional text instead of an image
                ]
            }
        ],
        temperature=0,
    )
    cost = check_cost(response, model)
    return response.choices[0].message.content, cost