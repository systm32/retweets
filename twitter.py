import requests
from BeautifulSoup import BeautifulSoup
from ConfigParser import SafeConfigParser
import HTMLParser
headers={"Connection": "keep-alive","X-Requested-With": "XMLHttpRequest","Accept-Language":"en-US,en;q=0.5", "Accept": "application/json, text/javascript, */*; q=0.01", "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0", "Accept-Encoding": "gzip", "Content-Type": "application/x-www-form-urlencoded; charset=utf-8", "Proxy-Connection": "keep-alive"}
proxies = {'http':'127.0.0.1:8081','https':'127.0.0.1:8081'}


def retweet(tag):
	login_cookies = getLoginSession()
	config = SafeConfigParser()
	config.optionxform = str
	config.read("tags.cfg")
	tags = dict(config.items('TAGS'))
	for val in tags.keys():
		tag = tags[val]
		url='https://twitter.com/search?src=typd&q='+tag
		r = requests.get(url,verify=False,proxies=proxies,headers=headers,cookies=login_cookies)
		page = r.text
		soup = BeautifulSoup(page)
		input = soup.findAll('input',{'name':'authenticity_token'});
		div = soup.findAll('div',{'class':'account-group js-mini-current-user'})
		data_user_id = div[0]['data-screen-name']
		referer = 'https://twitter.com/'+data_user_id
		headers['Referer'] = referer;
		print headers;
		authenticity_token = input[0]['value']
		print authenticity_token
		params = {}
		params['authenticity_token'] = authenticity_token
		tweets = soup.findAll('li',{'data-item-type':'tweet'})
		for tweet in tweets:
			params['id'] = tweet['data-item-id']
			retweet_url = 'https://twitter.com/i/tweet/retweet'
			print params
			r_retweet = requests.post(retweet_url,data=params,verify=False,cookies=login_cookies,proxies=proxies,headers=headers)



def getLoginSession():
	url = 'https://twitter.com'
	r = requests.get(url,verify=False)
	cookies = dict(r.cookies)
	page = r.text
	soup = BeautifulSoup(page);
	input = soup.findAll('input',{'name':'authenticity_token'});
	authenticity_token = input[0]['value'];
	config = SafeConfigParser()
	config.optionxform = str
	config.read("tags.cfg")
	username = config.get('USER','username')
	password = config.get('USER','password')
	login_url = 'https://twitter.com/sessions'
	params = {}
	params['session[username_or_email]'] = username
	params['session[password]'] = password
	params['authenticity_token'] = authenticity_token
	params['redirect_after_login'] = '/'
	params['return_to_ssl'] = 'true';

	login_req = requests.post(login_url,data=params,cookies=cookies,verify=False,proxies=proxies,headers=headers,allow_redirects=False)
	login_cookies = login_req.cookies;
	
	check_url = 'https://twitter.com/'
	check_req = requests.get(check_url,headers=headers,proxies=proxies,verify=False,cookies=login_cookies);
	return login_cookies;


if __name__ == '__main__':
	retweet()
