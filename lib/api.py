from fastapi import FastAPI, File, UploadFile
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Try different TensorFlow Lite import approaches
try:
    # First try: TensorFlow Lite Runtime
    import tflite_runtime.interpreter as tflite
    interpreter = tflite.Interpreter(model_path="./assets/food_classifier_flex.tflite")
except ImportError:
    try:
        # Second try: Full TensorFlow
        import tensorflow as tf
        interpreter = tf.lite.Interpreter(model_path="./assets/food_classifier_flex.tflite")
    except ImportError:
        # Third try: Direct TensorFlow Lite import
        from tensorflow.lite.python.interpreter import Interpreter
        interpreter = Interpreter(model_path="./assets/food_classifier_flex.tflite")

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess_image(image_bytes):
    # Sesuaikan preprocessing dengan model Anda (resize, normalisasi, dsb)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))  # Contoh: resize ke 224x224
    img_array = np.array(image, dtype=np.float32)
    img_array = img_array / 255.0  # Contoh normalisasi
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    input_data = preprocess_image(image_bytes)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    prediction = np.argmax(output_data)
    confidence = float(np.max(output_data))
    return {"class": int(prediction), "confidence": confidence}

@app.get("/")
async def root():
    return {"message": "Food Classifier API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)