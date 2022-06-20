from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value: str):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    # перевірка на вірність значень
    # критерії перевірки: телефон має складатись з 9 цифр
    @Field.value.setter
    def value(self, value):
        if value.isdigit() and len(value) == 9:
            self._value = value
        else:
            print('Wrong format of Phone, 9 digits needed')
            raise ValueError


class Birthday(Field):
    # перевірка на вірність значень
    # критерії перевірки: формат dd.mm.yyyy

    @Field.value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, '%m.%d.%Y').date()
            return True
        except ValueError:
            return False


class Record:
    # Ініціалізуємо запис, щоб в ній зберігалися обов'язковий параметр ім'я, необов'язковий телефон,
    # а також створюємо список з об'єктів - телефонів
    # а також, зберігання необов'язкового поля birthday та
    #  додаткову функцію, що рахує кількість днів до наступного дня народження

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone is not None:
            self.phones.append(phone)
        self.birthday = birthday

    # Фукція для додавання нового телефону для юзера
    def add_phone(self, ph: Phone):
        self.phones.append(ph)

    # Функція для зміни телефона на новий
    def change_phone(self, ph: Phone, new_ph: Phone):
        i = 0
        while i < len(self.phones):
            if self.phones[i] == ph:
                self.phones[i] = new_ph
                break
            else:
                i += 1

    # Функція, яка повертає кількість днів до наступного дня народження
    def days_to_birthday(self):
        if not self.birthday:
            return None

        now_day = datetime.now()

        bd_date = self.birthday.value
        bd_day, bd_month = bd_date.day, bd_date.month
        bd_this_year = datetime(day=bd_day, month=bd_month, year=now_day.year)
        bd_next_year = datetime(day=bd_day, month=bd_month, year=now_day.year + 1)
        if bd_this_year < now_day:
            delta = bd_next_year - now_day
        else:
            delta = bd_this_year - now_day
        return delta.days

    def __str__(self):
        str_of_phones = [ph.value for ph in self.phones]
        if self.birthday is not None:
            res = '{:<10}'.format(self.name.value) + ':' + ', '.join(str_of_phones) + f', Birthday is: {self.birthday.value} '
        else:
            res = '{:<10}'.format(self.name.value) + ':' + ', '.join(str_of_phones)

        return res


class AddressBook(UserDict):

    def add_record(self, rec: Record):
        k, i = rec.name.value, rec
        self.data[k] = i

    def iterator(self, rec_num=2):
        block = ''
        string_counter = 0
        for rec in self.data.values():
            string_counter += 1
            block += str(rec) + '\n'
            if string_counter == rec_num:
                block += '-' * 40 + '\n'
                yield block
                string_counter = 0
                block = ''
        yield block
