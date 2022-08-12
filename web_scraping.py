from bs4 import BeautifulSoup
import requests
import os


def imagedown(url, folder):
    newdir = os.path.join(os.getcwd(), folder)
    isExist = os.path.exists(newdir)
    if not isExist:
        os.mkdir(newdir)

    os.chdir(newdir)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')
    prices = soup.find_all(text='$')
    pricesLength = len(prices)

    index = 0
    with open(folder + "_data", 'w') as fd:
        fd.write("[\n")
        for image in images:
            if(index >= pricesLength):
                break
            name = image['alt']
            link = image['src']
            price = prices[index].parent.find("strong").string
            fileExtension = link[len(link) - 4:]
            fileName = name.replace(' ', '-').replace('/', '') + fileExtension

            print("Checking: ", link)
            if not link.startswith('https://'):
                continue

            with open(fileName, 'wb') as f:
                im = requests.get(link)
                f.write(im.content)
                print("Writing: ", name, url, price, " --> ",
                      index, " : ", pricesLength)

                line = "{ id: '" + str(index) + "', text: '" + \
                    name + "', price: " + \
                    str(price).replace(",", "") + \
                    ", img: '" + fileName + "' },\n"
                fd.write(line)

            index = index + 1

        fd.write("]\n")


url = "https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48"
imagedown(url, "data")
