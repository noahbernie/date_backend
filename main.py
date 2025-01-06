# main.py
from flask import Flask
from app.services.services import get_image_path, get_image_results, filter_results

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the backend service!"

@app.route('/get-image-path', methods=['GET'])
def get_image_path_endpoint():
    """
    Flask endpoint to invoke the get_image_path function and return the result.
    """
    image_path = get_image_path()
    return f"Image Path or URL provided: {image_path}"

if __name__ == "__main__":
    print("Suuuuuiiiiiiii you losers")
    image_path = get_image_path()
    error, urls_images = get_image_results(image_path)
    print("Search Completed")

    # if urls_images:
    #     for im in urls_images:      # Iterate search results
    #         score = im['score']     # 0 to 100 score how well the face is matching found image
    #         url = im['url']         # url to webpage where the person was found
    #         image_base64 = im['base64']     # thumbnail image encoded as base64 string
    #         print(f"{score} {url} {image_base64[:32]}...")
    # else:
    #     print(error)

    instagram_usernames, linkedin_usernames, twitter_usernames, facebook_usernames = filter_results(urls_images)

    if instagram_usernames:
        print("Instagram")
        print(instagram_usernames)
    if linkedin_usernames:
        print("LinkedIn")
        print(linkedin_usernames)
    if facebook_usernames:
        print("Facebook")
        print(facebook_usernames)
    if twitter_usernames:
        print("Twitter")
        print(twitter_usernames)

    print("Thanks for trying this out BOI")

    print("Feel free to try again")
    

    # app.run(debug=True)
