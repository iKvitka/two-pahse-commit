import psycopg2


def start(new_amount):
    fly_sql = "INSERT INTO fly_booking(client_name, fly_number, fly_from, fly_to, date) VALUES(%s,%s,%s,%s,%s);"
    hotel_sql = "INSERT INTO hotel_booking(client_name, hotel_name, arrival, departure) VALUES(%s,%s,%s,%s);"
    account_sql = "UPDATE account SET amount = %s WHERE client_name = %s"

    account_conn = psycopg2.connect(
        database="account",
        user="postgres",
        password="123",
        host="localhost",
        port=5433
    )
    fly_booking_conn = psycopg2.connect(
        database="fly_booking",
        user="postgres",
        password="123",
        host="localhost",
        port=5433
    )
    hotel_booking_conn = psycopg2.connect(
        database="hotel_booking",
        user="postgres",
        password="123",
        host="localhost",
        port=5433
    )

    account_xid = account_conn.xid(1, "lol", "kek")
    fly_booking_xid = fly_booking_conn.xid(2, "lol", "kek")
    hotel_booking_xid = hotel_booking_conn.xid(3, "lol", "kek")

    account_cur = account_conn.cursor()
    fly_booking_cur = fly_booking_conn.cursor()
    hotel_booking_cur = hotel_booking_conn.cursor()

    print("start two phase commit")
    account_conn.tpc_begin(account_xid)
    fly_booking_conn.tpc_begin(fly_booking_xid)
    hotel_booking_conn.tpc_begin(hotel_booking_xid)

    fly_booking_cur.execute(fly_sql, ('Oleh', 'SS1337', 'Berlin', 'Danzig(Gdańsk)', '1939-09-01'))
    hotel_booking_cur.execute(hotel_sql, ('Oleh', 'The Grand Budapest Hotel', '2021-01-28', '2021-01-31'))
    account_cur.execute(account_sql, (new_amount, 'Oleh'))

    try:
        account_conn.tpc_prepare()
        fly_booking_conn.tpc_prepare()
        hotel_booking_conn.tpc_prepare()
    except psycopg2.DatabaseError as error:
        print(error)
        account_conn.tpc_rollback()
        fly_booking_conn.tpc_rollback()
        hotel_booking_conn.tpc_rollback()
    else:
        # account_conn.tpc_commit()
        fly_booking_conn.tpc_commit()
        hotel_booking_conn.tpc_commit()
        print("this is fine!")

    account_cur.close()
    fly_booking_cur.close()
    hotel_booking_cur.close()

    account_conn.close()
    fly_booking_conn.close()
    hotel_booking_conn.close()
