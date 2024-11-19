import threading
import random
import time
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number  # Номер стола
        self.guest = None  # Гость за столом (по умолчанию None)

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name  # Имя гостя

    def run(self):
        # Гость ждет случайное время от 3 до 10 секунд
        wait_time = random.randint(3, 10)
        time.sleep(wait_time)

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()  # Очередь для гостей
        self.tables = tables  # Список столов

    def guest_arrival(self, *guests):
        for guest in guests:
            # Проверяем наличие свободного стола
            free_table = next((table for table in self.tables if table.guest is None), None)
            if free_table:
                free_table.guest = guest  # Садим гостя за стол
                guest.start()  # Запускаем поток гостя
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:
                self.queue.put(guest)  # Помещаем в очередь
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None:
                    if not table.guest.is_alive():  # Проверяем, закончил ли гость
                        print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                        print(f"Стол номер {table.number} свободен")
                        table.guest = None  # Освобождаем стол

                        # Проверяем очередь на наличие гостей
                        if not self.queue.empty():
                            next_guest = self.queue.get()  # Берем следующего из очереди
                            table.guest = next_guest  # Сажаем за стол
                            next_guest.start()  # Запускаем поток этого гостя
                            print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
            time.sleep(1)  # Задержка перед следующей проверкой

# Создание столов
tables = [Table(number) for number in range(1, 6)]

# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание гостей
guests = [Guest(name) for name in guests_names]

# Заполнение кафе столами
cafe = Cafe(*tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()