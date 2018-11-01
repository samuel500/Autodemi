import secrets
from PIL import Image
import urllib.request, urllib.error, urllib.parse
import json
import base64
import os


def content_interactions_html_dict(interaction):
    if interaction:
        buttons_list = {'consuming': interaction.consuming, 'star': interaction.star, 'to_consume': interaction.to_consume, 'consumed': interaction.consumed, 'add_to_library': True}
    else:
        buttons_list = {'consuming': False, 'star': False, 'to_consume': False, 'consumed': False, 'add_to_library': False}
    for k in buttons_list:
        if buttons_list[k]:
            buttons_list[k] = "content-library-button-selected"
        else:
            buttons_list[k] = "content-library-button-unselected"
    return buttons_list


def process_url(url):

    url = url.replace('//m.', '//www.') # If mobile link

    if "https://www.youtube." in url and "watch?" in url:
        if "list=" in url:
            url = url.replace('watch', 'embed/', 1)
            url_parts = url.split('?')
            url_args = url_parts[1].split('&')
            url = url_parts[0]
            url += "videoseries?list=" + [x.replace('list=', '') for x in url_args if 'list=' in x][0]
            if "index=" in url_parts[1]:
                url += "&" + [str(int(x.replace('index=', ''))-1) for x in url_args if 'index=' in x][0]
        else:
            url = url.replace('watch?v=', 'embed/')

    return url


def screenshot_site(url, mobile=True):
    """
    Takes a screenshot of the website. Uses Google's API
    Might be useful to look into this in the future: https://github.com/DistilledLtd/heimdall
    """

    # The Google API.  Remove "&strategy=mobile" for a desktop screenshot
    mobile_arg = ''
    if mobile:
        mobile_arg = '&strategy=mobile'
    api = "https://www.googleapis.com/pagespeedonline/v1/runPagespeed?screenshot=true" + mobile_arg + "&url=" + urllib.parse.quote(url)
    file_name = 'content' + '_' + secrets.token_hex(12) + '.jpg'
    file_path = os.path.join(current_app.root_path, 'static/site_pics', file_name)
    unavailable_file_name = 'unavailable.jpg'

    # Get the results from Google
    try:
        site_data = json.load(urllib.request.urlopen(api))
    except urllib.error.URLError:
        print("Unable to retreive data")
        return unavailable_file_name

    try:
        screenshot_encoded =  site_data['screenshot']['data']
    except ValueError:
        print("Invalid JSON encountered.")
        return unavailable_file_name

    # Google has a weird way of encoding the Base64 data
    screenshot_encoded = screenshot_encoded.replace("_", "/")
    screenshot_encoded = screenshot_encoded.replace("-", "+")

    # Decode the Base64 data
    screenshot_decoded = base64.b64decode(screenshot_encoded)

    # Save the file
    with open(file_path, 'wb') as file_:
        file_.write(screenshot_decoded)

    return file_name
