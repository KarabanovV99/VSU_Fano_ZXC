from collections import Counter
from math import log2

print("Вводить текст(1), Вводить символ и вероятность(2)")
format = int(input("Ваш выбор: "))


def build_tuple_list():
    prob_list = []

    while True:
        user_input = input("Введите символ и вероятность: ")
        if not user_input:
            break

        try:
            char, probability = user_input.split()
            probability = int(probability)
            prob_list.append((char, probability))
        except ValueError:
            print("Ошибка ввода")

    # Сортируем список кортежей по убыванию значений второго элемента (вероятности)
    prob_list.sort(key=lambda x: x[1], reverse=True)

    return prob_list


if format == 1:
    input_text = input("Введите текст: ")
elif format == 2:
    input_text = build_tuple_list()


print("Полученный словарь:", input_text)

# input_text = input("Введите текст: ")
# input_text = "ааааббвввг"
# input_text = "абвг"
# input_text = "ИНН 637322757237"
n = 8  # 8 бит при равномерном кодировании


def count(txt: str, format: int) -> list:  # создание массива картежей, ключь - символ, значение - кольчество этого символа в тексте
    if format == 1:
        return Counter(txt).most_common()
    elif format == 2:
        return txt


def pi_dict(inp: list, input_text: str) -> dict:  # вычисление относительной вероятности символов
    j = {}
    for n, m in inp:
        Pi = m / len(input_text)
        j[n] = Pi
    return j


def h_entropy(inp: dict) -> float:  # вычисление энтропии
    entropy = 0
    for p in inp.values():
        entropy -= p * log2(p)
    return entropy


def redundancy_evenly(H: int, n: int) -> int:  # избыточность. H-энтропия, n-бит
    r = round(((1 - (H / n)) * 100), 2)
    return r


def shannon_fano_encoding(keys: list[str], values: list[float], code='') -> tuple:  # новый текст start
    i = sf_cut(values)
    pos_keys, pos_values, new_keys, new_values = keys[:i], values[:i], keys[i:], values[i:]
    '''Получаем на вход отдельно список ключей и список значений. Разделяем их (используем срез), получая
    в итоге 4 списка (2 из которых содержут просто ключи) с примерно одинаковой относительной вероятностью 
    появления символов.'''

    if len(pos_keys) == 1:
        if len(new_keys) == 1:
            return {pos_keys[0]: code + '0'}, {new_keys[0]: code + '1'}
        else:
            return {pos_keys[0]: code + '0'}, *shannon_fano_encoding(new_keys, new_values, code + '1')

    return (*shannon_fano_encoding(pos_keys, pos_values, code + '0'),
            *shannon_fano_encoding(new_keys, new_values, code + '1'))


def sf_cut(values: list[float]) -> int:
    con = [(sum(values[:i]), sum(values[i:])) for i in range(len(values))]
    a = min(con, key=lambda x: abs(x[0] - x[1]))
    '''Представляем суммы вероятностей всех срезов в виде кортежей (первый элемент - 0, второй - 1).
    Находит разницу вероятностей между 2-мя элементами каждого кортежа и берём минимальный'''

    current_summa = 0
    for i in range(len(values)):
        current_summa += values[i]
        if current_summa == a[0]:
            return i + 1


def encoding(pos: tuple[dict]) -> dict:  # Получаем из кортежа со словорями 1 единственный словарь
    j = {}
    for i in pos:
        j |= i  # Работает с python 3.9+
    return j


# end


def merge_dicts(dicts: list) -> dict:  # перевод массива картежей в словарь
    result = {}
    for d in dicts:
        result.update(d)
    return result


def trsnslate(input_text: str, dic: dict) -> str:  # соотношение входного текста со словарём(превод)
    r = ''.join(dic[i] for i in input_text)
    return r


result_count = count(input_text, format)  # функции со старым секстом
num_uniq_char = len(result_count)
result_Pi_dict = pi_dict(result_count, input_text)
result_H_entropy = h_entropy(result_Pi_dict)
result_redundancy_evenly = redundancy_evenly(result_H_entropy, n)


result_shannon_fano = shannon_fano_encoding(list(result_Pi_dict.keys()), list(result_Pi_dict.values()))
result_shannon_fano_encoding = encoding(result_shannon_fano)


if format == 1:
    result_translate = trsnslate(input_text, result_shannon_fano_encoding)


    n1 = len(result_translate) / len(input_text)  # функции с новым текстом
    result_count_new = count(result_translate, format)
    num_uniq_char_new = len(result_count_new)
    result_Pi_dict_new = pi_dict(result_count_new, result_translate)
    result_H_entropy_new = h_entropy(result_Pi_dict_new)
    result_redundancy_evenly_new = redundancy_evenly(result_H_entropy, n1)


    print("Результат перевода:", result_translate)
    print("Абсолютная частота символов в новом тексте:", result_count_new)
    print("Относительная частота символов:", result_Pi_dict_new)
    print("Энтропия в новом тексте:", result_H_entropy_new)
    print("Избыточность в новом тексте:", result_redundancy_evenly_new, "%")


print("Количество уникальных символов:", num_uniq_char)
print("Абсолютная частота символов:", result_count)
print("Относительная частота символов:", result_Pi_dict)
print("Энтропия:", result_H_entropy)
print("Избыточность:", result_redundancy_evenly, "%")


''' новый текст '''
print("Словать перевода в новый алфавит:", result_shannon_fano_encoding)
# print("Результат перевода:", result_translate)
# print("Абсолютная частота символов в новом тексте:", result_count_new)
# print("Относительная частота символов:", result_Pi_dict_new)
# print("Энтропия в новом тексте:", result_H_entropy_new)
# print("Избыточность в новом тексте:", result_redundancy_evenly_new, "%")
