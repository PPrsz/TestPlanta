import os
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
from google import genai
from dotenv import load_dotenv

# Carrega a chave de API segura do arquivo .env
load_dotenv()

print("A carregar o modelo SavedModel...")
# 1. Carregar o modelo no formato SavedModel (aponte para a pasta onde está o modelo)
# Se descompactou e a pasta chama-se 'saved_model', coloque o nome dela aqui:
model_path = "." # ou o nome da pasta correspondente
imported = tf.saved_model.load(model_path)
infer = imported.signatures["serving_default"]

# Carregar as labels
with open("labels.txt", "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

# 2. Definir a imagem da planta que você quer analisar
image_path = "plantas_1.jpg"  # Mude para o nome da foto que está na pasta

try:
    image = Image.open(image_path).convert("RGB")
except FileNotFoundError:
    print(f"Erro: A imagem '{image_path}' não foi encontrada na pasta.")
    exit()

# 3. Preparar a imagem para o Teachable Machine (224x224 pixels)
size = (224, 224)
image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
image_array = np.asarray(image_resized, dtype=np.float32)

# Normalizar os pixels de 0-255 para o intervalo de -1 a 1
normalized_image_array = (image_array / 127.5) - 1

# Criar o batch da imagem: formato [1, 224, 224, 3]
data = np.expand_dims(normalized_image_array, axis=0)

# Converter para tensor do TensorFlow
input_tensor = tf.convert_to_tensor(data)

# 4. Fazer a predição local com o SavedModel
print("A analisar a imagem com o modelo local...")
predictions = infer(input_tensor)

# Obter o array de probabilidades da primeira saída do modelo
output_key = list(predictions.keys())[0]
prediction_array = predictions[output_key].numpy()[0]

index = np.argmax(prediction_array)
classe_detectada = class_names[index]
confianca = prediction_array[index] * 100

print(f"-> O modelo local identificou: **{classe_detectada}** ({confianca:.2f}% de confiança)\n")

# 5. Acionar o Gemini para dar o diagnóstico detalhado e a cura
print("A consultar o Agrónomo Virtual (Gemini)...")
client = genai.Client()

prompt = f"""
Meu modelo de IA local identificou esta planta/folha com a seguinte classe: '{classe_detectada}' (com {confianca:.2f}% de confiança).
Atue como um agrónomo especialista e botânico experiente. Olhando para a imagem enviada junto, por favor:
1. Confirme ou ajuste o diagnóstico de forma detalhada.
2. Explique quais são as prováveis causas desse problema (se houver doença ou carência).
3. Dê um passo a passo prático de tratamento, cuidados e como fazer a cura ou recuperação da planta.
Responda de forma clara, organizada e didática em português.
"""

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[image, prompt]
)

# 6. Exibir o resultado final do especialista
print("\n" + "=" * 60)
print("🌿 RELATÓRIO DO AGRÓNOMO VIRTUAL (GEMINI)")
print("=" * 60)
print(response.text)
print("=" * 60)
