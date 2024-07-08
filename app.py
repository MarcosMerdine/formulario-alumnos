from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATABASE = 'alumnos.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, nombre, apellido, email, edad FROM alumnos')
    alumnos = cur.fetchall()
    return render_template('index.html', alumnos=alumnos)

@app.route('/alumno', methods=['POST'])
def validar_alumno():
    dni = request.form['dni']
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM alumnos WHERE dni = ?', (dni,))
    alumno = cur.fetchone()
    if alumno:
        session['alumno_id'] = alumno['id']
        return redirect(url_for('alumno', alumno_id=alumno['id']))
    else:
        flash('DNI no encontrado')
        return redirect(url_for('index'))

@app.route('/alumno/<int:alumno_id>')
def alumno(alumno_id):
    if 'alumno_id' not in session or session['alumno_id'] != alumno_id:
        flash('Debe validar su DNI para acceder')
        return redirect(url_for('index'))
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM alumnos WHERE id = ?', (alumno_id,))
    alumno = cur.fetchone()
    
    cur.execute('SELECT * FROM materias WHERE alumno_id = ?', (alumno_id,))
    materias = cur.fetchall()
    
    return render_template('alumno.html', alumno=alumno, materias=materias)

@app.route('/agregar_alumno', methods=['POST'])
def agregar_alumno():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    dni = request.form['dni']
    email = request.form['email']
    edad = request.form['edad']
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO alumnos (nombre, apellido, dni, email, edad) VALUES (?, ?, ?, ?, ?)', (nombre, apellido, dni, email, edad))
    conn.commit()
    conn.close()
    
    flash('Alumno agregado con éxito')
    return redirect(url_for('index'))

@app.route('/editar_alumno/<int:alumno_id>', methods=['GET', 'POST'])
def editar_alumno(alumno_id):
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        edad = request.form['edad']
        
        cur.execute('''
            UPDATE alumnos
            SET nombre = ?, apellido = ?, email = ?, edad = ?
            WHERE id = ?
        ''', (nombre, apellido, email, edad, alumno_id))
        
        conn.commit()
        conn.close()
        
        flash('Datos del alumno actualizados con éxito')
        return redirect(url_for('alumno', alumno_id=alumno_id))
    else:
        cur.execute('SELECT * FROM alumnos WHERE id = ?', (alumno_id,))
        alumno = cur.fetchone()
        return render_template('editar_alumno.html', alumno=alumno)

@app.route('/eliminar_alumno/<int:alumno_id>', methods=['POST'])
def eliminar_alumno(alumno_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM alumnos WHERE id = ?', (alumno_id,))
    cur.execute('DELETE FROM materias WHERE alumno_id = ?', (alumno_id,))
    conn.commit()
    conn.close()
    
    flash('Alumno eliminado con éxito')
    return redirect(url_for('index'))

@app.route('/agregar_materia/<int:alumno_id>', methods=['POST'])
def agregar_materia(alumno_id):
    materia = request.form['materia']
    turno = request.form['turno']
    profesor = request.form['profesor']
    aula = request.form['aula']
    comision = request.form['comision']
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO materias (alumno_id, materia, turno, profesor, aula, comision)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (alumno_id, materia, turno, profesor, aula, comision))
    
    conn.commit()
    conn.close()
    
    flash('Materia agregada con éxito')
    return redirect(url_for('alumno', alumno_id=alumno_id))

@app.route('/editar_materia/<int:materia_id>', methods=['GET', 'POST'])
def editar_materia(materia_id):
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        materia = request.form['materia']
        turno = request.form['turno']
        profesor = request.form['profesor']
        aula = request.form['aula']
        comision = request.form['comision']
        
        cur.execute('''
            UPDATE materias
            SET materia = ?, turno = ?, profesor = ?, aula = ?, comision = ?
            WHERE id = ?
        ''', (materia, turno, profesor, aula, comision, materia_id))
        
        conn.commit()
        conn.close()
        
        flash('Materia actualizada con éxito')
        return redirect(url_for('alumno', alumno_id=request.form['alumno_id']))
    else:
        cur.execute('SELECT * FROM materias WHERE id = ?', (materia_id,))
        materia = cur.fetchone()
        return render_template('editar_materia.html', materia=materia)

@app.route('/eliminar_materia/<int:materia_id>', methods=['POST'])
def eliminar_materia(materia_id):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('SELECT alumno_id FROM materias WHERE id = ?', (materia_id,))
    alumno_id = cur.fetchone()['alumno_id']
    
    cur.execute('DELETE FROM materias WHERE id = ?', (materia_id,))
    conn.commit()
    conn.close()
    
    flash('Materia eliminada con éxito')
    return redirect(url_for('alumno', alumno_id=alumno_id))

if __name__ == '__main__':
    app.run(debug=True)
