def check_species_list(list_of_species):
    names = []
    for i in list_of_species:
        i = i.upper()
        i = i.replace(' ', '')
        names.append(i)
    return names
