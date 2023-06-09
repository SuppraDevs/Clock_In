from threading import Timer
import connect as con
from clock import get_curr_time
from datetime import datetime
from functions import check_entrance, check_exit, format

# current_time = get_curr_time()
# # current_time = '2023-05-03 11:31:00'
# print(current_time)
# current_time_list = current_time.split(' ')
# # current_time_list = [0, "07:27:00"]


def db_commit(sql):
    for command in sql:
        con.cursor.execute(command)
        con.db.commit()


def read_element(rfID, element, table='students'):
    sql = f"SELECT {element} FROM {table} WHERE rfID = {rfID}"
    con.cursor.execute(sql)
    result = con.cursor.fetchall()
    return result[0][0]


def hit_point(rfID, current_time):
    # current_time = get_curr_time()
    # current_time = '2023-05-03 11:31:00'
    current_time_list = current_time.split(' ')
    # current_time_list = [0, "07:27:00"]

    presence = read_element(rfID, 'isPresent')

    if presence == 1:
        presence = 0
        create_exit(rfID, current_time_list, current_time)
    elif format(current_time_list[1]) >= format("07:25:00"):
        presence = 1
        create_entrance(rfID, current_time_list, current_time)

    sql = [f"UPDATE students SET isPresent = {presence} WHERE rfID = {rfID}"]
    db_commit(sql)
    return current_time, current_time_list      


# CALLED WHEN HIT
def create_entrance(rfID, current_time_list, current_time):
    presence, lateness = check_entrance(current_time_list[1])
    sql = [
        f"INSERT INTO entrance_table (timeEntrance, rfID) VALUES ('{current_time}', '{rfID}')",
        f"UPDATE students SET presenceStudent = {presence}, lateStudent = {lateness} WHERE rfID = {rfID}"
    ]
    db_commit(sql)

    def exit_closure():
        return hit_point(rfID)

    def timer():
        timer_variable = Timer(14400, exit_closure)
        timer_variable.start()
    
    # timer()


def create_exit(rfID, current_time_list, current_time):
    abscense = check_exit(current_time_list[1]) 
    presence = read_element(rfID, 'presenceStudent')

    new_presence = int(presence) - int(abscense) 
    new_abscence = 5 - int(new_presence)

    sql = [
        f"INSERT INTO exit_table (timeExit, rfID) VALUES ('{current_time}', '{rfID}')",
        f"UPDATE students SET presenceStudent = {new_presence}, absenceStudent = {new_abscence} WHERE rfID = {rfID}"

    ]
    db_commit(sql)
    update_gen_att(rfID)
    return current_time


def update_gen_att(rfID):
    old_presence_gn = read_element(rfID, 'presenceStudent', 'general_attendance')
    old_absence_gn = read_element(rfID, 'absenceStudent', 'general_attendance')
    old_late_gn = read_element(rfID, 'lateStudent', 'general_attendance')

    old_presence_st = read_element(rfID, 'presenceStudent')
    old_absence_st = read_element(rfID, 'absenceStudent')
    old_late_st = read_element(rfID, 'lateStudent')

    new_presence = int(old_presence_gn) + int(old_presence_st)
    new_absence = int(old_absence_gn) + int(old_absence_st)
    new_late = int(old_late_gn) + int(old_late_st)


    sql = [
        f"UPDATE general_attendance SET presenceStudent = {new_presence}, absenceStudent = {new_absence}, lateStudent = {new_late} WHERE rfID = {rfID}"
    ]
    db_commit(sql)
