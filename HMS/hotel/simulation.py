import random
import simpy
import numpy as np

def maid_simulation(num_rooms, num_maids, arrival_interval, cleaning_time):
    def guest_arrival(env, hotel, num_rooms, arrival_interval):
        for i in range(num_rooms):
            yield env.timeout(random.expovariate(1.0 / arrival_interval))
            env.process(guest_stay(env, hotel, i))

    def guest_stay(env, hotel, room_num):
        with hotel.request() as request:
            yield request
            yield env.timeout(random.expovariate(1.0 / cleaning_time))
            cleaning_schedule.append((room_num, round(env.now, 2)))

    def format_time(minutes):
        hours = int(minutes // 60)
        minutes = int(minutes % 60)
        formatted_time = f"{hours} ч {minutes} мин"
        return formatted_time

    cleaning_schedule = []
    env = simpy.Environment()
    hotel = simpy.Resource(env, capacity=num_maids)
    env.process(guest_arrival(env, hotel, num_rooms, arrival_interval))
    env.run()

    # Формирование строки вывода
    maid_simulation_output = "\n".join([f"Комната {room_num}: {format_time(time)};" for room_num, time in cleaning_schedule])

    return maid_simulation_output



def format_price(value):
    if value < 1000:
        formatted_value = f"{value} руб."
    else:
        formatted_value = f"{value:,.0f} руб"

    return formatted_value


def profit_simulation(num_rooms, price_per_room, cost_per_room, maid_wage, num_maids, arrival_interval, stay_duration):
    # Среднее количество прибытий в день
    arrivals_per_day = 24 / arrival_interval
    # Среднее количество занятых номеров в день
    occupied_rooms_per_day = arrivals_per_day * stay_duration

    # Ограничиваем количество занятых номеров числом доступных номеров
    if occupied_rooms_per_day > num_rooms:
        occupied_rooms_per_day = num_rooms

    # Расчет стоимости обслуживания всех номеров
    total_room_cost = num_rooms * cost_per_room

    # Расчет зарплаты для всех горничных
    total_maid_wage = num_maids * maid_wage

    # Вычисление фактора заполнения номеров
    occupancy_factor = occupied_rooms_per_day / num_rooms

    # Увеличиваем цену номера в зависимости от фактора занятости
    adjusted_price_per_room = price_per_room * (1 + occupancy_factor)

    # Расчет общей прибыли от занятых номеров
    daily_profit = occupied_rooms_per_day * adjusted_price_per_room

    # Вычитаем общие затраты (стоимость обслуживания номеров и зарплату горничных)
    net_daily_profit = daily_profit - (total_room_cost + total_maid_wage)

    formatted_daily_profit = format_price(net_daily_profit)

    return formatted_daily_profit