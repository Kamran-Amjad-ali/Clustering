
import requests as rq
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import codecs

f=open('url1').readlines()
url_list=[x.strip() for x in f]

for i in range(len(url_list)):
	try:
		driver = webdriver.Chrome(executable_path='/home/kamran/Desktop/chromedriver')
		driver.get(url_list[i])
		time.sleep(5)
		content = driver.page_source.encode('utf-8').strip()
		driver.close()	
		soup = BeautifulSoup(content,"html.parser")
		#officials = soup.findAll("div",{"class":"text"})
		poss = soup.findAll("p","positive")
		negs = soup.findAll("p","negative")
		pos_reviews=[t.text for t in poss]
		neg_reviews=[t.text for t in negs]		
		ref_pos_rev=[x.strip() for x in pos_reviews]
		ref_neg_rev=[x.strip() for x in neg_reviews]
		ref_rev_pos=[]
		for h in ref_pos_rev:
			posit=re.sub(u"[^a-zA-Z0-9]+", ' ', unicode(h))
			ref_rev_pos.append(posit)
		ref_rev_neg=[]
		for k in ref_neg_rev:
			negit=re.sub(u"[^a-zA-Z0-9]+", ' ', unicode(k))
			ref_rev_neg.append(negit)
		filename_pos="pos_file_" + str(i) + ".txt"
		filename_neg="neg_file_" + str(i) + ".txt"
		f_pos= codecs.open(filename_pos,'w', encoding='utf-8')
		f_neg= codecs.open(filename_neg,'w', encoding='utf-8')
		for listitem in ref_rev_pos:
			f_pos.write('%s\n' % listitem)	

		for listitem in ref_rev_neg:
			f_neg.write('%s\n' %listitem)

		f_pos.close()
		f_neg.close()
		print i
	except Exception as e:
		print e	
		pass

