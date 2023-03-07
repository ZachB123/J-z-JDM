from database import db 
from cache import cache_db
import pytest


@pytest.mark.fast
def test_get_all_users():
    assert cache_db.get_all_users() == db.get_all_users()

@pytest.mark.fast
def test_get_user_by_id():
    assert cache_db.get_user_by_id((1,)) == cache_db.get_user_by_id((1,))

@pytest.mark.stress
def test_get_user_by_id_stress():
    for id in range(1, 100):
        assert cache_db.get_user_by_id((id,)) == db.get_user_by_id((id,))

@pytest.mark.fast
def test_get_user_by_username():
    assert cache_db.get_user_by_username(("ZachB123",)) == db.get_user_by_username(("ZachB123",))

@pytest.mark.stress
def test_get_user_by_username_stress():
    usernames = ["ZachB123", "test", "test2", "Lincoln Paulsen", "jWIZbigOLpackage",
                 "jdickens", "Dillon Croco", "MomB", "jb", "Mason Van Waning",
                 "Thomas Kerns", "Mohana Sunkara", "Karen Liu", "TriciaB", "Joe",
                 "flygirl", "nonexistent_user"]
    for username in usernames:
        assert cache_db.get_user_by_username((username,)) == db.get_user_by_username((username,))

@pytest.mark.fast
def test_get_all_cars():
    assert cache_db.get_all_cars() == db.get_all_cars()

@pytest.mark.fast
def test_get_car_by_id():
    assert cache_db.get_car_by_id(40) == db.get_car_by_id(40)
    assert cache_db.get_car_by_id(100) == db.get_car_by_id(100)

@pytest.mark.stress
def test_get_car_by_id_stress():
    for id in range(1,150):
        assert cache_db.get_car_by_id(id) == db.get_car_by_id(id)

@pytest.mark.fast
def test_get_images_from_car_id():
    assert cache_db.get_images_from_car_id(41) == db.get_images_from_car_id(41)

@pytest.mark.stress
def test_get_images_from_car_id_stress():
    for id in range(1,150):
        assert cache_db.get_images_from_car_id(id) == db.get_images_from_car_id(id)

@pytest.mark.fast
def test_paginate_cars():
    assert cache_db.paginate_cars((6,0)) == db.paginate_cars((6,0))

@pytest.mark.stress
def test_paginate_cars_stress():
    for cars in range(1,22):
        for offset in range(0,21):
            assert cache_db.paginate_cars((cars, offset)) == db.paginate_cars((cars, offset))

@pytest.mark.fast
def test_get_all_sales_rep():
    assert cache_db.get_all_sales_reps() == db.get_all_sales_reps()

@pytest.mark.fast
def test_get_sales_rep_by_user_id():
    assert cache_db.get_sales_rep_by_user_id((6)) == db.get_sales_rep_by_user_id((6))

@pytest.mark.stress
def test_get_sales_rep_by_user_id_stress():
    for id in range(1,50):
        assert cache_db.get_sales_rep_by_user_id((id)) == db.get_sales_rep_by_user_id((id))

@pytest.mark.fast
def test_get_cars_by_sales_rep_id():
    assert cache_db.get_cars_by_sales_rep_id((6)) == db.get_cars_by_sales_rep_id((6))

@pytest.mark.stress
def test_get_cars_by_sales_rep_id_stress():
    for id in range(1,50):
        assert cache_db.get_cars_by_sales_rep_id((id)) == db.get_cars_by_sales_rep_id((id))

@pytest.mark.fast
def test_get_sales_rep_by_user_id():
    assert cache_db.get_sales_rep_by_user_id((6)) == db.get_sales_rep_by_user_id((6))

@pytest.mark.stress
def test_get_sales_rep_by_user_id_stress():
    for id in range(1,50):
        assert cache_db.get_sales_rep_by_user_id((id)) == db.get_sales_rep_by_user_id((id))

@pytest.mark.fast
def test_is_car_favorited():
    assert cache_db.is_car_favorited((1,28)) == db.is_car_favorited((1,28))

@pytest.mark.stress
def test_is_car_favorited_stress():
    for user_id in range(1,20):
        for car_id in range(20,40):
            assert cache_db.is_car_favorited((user_id,car_id)) == db.is_car_favorited((user_id,car_id))

@pytest.mark.fast
def test_get_all_favorited():
    assert cache_db.get_all_favorited((1)) == cache_db.get_all_favorited((1))

@pytest.mark.stress
def test_get_all_favorited_stress():
    for id in range(1,50):
        assert cache_db.get_all_favorited((id)) == db.get_all_favorited((id))

@pytest.mark.fast
def test_get_messages():
    assert cache_db.get_messages((1,6)) == db.get_messages((1,6))

@pytest.mark.stress
def test_get_messages_stress():
    for sender_id in range(1,20):
        for recipient_id in range(1,20):
            assert cache_db.get_messages((sender_id,recipient_id)) == db.get_messages((sender_id,recipient_id))

@pytest.mark.fast
def test_direct_message_senders():
    assert sort_tuples(cache_db.direct_message_senders((6))) == sort_tuples(db.direct_message_senders((6)))

@pytest.mark.stress
def test_direct_message_senders_stress():
    for id in range(1,50):
        assert sort_tuples(cache_db.direct_message_senders((id))) == sort_tuples(db.direct_message_senders((id)))


def sort_tuples(lst):
    sorted_lst = sorted(lst, key=lambda x: x[0])
    return sorted_lst