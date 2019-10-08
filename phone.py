import requests
import re
import csv

column_name = ["phone name", "height", "width"]
phone = []
phone_link = []
row_info = []
height_in_mm = []
height_in_inch = []
width_in_mm = []
width_in_inch = []
thickness_in_mm = []
thickness_in_inch = []


def phone_details(links):
    for i in range(len(links)):
        resp = requests.get(links[i])
        text1 = resp.text
        text1 = text1.replace("\n", " ")
        dimensions = re.compile(r'<td class="nfo" data-spec="dimensions">(.*?)</td>')
        dimensions = re.findall(dimensions, text1)
        size = dimensions[0]
        size = re.findall(r'\d*\.\d+|\d+', size)
        global height_in_mm, height_in_inch, width_in_mm, width_in_inch, thickness_in_mm, thickness_in_inch
        height_in_mm.append(size[0])
        height_in_inch.append(size[3])
        width_in_mm.append(size[1])
        width_in_inch.append(size[4])
        thickness_in_mm.append(size[2])
        thickness_in_inch.append(size[5])
        size.pop()


def phone_name(name):
    for i in range(len(name)):
        phone_name = re.compile(r'https://www.gsmarena.com/(.*?)-')
        result = re.findall(phone_name, name[i])
        global phone
        phone.append(result[0])
        result.pop()


def csv_create(column, row):
    with open("phone.csv", "a", newline='') as csvf:
        csv_writer = csv.writer(csvf, delimiter=',', quotechar="\"", quoting=csv.QUOTE_ALL)
        csv_writer.writerow(column)
        for book in row:
            csv_writer.writerow(book)


def phone_link_append():
    for line in open('phone_links.txt', 'r').readlines():
        global phone_link
        phone_link.append(line.strip())


def row_info_add():
    global row_info, phone, height_in_mm, width_in_mm
    for i in range(len(height_in_mm)):
        row_info.append([phone[i], height_in_mm[i], width_in_mm[i]])


phone_link_append()
phone_details(phone_link)
phone_name(phone_link)
row_info_add()
csv_create(column_name, row_info)


