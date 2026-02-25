from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__, template_folder='.', static_folder='.')

API_BASE_URL = "http://localhost:5000/v1/users"

@app.route('/')
def inicio():
    try:
        response = requests.get(API_BASE_URL)
        if response.status_code == 200:
            data = response.json()
            lista_usuarios = data.get("data", [])
        else:
            lista_usuarios = []
    except:
        lista_usuarios = []
    return render_template('inicio.html', users=lista_usuarios)

@app.route('/agregar', methods=['POST'])
def agregar_usuario():
    try:
        nuevo_usuario = {
            "id": int(request.form['id']),
            "name": request.form['name'],
            "age": int(request.form['age']),
            "aka": request.form['aka']
        }
        requests.post(API_BASE_URL, json=nuevo_usuario)
    except:
        pass
    return redirect(url_for('inicio'))

@app.route('/borrar/<int:id>')
def borrar_usuario(id):
    try:
        requests.delete(f"{API_BASE_URL}/{id}")
    except:
        pass
    return redirect(url_for('inicio'))

@app.route('/editar/<int:id>')
def vista_editar(id):
    usuario_a_editar = None
    try:
        response = requests.get(f"http://localhost:5000/v1/user_optional/?id={id}")
        if response.status_code == 200:
            data = response.json()
            if "user" in data:
                usuario_a_editar = data["user"]
    except:
        pass
    return render_template('editar.html', user=usuario_a_editar)

@app.route('/actualizar', methods=['POST'])
def actualizar_usuario():
    try:
        id_usuario = int(request.form['id'])
        datos_actualizados = {
            "name": request.form['name'],
            "age": int(request.form['age']),
            "aka": request.form['aka']
        }
        requests.put(f"{API_BASE_URL}/{id_usuario}", json=datos_actualizados)
    except:
        pass
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)