import requests
from bs4 import BeautifulSoup

url = "http://phaster.com/zip_code.html"
req = requests.get(url)

tds = []
res = []
if req.status_code == 200:
	soup = BeautifulSoup(req.content, 'html.parser')
	divs = soup.find_all("table")
	for div in divs:
		rows = div.find_all('tr')
		for row in rows :
			temp = row.findAll('td')
			res.append([item.text for item in temp])
fl = open("us_data","a")
new_data = []
for val in res:
	if len(val)>2 and val[1]:
		val[1] = val[1].split("\xa0")
		val[2] = val[2].split("\xa0")
		for itr,item in enumerate(val[2]):
			nums, nums1 = [], []
			try:
				nums = [int(x) for x in item.split(" thru ")]
			except Exception as ex:
				# print(str(ex))
				try:
					nums1 = [int(x.strip()) for x in item.split("-")]
				except Exception as ex:
					# print(str(ex))
					pass
			total_lists = nums + nums1 
			total_lists.sort()
			if len(total_lists) > 1:
				all_nums = [ list(range(total_lists[it], total_lists[it+1]))  for it in range(len(total_lists)-1)]
				all_nums = [ f for ite in all_nums for f in ite  ]
				for vl in all_nums:
					print( val[0].split("(")[-1].split(")")[0], val[1][itr], vl )
					fl.write(",".join( [str(val[0].split("(")[-1].split(")")[0]),str(vl)] )+"\n" )
fl.close()