from flask import Flask, request
import base64
# from PIL import Image


from jina import Flow, Document

def encode_image_to_base64(image_file):
    with open(image_file, "rb") as file:
        encoded_image = base64.b64encode(file.read())
        encoded_image = str(encoded_image)
        return encoded_image

app = Flask(__name__)

f = Flow.load_config("flows/flow.yml")
f.start()

@app.route("/query", methods=['POST'])
def query():
    uploaded_file = request.files['file'] if request.files.get('file') else None
    
    img_byte = uploaded_file.read()
    doc = Document(buffer=img_byte
    )
    
    
    match_images_b64 = []
    
    
    res = f.search(inputs = [doc], top_k=3, return_results=True)
    matches = res[0].docs[0].matches
    for m in matches:
        fname = m.tags["filename"]
        # match_images_b64.append(encode_image_to_base64(fname))
        match_images_b64.append(fname)
    return {
        "status": 200,
        "matches": match_images_b64
    }
    

# @app.route("/query_jina", methods=['POST'])
# def query_jina():
#     uploaded_file = request.files['file'] if request.files.get('file') else None
#     img_byte = uploaded_file.read()
#     doc = Document(buffer=img_byte
#     )
    
#     c = Client(port=40705)
#     c.post(on='/search', inputs=[doc], on_done=print)

if __name__=="__main__":
    app.run()


# curl -X POST http://127.0.0.1:5000/query   -H 'cache-control: no-cache'   -H 'content-type: multipart/form-data'  -F file=@test/test_full.jpeg
