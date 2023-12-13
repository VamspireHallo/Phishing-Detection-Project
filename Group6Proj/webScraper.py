from collections import Counter
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse

def getFeatures(url):
    results = []
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)
        return "Error fetching website"
    if r.status_code == 200:
        soup = bs(r.content, 'html.parser')
        list_of_links = soup.find_all('a')



        #Number of dots
        dotCount = 0
        for c in r.url:
            if c == '.':
                dotCount += 1
        results.append(dotCount)

        #NumDash
        dashCount = 0
        for c in r.url:
            if c == '-':
                dashCount += 1
        results.append(dashCount)

        #NumSensitiveWords
        numSensitiveWords = 0
        sensitive_words = ["secure", "account", "webscr", "login", "signin", "banking", "confirm"]
        for word in sensitive_words:
            if word in url:
                numSensitiveWords += 1
        results.append(numSensitiveWords)

        #PctExtHyperlinks
        ext_count = 0
        ext_pct = 0
        main_domain = urlparse(url).hostname
        for link in list_of_links:
            ext = urlparse(link.get("href")).hostname
            if ext is None:
                continue
            if ext != main_domain and not ext.endswith('.' + main_domain):
                ext_count += 1
        if len(list_of_links) > 0:
            ext_pct = ext_count / len(list_of_links)
        results.append(ext_pct)

        #Insecure forms
        temp = []
        for link in list_of_links:
            action = link.get('action', '')
            csrf_token = link.find('input', {'name': 'csrf_token'})
            if action.startswith('https://'):
                temp.append(link)
            elif csrf_token is None:
                temp.append(link)

        insecure_form = 0
        if len(temp) > 0:
            insecure_form = 1
        results.append(insecure_form)

        #PctNullSelfRedirectHyperlinks
        nullSelfRedLinkCount = 0
        for link in list_of_links:
            count = 0
            href = link.get("href")
            if href is None:
                count += 1
            elif href == r.url and count == 0:
                count += 1
            elif isinstance(href, str) and '#' in href and count == 0:
                count += 1
            elif isinstance(href, str) and 'file://' in href and count == 0:
                count += 1
            if count > 0:
                nullSelfRedLinkCount += 1
        nullSelfRedLinkPCT = 0
        if len(list_of_links) > 0:
            nullSelfRedLinkPCT = nullSelfRedLinkCount/len(list_of_links)

        results.append(nullSelfRedLinkPCT)


        #FrequentDomainNameMismatch
        list_of_domains = []
        main_domain = urlparse(url).netloc
        main_domain = split_helper(main_domain)
        frequent = main_domain
        for link in list_of_links:
            if urlparse(link.get('href')).netloc:
                list_of_domains.append(urlparse(link.get('href')).netloc)
                frequent = Counter(list_of_domains).most_common(1)[0][0]
                frequent = split_helper(frequent)
        if frequent != main_domain:
            results.append(1)
        else:
            results.append(0)



        #SubmitInfoToEmail
        contains_mailto = 0
        if 'mailto' in soup.prettify():
            contains_mailto = 1
        if contains_mailto == 1:
            results.append(1)
        else:
            results.append(0)

        #iframe or frame
        # Check for iframes
        iframes = soup.find_all('iframe')
        contains_iframe_or_frame = 0
        if iframes:
            contains_iframe_or_frame = 1
        # Check for frames
        frames = soup.find_all('frame')
        if frames:
            contains_iframe_or_frame = 1
        results.append(contains_iframe_or_frame)

        #PctExtNullSelfRedirectHyperlinksRT
        external_link_indicators = ['#','javascript:void(0)']
        ext_links = []
        url_root = split_helper(urlparse(url).netloc)
        for link in list_of_links:
            href = link.get('href')
            if href is not None:
                parsed_href = urlparse(href)
                if parsed_href.netloc:
                    root = split_helper(parsed_href.netloc)
                    if root != url_root or href in external_link_indicators:
                        ext_links.append(link)
        pctExtNull = 0
        if len(list_of_links) > 0:
            pctExtNull = len(ext_links) / len(list_of_links)
        if pctExtNull < 0.33:
            results.append(1)
        elif pctExtNull  >= 33 and pctExtNull <= 67:
            results.append(0)
        else:
            results.append(-1)
        return results
    else:
        return "Error connecting"

def split_helper(input):

    return '.'.join(input.split('.')[-2:])