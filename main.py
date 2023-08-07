import calendar
import csv
from collections import UserDict
from datetime import datetime
import pickle

class Field:
    pass


class Phone(Field):
    def __init__(self, phone: str):
        self.__value = None
        self.phone = phone

    @property
    def phone(self):
        return self.__value

    @phone.setter
    def phone(self, new_phone):
        if len(new_phone) == 10 and new_phone.isdigit():
            self.__value = new_phone
        else:
            raise ValueError("Incorrect phone number! It must contain exactly 10 numbers.")

    def __str__(self):
        return self.phone


class Name(Field):
    def __init__(self, name: str):
        self.__value = None
        self.name = name.capitalize()

    @property
    def name(self):
        return self.__value

    @name.setter
    def name(self, new_name):
        if new_name.isalpha():
            self.__value = new_name.capitalize()
        else:
            raise ValueError('Name can contain only letters!')


class Birthday(Field):
    def __init__(self, birthday: str):
        self.__value = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__value

    @birthday.setter
    def birthday(self, new_bday: str):
        try:
            bday = datetime.strptime(new_bday, '%d.%m.%Y')
        except ValueError:
            print('Wrong date format! Please provide correct form dd.mm.yyyy')
            quit()
        #Перевірка реальності дати
        if bday.date() > datetime.now().date() or bday.year <= datetime.now().year - 120:
            print('Unrealistic date! Provide the real one.')
            quit()
        else:
            self.__value = new_bday


class Record:
    def __init__(self, name: Name, *phone: Phone, birthday = None):
        if len(phone) == 0:
            phone = []
        self.name = name
        self.phones = list(phone)
        self.birthday = birthday

    #функція додавання телефону
    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    #функція вилучення телефону
    def remove_phone(self, phone: Phone):
        for ph in self.phones:
            if ph.phone == phone.phone:
                self.phones.remove(ph)

    #функція зміни телефону
    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if old_phone == phone.phone:
                phone.phone = new_phone

    #функіця, яка рахує кількість днів до наступного дня народження даного контакту
    def days_to_birthday(self) -> int:
        if self.birthday is not None:
            bday = self.birthday.birthday[:-4] + str(datetime.now().year)
            bday = datetime.strptime(bday, '%d.%m.%Y')
            now = datetime.now()
            result = bday.toordinal() - now.toordinal() #обчислення різниці днів між двома датами у поточному році
            if result < 0 and calendar.isleap(now.year):
                result += 366
            elif result < 0 and not calendar.isleap(now.year):
                result += 365
            return result

class AddressBook(UserDict):
    def __init__(self, N=1):
        super().__init__()
        self.N = N  # Кількість записів, які повертаються за одну ітерацію
    def list_contacts(self) -> dict:
        return self.data

    #до списку контактів додає об'єкт Record
    def add_record(self, record: Record):
        self.data.update({record.name.name.capitalize(): record})

    # повертає список об'єктів phone
    def get_contact(self, name: str) -> list:
        return self.data.get(name.capitalize()).phones

    # видаляє контакт
    def remove_contact(self, name: str):
        self.data.pop(name.capitalize())

    def __iter__(self, n = None):
        if n:
            self.N = n
        iter_list = list(self.data.items())
        grouped = [iter_list[n:n+self.N] for n in range(0, len(iter_list),self.N)]
        for group in grouped:
            yield group

    """"функція завантажує до вказаного файлу дані, 
        які знаходяться в об'єкті AddressBook на момент її виклику"""
    def load_to_disk(self, filename: str):
        with open(filename, 'ab') as fh:
            pickle.dump(self.data,fh)

    """"функція, яка зі вказаного файлу завантажує дані до об'єкту AddressBook"""
    def load_from_disk(self, filename: str):
            with open(filename, 'rb') as fh:
                self.data = pickle.load(fh)

    """"функція, яка повертає список записів у об'єкті AddressBook,
        номери яких, співпадають із поданим, як параметр, фрагментом номеру"""
    def search_by_number(self, number: str) -> list[Record]:
        return [record for record in self.data.values() for phone in record.phones if number in phone.phone]

    """"функція, яка повертає список записів у об'єкті AddressBook,
        імена яких, співпадають із поданим, як параметр, фрагментом імені"""
    def search_by_name(self, name: str) -> list[Record]:
        return [self.data[n] for n in self.data.keys() if name.upper() in n.upper()]

    """"функція, яка створює файл csv і записує туди, у відповідній формі,
        усі дані, які знаходяться у об'єкті AddressBook"""
    def create_csv_table(self, name_of_table: str):
        with open(name_of_table,'w', newline='') as fh:
            """"заголовки стовпців таблиці"""
            field_names = ['name', 'birthday', 'phones']
            csv.writer(fh).writerow(field_names)
            """"список словників, кожен з яких має ключі 'name', 'birthday' та 'phones'"""
            formatted_list = []
            for value in self.data.values():
                formatted_list.append({'name':value.name.name, 'birthday':value.birthday, 'phones': [value.phones[i].phone for i in range(len(value.phones))]})
            writer = csv.DictWriter(fh, fieldnames=field_names)
            writer.writerows(formatted_list)

    """"функція зчитує та повертає у вигляді списку словників дані з файлу з таблицею csv"""
    def read_from_csv_table(self, name_of_table: str):
        with open(name_of_table, newline='') as fh:
            reader = csv.DictReader(fh)
            return [row for row in reader]



if __name__ == "__main__":
    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name, phone)
    name = Name('Billq')
    phone = Phone('1234567891')
    rec1 = Record(name, phone)
    name = Name('Billw')
    phone = Phone('1234567892')
    rec2 = Record(name, phone)
    name = Name('Bille')
    phone = Phone('1234567893')
    rec3 = Record(name, phone)
    rec4 = Record(Name('Billr'), Phone('1234567894'))
    rec5 = Record(Name('Billt'),Phone('1234567895'),Phone('1234567896'),Phone('1234567896'), birthday='12.08.1998')
    ab = AddressBook()
    # ab.load_from_disk('disk.bin')
    ab.add_record(rec)
    ab.add_record(rec1)
    ab.add_record(rec2)
    ab.add_record(rec3)
    ab.add_record(rec4)
    ab.add_record(rec5)
    #ab.load_to_disk('disk.bin') #зразок виклику функції та назви файлу

    #приклад пошуку контакту за фрагментом номеру телефону
    print([ab.search_by_number('34')[i].name.name for i in range(len(ab.search_by_number('34')))])
    # приклад пошуку контакту за фрагментом імені
    print([ab.search_by_name('iLl')[i].name.name for i in range(len(ab.search_by_name('iLl')))])

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].phone == '1234567890'
    print('All Ok)')
    print(ab.list_contacts())
    ab.create_csv_table('contacts_table.csv')
    print(ab.read_from_csv_table('contacts_table.csv'))