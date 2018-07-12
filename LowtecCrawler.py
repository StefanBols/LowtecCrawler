from urllib.request import urlopen
import re

def getIt(url, regex):
    response = urlopen(url)
    html = response.read()
    htmlPython = html.decode('utf-8')

    content = re.findall(regex, htmlPython)
    content = set(content) #Remove duplicates
    content = [i for i in content if i[0] != url] #Remove if url is current url

    return content

############################################# GET BRANDS #############################################
brandslinks = getIt('https://www.lowtec.de/en/', r'<option class=\"option_selection\" value=\"(.+)\"[\s]*>\n(.+)\n<\/option>')
print ('Found ' + str(len(brandslinks)) + ' brands')
brands = [x[1] for x in brandslinks]
brandslinks.sort(key=lambda tup: tup[1])


############################################# GET MODELS #############################################
for brandlink in brandslinks:
    link = brandlink[0]
    brandurl = link
    brand = brandlink[1]

    print ('Resolving \'' + brand + '\'')

    modellinks = getIt(link, r'<option class=\"option_selection\" value=\"'+link+'(.+)\"[\s]*>\n(.+)\n<\/option>')
    modellinks.sort(key=lambda tup: tup[1])
    print ('Found ' + str(len(modellinks)) + ' models')

    print ([x[1] for x in modellinks])

    ############################################# GET TYPES #############################################
    for modellink in modellinks:
        link = brandurl + modellink[0]
        model = modellink[1]

        print ('Resolving \'' + brand + ' ' + model + '\'')
        typelinks = getIt(link, r'<option class=\"option_selection\" value=\"'+link+'(.+)\"[\s]*>\n(.+)\n<\/option>')
        typelinks.sort(key=lambda tup: tup[1])
        print ('Found ' + str(len(typelinks)) + ' types')

        for cartype in typelinks:
            cartype = cartype[1]
            print ('Printing \'' + brand + ' ' + model + ' '+ cartype+'\' to csv file')
            filename = './output.csv'
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(brand + ';' + model + ';' + cartype + '\n')

print ('Operation finished')