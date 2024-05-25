import requests
import pandas as pd
from bs4 import BeautifulSoup
#columns=['href ', 'name', 'salary', 'Company', 'Geography',
#                                            'Age_work'
#
#

def parse_hh_ru():
    df = pd.DataFrame(columns=['href', 'name', 'salary', 'company', 'geography', 'age_work'])
    df.to_excel('test.xlsx', index=False)
    for page in range(41): #Цикл от 1-й страницы до последней(В нашем случае 40-й)
        count = 1
        url = 'https://omsk.hh.ru/search/vacancy?hhtmFrom=main&hhtmFromLabel=vacancy_search_line&search_field=name&search_field=company_name&search_field=description&text=Python&enable_snippets=false&L_save_area=true&page=%d' % page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}#"Маска для HH.ru"
        r = requests.get(url, headers=headers)#Отправление запроса на сервак
        if r.status_code == 200:#Ответ, если получилось
            print("Сonnection Аccess")
            soup = BeautifulSoup(r.text, features="html.parser")
            with open('test.html', 'w', encoding="utf-8") as output_file:
                output_file.write(str(soup))

                # Открытие файла с HTML-кодом
            with open('test.html', 'r', encoding='utf-8') as file:
                html_content = file.read()

                # Инициализация BeautifulSoup с содержимым файла
            soup = BeautifulSoup(html_content, 'html.parser')
            vacancies = soup.find_all('div', class_='vacancy-card--H8LvOiOGPll0jZvYpxIF font-inter')
            for vacancy in vacancies:
                href = ((vacancy.find('a', {'class': 'bloko-link'}))['href'])#Ссылка на вакансию
                age_work =  (((vacancy.find('span', {'class': 'label--rWRLMsbliNlu_OMkM_D3 label_light-gray--naceJW1Byb6XTGCkZtUM','data-qa':'vacancy-serp__vacancy-work-experience'})).text).replace("\xa0", ""))#Опыт работы
                geography =  ((vacancy.find('span', {'class': 'fake-magritte-primary-text--qmdoVdtVX3UWtBb3Q7Qj'})).text).replace("\xa0", "")#Где находится
                company =  ((vacancy.find('span', {'class':'company-info-text--O32pGCRW0YDmp3BHuNOP'})).text).replace("\xa0", "")# Работодатель
                name =  vacancy.find('span', {'data-qa': 'serp-item__title'}).text.replace("\xa0", "")#Кем работать
                salary = vacancy.find('span',{'data-qa':'vacancy-serp__vacancy-compensation'})#Поиск зп
                salary_text = (salary.text if salary else 'Зарплата не указана').replace("\xa0", "")#преобразование данных в ЗП
                # print(f'Ссылка: {href}, Профессия: {name},Зарплата: {salary_text},Географическое положение: {Geography},Опыт работы: {Age_work},Работодатель: {Company} ')
                #,[name],[salary_text],[company],[geography],[age_work]
                data = {
                    'href': [href],
                    'name': [name],
                    'salary': [salary_text],
                    'company': [company],
                    'geography': [geography],
                    'age_work': [age_work]
                }
                df = df._append(pd.DataFrame(data,columns=['href', 'name', 'salary', 'company', 'geography', 'age_work']),ignore_index=True)
            print(df)
            df.to_excel('test.xlsx', index=False)

            # # Заданные вами теги
            # tags = ['h1', 'p', 'a']
            #
            # # Проходим по каждому тегу из списка и извлекаем информацию
            # for tag_name in tags:
            #     # Находим все теги с указанным именем
            #     tag_elements = soup.find_all(tag_name)
            #
            #     # Выводим содержимое каждого найденного тега
            #     for tag in tag_elements:
            #         print(tag)

        else:
            print("Connection Lost, please try again")

    ' class ="serp-item serp-item_link" ,data-qa="vacancy-serp__vacancy vacancy-serp__vacancy_standard" '
    'id="HH-React-Root"'