import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Function to generate recipe from OpenAI
def generate_recipe(ingredients):
    prompt = f"Create a recipe using the following ingredients: {ingredients}. Provide a detailed recipe with steps and ingredient quantities.End each line with |."

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    recipe = ""
    # Iterate through the response chunks as they are streamed
    for chunk in response:
        # Check if there is content in the chunk
            if chunk.choices[0].delta.content is not None:
                recipe += chunk.choices[0].delta.content
                recipe.strip()
                delimiter = "|"
                recipe.split(delimiter)
            
    # Return the generated recipe
    return recipe

# Home route
@app.route('/', methods=["GET", "POST"])

def home():
    if request.method == "POST":
        ingredients = request.form["ingredients"]
        if ingredients:
            recipe = generate_recipe(ingredients)
            return render_template("index2.html", recipe=recipe, ingredients=ingredients)
    return render_template("index2.html", recipe=None)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)