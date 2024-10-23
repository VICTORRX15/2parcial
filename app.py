from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'


@app.route("/")
def gestion_productos():
    if 'productos' not in session:
        session['productos'] = [] 
    
    return render_template('index.html', productos=session['productos'])



@app.route("/agregar", methods=['POST'])
def agregar_producto():
    producto_id = request.form.get('producto_id')
    nombre = request.form.get('nombre')
    cantidad = request.form.get('cantidad')
    precio = request.form.get('precio')
    fecha_vencimiento = request.form.get('fecha_vencimiento')
    categoria = request.form.get('categoria')

    try:
        cantidad = int(cantidad)
        precio = float(precio)
    except ValueError:
        return redirect(url_for('gestion_productos'))

    productos = session['productos']

    if producto_id:  
        for producto in productos:
            if producto['id'] == int(producto_id):
                producto['nombre'] = nombre
                producto['cantidad'] = cantidad
                producto['precio'] = precio
                producto['fecha_vencimiento'] = fecha_vencimiento
                producto['categoria'] = categoria
                break
    else: 
        nuevo_id = len(productos) + 1 if productos else 1
        nuevo_producto = {
            'id': nuevo_id,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }
        productos.append(nuevo_producto)

    session.modified = True
    return redirect(url_for('gestion_productos'))



@app.route("/eliminar/<int:id>")
def eliminar_producto(id):
    if 'productos' in session:
        productos = session['productos']
        session['productos'] = [p for p in productos if p['id'] != id]
        session.modified = True

    return redirect(url_for('gestion_productos'))



@app.route("/editar/<int:id>")
def editar_producto(id):
    productos = session.get('productos', [])
    producto = next((p for p in productos if p['id'] == id), None)
    return render_template('editar.html', producto=producto)



@app.route("/vaciar")
def vaciar():
    session.pop('productos', None)
    return redirect(url_for('gestion_productos'))


if __name__ == "__main__":
    app.run(debug=True)
