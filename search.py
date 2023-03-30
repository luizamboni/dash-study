def search_dicts(dicts, query):
    def check_start(value, word):
        return value.startswith(word)

    def check_end(value, word):
        return value.endswith(word)

    def check_contains(value, word):
        return word in value

    def process_query(query):
        parts = query.split(" ")
        conditions = []
        for part in parts:
            if "start:" in part:
                conditions.append(("start", part.replace("start:", "")))
            elif "end:" in part:
                conditions.append(("end", part.replace("end:", "")))
            elif "||" in part:
                conditions.append(("or",))
            elif "&&" in part:
                conditions.append(("and",))
            else:
                conditions.append(("contains", part))
        return conditions

    def check_item(item, conditions):
        or_conditions = []
        current_conditions = []
        for condition in conditions:
            if condition[0] == "or":
                or_conditions.append(current_conditions)
                current_conditions = []
            else:
                current_conditions.append(condition)
        or_conditions.append(current_conditions)

        for current_conditions in or_conditions:
            and_results = []
            for condition in current_conditions:
                if condition[0] == "start":
                    and_results.append(any(check_start(str(value), condition[1]) for value in item.values()))
                elif condition[0] == "end":
                    and_results.append(any(check_end(str(value), condition[1]) for value in item.values()))
                elif condition[0] == "contains":
                    and_results.append(any(check_contains(str(value), condition[1]) for value in item.values()))

            if all(and_results):
                return True

        return False

    conditions = process_query(query)
    return [item for item in dicts if check_item(item, conditions)]


# Exemplo de uso
data = [
    {"nome": "Fulano da Silva", "sobrenome": "Silva"},
    {"nome": "Beltrano dos Santos", "sobrenome": "Santos"},
    {"nome": "Ciclano de Oliveira", "sobrenome": "Oliveira"},
    {"nome": "Delano da Silva", "sobrenome": "Silva"},
    {"nome": "José", "profissão": "Engenheiro de Software"},
    {"nome": "Maria", "profissão": "Analista de Sistemas"},
]

# result1 = search_dicts(data, "start:Fulano")
# print(result1)

# result2 = search_dicts(data, "start:Delano || end:Software")
# print(result2)

# result3 = search_dicts(data, "start:Engenheiro && end:Sistemas")
# print(result3)

# result4 = search_dicts(data, "start:José || end:Silva")
# print(result4)


result5 = search_dicts(data, "de && end:Sistemas")
print(result5)