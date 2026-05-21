from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'campus_reservation_secret_key'

def get_db_connection():
    db_path = 'database.db'
    db_exists = os.path.exists(db_path)
    if not db_exists:
        from init_db import init_db
        init_db()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def require_login():
    allowed_routes = ['login', 'static']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM User WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='帳號或密碼錯誤')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/dashboard-stats')
def dashboard_stats():
    conn = get_db_connection()
    try:
        room_data = conn.execute('''
            SELECT r.name, COUNT(b.id) as count
            FROM Room r
            LEFT JOIN Booking b ON r.id = b.room_id AND b.status != 'cancelled'
            GROUP BY r.id
        ''').fetchall()
        
        equip_data = conn.execute('''
            SELECT e.name, COUNT(b.id) as count
            FROM Equipment e
            LEFT JOIN Booking b ON e.id = b.equipment_id AND b.status != 'cancelled'
            GROUP BY e.id
        ''').fetchall()

        stats = {
            'rooms': {
                'labels': [row['name'] for row in room_data],
                'data': [row['count'] for row in room_data]
            },
            'equipments': {
                'labels': [row['name'] for row in equip_data],
                'data': [row['count'] for row in equip_data]
            }
        }
        return jsonify(stats)
    finally:
        conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    
    query = '''
        SELECT b.id, u.username, r.name as room_name, e.name as equip_name, b.start_time, b.end_time, b.status, b.user_id 
        FROM Booking b
        JOIN User u ON b.user_id = u.id
        LEFT JOIN Room r ON b.room_id = r.id
        LEFT JOIN Equipment e ON b.equipment_id = e.id
    '''
    
    if session['role'] == 'student':
        query += ' WHERE b.user_id = ? ORDER BY b.start_time DESC LIMIT 15'
        recent_bookings = conn.execute(query, (session['user_id'],)).fetchall()
    else:
        query += ' ORDER BY b.start_time DESC LIMIT 15'
        recent_bookings = conn.execute(query).fetchall()
        
    conn.close()
    
    return render_template('index.html', bookings=recent_bookings)

@app.route('/book')
def book_page():
    conn = get_db_connection()
    rooms = conn.execute('SELECT * FROM Room').fetchall()
    equipments = conn.execute('SELECT * FROM Equipment').fetchall()
    conn.close()
    return render_template('book.html', rooms=rooms, equipments=equipments)

@app.route('/api/book', methods=['POST'])
def api_book():
    data = request.json
    user_id = session['user_id']
    room_id = data.get('room_id')
    equipment_id = data.get('equipment_id') or None
    date_str = data.get('date')
    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')

    if not all([room_id, date_str, start_time_str, end_time_str]):
        return jsonify({'error': '缺少必填欄位'}), 400

    if start_time_str >= end_time_str:
        return jsonify({'error': '結束時間必須晚於開始時間'}), 400

    start_dt_str = f"{date_str} {start_time_str}:00"
    end_dt_str = f"{date_str} {end_time_str}:00"

    conn = get_db_connection()
    try:
        room_conflict = conn.execute('''
            SELECT id FROM Booking 
            WHERE room_id = ? AND status != 'cancelled'
            AND start_time < ? AND end_time > ?
        ''', (room_id, end_dt_str, start_dt_str)).fetchone()

        if room_conflict:
            return jsonify({'error': '該空間在所選時段內已被預約，請選擇其他時間或空間。'}), 400

        if equipment_id:
            equip_conflict = conn.execute('''
                SELECT id FROM Booking 
                WHERE equipment_id = ? AND status != 'cancelled'
                AND start_time < ? AND end_time > ?
            ''', (equipment_id, end_dt_str, start_dt_str)).fetchone()

            if equip_conflict:
                return jsonify({'error': '該設備在所選時段內已被借走，請選擇其他設備或時間。'}), 400

        conn.execute('''
            INSERT INTO Booking (user_id, room_id, equipment_id, start_time, end_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, room_id, equipment_id, start_dt_str, end_dt_str))
        conn.commit()
        return jsonify({'message': '預約成功！'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/cancel-booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    conn = get_db_connection()
    try:
        booking = conn.execute('SELECT * FROM Booking WHERE id = ?', (booking_id,)).fetchone()
        if not booking:
            return jsonify({'error': '找不到該筆預約'}), 404
            
        if session['role'] != 'admin' and booking['user_id'] != session['user_id']:
            return jsonify({'error': '權限不足，無法取消他人的預約'}), 403
            
        conn.execute('UPDATE Booking SET status = "cancelled" WHERE id = ?', (booking_id,))
        conn.commit()
        return jsonify({'message': '預約已成功取消'})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
