from multiprocessing import Event
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from database.db import engine
from database.db import User
from database.db import Booking
from database.db import Object


class DataBase:
    def __init__(self):
        pass

    # создает новый объект (DONE)
    def insert_object(self, type, name, campus, floor, access=0):
        conn = engine.connect()
        ins = insert(Object).values(
            type=type,
            name=name,
            campus=campus,
            floor=floor,
            access=access
        )
        result = conn.execute(ins)

    # создает новую бронь (DONE)
    def insert_booking(self, tg_id, name, title, start_time, end_time, date):
        conn = engine.connect()
        sel = select(User.id).select_from(User).where(User.tg_id == tg_id)
        user_id = conn.execute(sel).first()[0]
        sel = select(Object.id).select_from(Object).where(Object.name == name)
        object_id = conn.execute(sel).first()[0]
        ins = insert(Booking).values(
            owner_id=user_id,
            id_obj=object_id,
            title=title,
            start_time=start_time,
            end_time=end_time,
            date=date
        )
        result = conn.execute(ins)

    # создает нового пользователя (role по умолчанию = 1) (DONE)
    def insert_user(self, tg_id, login, role=1):
        conn = engine.connect()
        ins = insert(User).values(
            role=role,
            login=login,
            tg_id=tg_id
        )
        result = conn.execute(ins)

    # возвращает список уникальных кампусов (DONE)
    def select_uniq_campus(self):
        conn = engine.connect()
        sel = select(Object.campus).select_from(Object).group_by(Object.campus)
        res = conn.execute(sel)
        return res

    # выдает уровень доступа юзера (DONE)
    def select_user_access(self, tg_id):
        conn = engine.connect()
        sel = select(User.role).select_from(
            User).where(User.tg_id == tg_id)
        res = conn.execute(sel)
        return res

    def select_login_by_tg_id(self, tg_id):
        conn = engine.connect()
        sel = select(User.login).select_from(User).where(User.tg_id == tg_id)
        res = conn.execute(sel)
        return res

    def select_user_bookingEntity(self, tg_id):
        conn = engine.connect()
        sel = select(User.id).select_from(User).where(User.tg_id == tg_id)
        res = conn.execute(sel)
        id_log = res.first()[0]
        sel = select(Object.name).where(
            Object.object_id.in_(
                select(Booking.id).where(Booking.owner_id == id_log)
            )
        )
        res = conn.execute(sel)
        return res

    def select_user_bookingName(self, tg_id):
        conn = engine.connect()
        sel = select(User.id).select_from(User).where(User.tg_id == tg_id)
        res = conn.execute(sel)
        id_log = res.first()[0]
        sel = select(Object.name).where(
            Object.id.in_(
                select(Booking.id_obj).where(Booking.owner_id == id_log)
            )
        )
        res = conn.execute(sel)

        return res

    # Возвращает доступные для пользователя типы объектов (DONE)
    def select_types_for_user(self, campus, tg_id):
        conn = engine.connect()
        sel = select(Object.type).select_from(Object).where(
                Object.access <= (
                    select(User.role).select_from(User).where(
                        User.tg_id == tg_id
                    )
                ), (
                    Object.campus == campus
                )
            ).group_by(Object.type)

        res = conn.execute(sel)
        return res

    def select_all_name_object(self):
        conn = engine.connect()
        sel = select(Object.name).select_from(Object).group_by(Object.name)
        res = conn.execute(sel)
        return res

    # Устанавливает роль по логину пользователя (DONE)

    def update_user_role(self, login, value):
        conn = engine.connect()
        upd = update(User).where(User.login == login).values(role=value)
        res = conn.execute(upd)
    # функция, изменяющая login пользователя

    def update_login(self, new_login, tg_id):
        conn = engine.connect()
        upd = update(User).where(User.tg_id == tg_id).values(login=new_login)
        res = conn.execute(upd)

        return res
    # возвращает ВСЕ брони по кампусу (DONE)

    def select_bookings(self, campus):
        conn = engine.connect()
        sel = select(Booking).filter(
            Booking.id_obj.in_(
                select(Object.id).select_from(Object).where(
                    Object.campus == campus
                )
            )
        )
        res = conn.execute(sel)

        return res

    # Возвращает списко стартов и концов броней по имени (DONE)
    def select_time_by_name(self, name):
        conn = engine.connect()
        sel = select(
            Booking.start_time,
            Booking.end_time,
            Booking.date
        ).select_from(Booking).filter(
            Booking.id_obj.in_(
                select(Object.id).where(
                    Object.name == name
                )
            )
        )
        res = conn.execute(sel)

        return res

    # функция получения всех start_time и end_time по id object и date
    def select_time_by_id_and_date(id, date):
        conn = engine.connect()
        sel = select(
            Booking.start_time,
            Booking.end_time
        ).where(
            Booking.id_obj == id,
            Booking.date == date
        )
        res = conn.execute(sel)

        return sel

    # функция получения всех Object по campus и type (Done)
    def select_objects_name(self, campus, type):
        conn = engine.connect()
        sel = select(Object.name).select_from(Object).where(
            Object.campus == campus,
            Object.type == type
        )
        res = conn.execute(sel)

        return res

    # type по campus и tg_id. Связь с User нужна
    # функция получения всех start_time и end_time по id object и date
