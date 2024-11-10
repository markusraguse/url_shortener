from flask import Flask, request, redirect, jsonify
from marshmallow import ValidationError, Schema, fields 
from flasgger import Swagger
import random
import string

app = Flask(__name__)
swagger = Swagger(app)
short_to_long_url = {"abc":"https://google.com"}

HOST = "localhost"
PORT = "5000"


class ShortenURLSchema(Schema):
    url = fields.Url(required=True)
shorten_url_schema = ShortenURLSchema()

def generate_short_code(length=6):
    #Small possibility that two identical short codes will be generated. Can be fixed with a while loop
    short_url = ""
    for _ in range(length):
        short_url += random.choice(string.ascii_letters + string.digits)
    return short_url

@app.route('/shorten-url', methods=['POST'])
def shorten_url():
    """
    Shorten a long URL
    ---
    tags:
      - URL Shortener
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - url
          properties:
            url:
              type: string
              example: "http://very-long-url.com"
    responses:
      200:
        description: A shortened URL
        schema:
          type: object
          properties:
            url:
              type: string
              example: "http://very-long-url.com"
            short_url:
              type: string
              example: "http://localhost:5000/abc123"
    """
    data = request.get_json()
    try:
        validated_data = shorten_url_schema.load(data)
      
    except ValidationError as err:
      #Fails if missing URL, invalid URL format, extra fields beyond "url" 
      return jsonify(err.messages), 400

    original_url = validated_data['url']

    short_code = ""

    #To avoid having multiple short urls mapping to the same long url
    if original_url in short_to_long_url.values():
        #Finds the key corresponding to the value of "original_url" and assigns it to "short_code"
        short_code = list(short_to_long_url.keys())[list(short_to_long_url.values()).index(original_url)]
    else:
        short_code = generate_short_code()
        short_to_long_url[short_code] = original_url

    short_url = f"http://{HOST}:{PORT}/{short_code}"
    return jsonify({"url": original_url, "short_url": short_url})

@app.route('/urls', methods=['GET'])
def list_url_pairs():
    """
    Lists all pairs of urls
    ---
    tags:
      - URL Shortener
    responses:
      200:
        description: An object containing the pairs of short urls and urls
    """
    return jsonify(short_to_long_url)

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    """
    Redirect to the original URL
    ---
    tags:
      - URL Shortener
    parameters:
      - name: short_code
        in: path
        required: true
        type: string
        example: "abc123"
    responses:
      302:
        description: Redirects to the original URL
        headers:
          Location:
            description: The original URL
            type: string
      404:
        description: URL not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "URL not found"
    """
    print(short_to_long_url)
    print(short_code)
    original_url = short_to_long_url[short_code]

    if original_url:
        return redirect(original_url, code=302)
    else:
        return jsonify({"error": "URL not found"}), 404
    

if __name__ == '__main__':
    app.run(debug=True)