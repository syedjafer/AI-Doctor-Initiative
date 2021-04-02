import requests
from bs4 import BeautifulSoup
base_url = "https://doctorfinder.ama-assn.org/doctorfinder/"
import traceback

url = "https://doctorfinder.ama-assn.org/doctorfinder/specialtySearch.do?specialty={}&state={}&city=&zip={}"
# url = "https://doctorfinder.ama-assn.org/doctorfinder/specialtySearch.do?specialty={}&state={}&city=&zip="


specialities = {}
specialty_file = open("specialities3.txt","r")
data = specialty_file.readlines()
for line in data:
	line = line.strip().split(",")
	specialities[line[1]] = line[0]

state_zip_code = []
state_zip_file = open("us_data","r")
data = state_zip_file.readlines()
for line in data:
	line = line.strip().split(",")
	state_zip_code.append( (line[0], line[1]) )

import re
def parseCookieFile(cookiefile):
    """Parse a cookies.txt file and return a dictionary of key value pairs
    compatible with requests."""

    cookies = {}
    with open (cookiefile, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                lineFields = line.strip().split('\t')
                try:
                	cookies[lineFields[5]] = lineFields[6]
                except:
                	pass
    return cookies
res = open("result_a_3.csv","a")

cookies = parseCookieFile("cookies.txt")
for specialty_key, code in specialities.items():
	for item in state_zip_code:
		# furl = url.format(code, item[0], item[1] )
		furl = url.format(code, item[0], item[1])
		# print(specialty_key, code, item, furl)
		try:
			req = requests.get(furl, timeout=30)
			if req.status_code == 200:
				try:
					soup = BeautifulSoup(req.content, "html.parser")
					trs = soup.find_all("tr")
					for row in range(1,len(trs)):
						try:
							each_data = trs[row].find_all("td")
							specialty_name = each_data[1].text.strip() if each_data[1] else None
							location = each_data[2].text.strip().replace(","," ") if  len(each_data)>2 and each_data[2] else None
							doc_name = each_data[0].text
							doc_url = each_data[0].find("a")
							doc_url = doc_url["href"] if doc_url else ""
							actual_doc_url = base_url + doc_url
							doc_data = ""
							gender = "Unknown"
							details = ""
							# print(actual_doc_url)
							doc_req = requests.get(actual_doc_url, cookies=cookies, timeout=30)
							if doc_req.status_code == 200:
								
								try:
									dsoup = BeautifulSoup(doc_req.content, "html.parser")
									dsoup = dsoup.find("table")
									doc_data = str(dsoup.text).strip().lower()
									gender = "Male" if "male" in doc_data else "Female"
									details = doc_data
								except Exception as ex:
									gender = "Unknown"
									details = ""
						except Exception as ex:
							print("1 ")
							details = ""
							print(str(ex))
							traceback.print_exc()
						else:
							details = details.strip().replace("\n","").replace("\r","").replace("\t","")
							print(specialty_key, item, actual_doc_url)
							if actual_doc_url != "https://doctorfinder.ama-assn.org/doctorfinder/":
								print("SUCCESS")
								fdata = "|".join([ str(specialty_name).strip(), str(location).strip(), str(doc_name).strip(), actual_doc_url.strip(), str(gender).strip(), str(details).strip() ])+"\n"
								res.write(fdata)
				except Exception as ex:
					print("2 ",ex)
					pass
		except Exception as ex:
			print("3 ",ex)
			pass



res.close()