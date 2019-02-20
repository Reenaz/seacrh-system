import pymorphy2


base_pages_directory = "pages/"
lem_pages_directory = "lem_pages/"

morph = pymorphy2.MorphAnalyzer()

for i in range(100):
    page_file = open(base_pages_directory + "page" + str(i) + ".txt", "r")
    word_list = open(base_pages_directory + "page0.txt", "r").readlines()[0].split()
    page_file.close()

    lem_file = open(lem_pages_directory + "lem_page" + str(i) + ".txt", "w")

    for index, word in enumerate(word_list):
        word_list[index] = morph.parse(word)[0].normal_form

    lem_file.write("\n".join(word_list))
    lem_file.close()

