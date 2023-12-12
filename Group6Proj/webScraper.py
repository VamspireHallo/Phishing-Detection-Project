from collections import Counter
from operator import truediv
import requests 
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from urllib.request import urlopen
import urllib
import joblib
import numpy
import argparse
import tkinter as tk

def getFeatures(url):

    array = []
    
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)
        return "Error fetching website from URL"

    if r.status_code == 200:

        soup = bs(r.content, 'html.parser')

        links_list = soup.find_all('a')

    

    #1. Number of dots
        dotCount = 0

        for c in r.url:
            if c == '.':
                dotCount += 1

        # print("1. # of dots in URL:", dotCount)
        array.append(dotCount)

    # 2. NumDash

        dashCount = 0

        for c in r.url:
            if c == '-':
                dashCount += 1

        # print("2. # of dashes in URL:", dashCount)
        array.append(dashCount)

    # 3. NumSensitiveWords

        numSensitive = 0 

        sensitive_words = ["secure", "account", "webscr", "login","ebayisapi", "signin", "banking", "confirm"]

        for word in sensitive_words:
            if word in url:
                numSensitive += 1

        # print('3. # of sensitive words: ',numSensitive)
        array.append(numSensitive)    

    # 4. PctExtHyperlinks

        external_count = 0

        current_domain = urlparse(url).hostname

        for link in links_list:
            href = urlparse(link.get("href"))
            link_domain = href.hostname
            
            if link_domain is None:  # Skip if href is a relative link
                continue
            
            if link_domain != current_domain and not link_domain.endswith('.' + current_domain):
                external_count += 1

        total_count = len(links_list)
        ext_percentage = 0

        if(external_count != 0): ext_percentage = (external_count / total_count)
        # print('Total # of links', total_count)
        # print('Total # of ext links', external_count)
        # print(f'4. Percentage of external hyperlinks: {ext_percentage}%')
        array.append(ext_percentage)    

    #5. Insecure forms
        temp = []
        for link in links_list:
            action = link.get('action', '')
            csrf_token = link.find('input', {'name': 'csrf_token'})
            if action.startswith('https://'):
                temp.append(link)
            elif csrf_token is None:
                temp.append(link)
        
        insecure_form = 0
        if len(temp) > 0:
        #
        # else:
            insecure_form = 1
            # print(insecure_form)
        array.append(insecure_form)
    # 6. PctNullSelfRedirectHyperlinks

        nsr_links = 0

        def is_Null(link):
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
            return count > 0


        for link in links_list:
            if(is_Null(link)): 
                nsr_links += 1

        # print('Total # of links: ',total_count)
        # print('# of null self redirecting links: ',nsr_links)
        Null_percentage = 0

        if(external_count != 0): Null_percentage = (nsr_links/total_count)
        # print('6. % of ext links are null, etc: ',Null_percentage, '%')
        array.append(Null_percentage)           


    # 7. FrequentDomainNameMismatch

        # extracts href, parses href for netloc (domain name), creates list of domain names
        domains = []

        for link in links_list:
            if urlparse(link.get('href')).netloc:
                domains.append(urlparse(link.get('href')).netloc)
        

        # gets the most common domain name

        # webpage domain name
        webpage_domain = urlparse(url).netloc
        webpage_domain = ".".join(webpage_domain.split(".")[-2:])
        
        most_common_domain = "None"
        if domains: 
            most_common_domain = Counter(domains).most_common(1)[0][0]
            most_common_domain = ".".join(most_common_domain.split(".")[-2:])
                

        # print("Webpage domain name: ",webpage_domain)
        # print("Most frequent HTML source code domain name: ",most_common_domain)
        domain_mist = 0
        if most_common_domain != webpage_domain:
            domain_mist = 1
            # print(domain_mist)
        # else:
        #         # print(domain_mist)
        if most_common_domain != webpage_domain: array.append(1)
        else: array.append(0)



    # 8. SubmitInfoToEmail

        has_mailto = 0

        if 'mailto' in soup.prettify():
            has_mailto = 1
            

        # print(f'8. {has_mailto}')
        if has_mailto == 1: array.append(1)
        else: array.append(0)    

    #9. iframe or frame

        iframes = soup.find_all('iframe')
        i_frame = 0
        if iframes:
            i_frame = 1
            # print(f'9 {i_frame}')

        # Check for frames
        frames = soup.find_all('frame')
        if frames:
            i_frame = 1
            # print(f'9 {i_frame}')

        # if not iframes and not frames:
        #     # print(f'9 {i_frame}')
        array.append((i_frame))

    #10. PctExtNullSelfRedirectHyperlinksRT

        dictionary = ['#','#skip','#content','javascript:void(0)']

        external_links = []
        for link in links_list:
            href = link.get('href')
            if href is not None:
                parsed_href = urlparse(href)
                if parsed_href.netloc:
                    root_domain = '.'.join(parsed_href.netloc.split('.')[-2:])
                    url_root_domain = '.'.join(urlparse(url).netloc.split('.')[-2:])
                    if root_domain != url_root_domain or href in dictionary:
                        external_links.append(link)


        external_count = len(external_links)
        total_count = len(links_list)

        if(external_count != 0 and total_count != 0): percentage = (external_count / total_count)
        else: percentage = 0
        # print(f'10. Percentage of external links with different domain names, starts with "#", or using "JavaScript ::void(0)": {percentage*100}%')
        if percentage * 100 < 31:
            #print('1\n')
            array.append(1)
        elif percentage * 100 >= 31 and percentage <= 67:
            #print('0\n')
            array.append(0)
        else:
            #print('-1\n')
            array.append(-1)


        # List = [dotCount, dashCount, numSensitive, ext_percentage, insecure_form, Null_percentage, domain_mist, has_mailto, i_frame, percentage ]
        # print(List)
        # print(array)





        # # Predicting
        # model_path = "models/Phishing_RFC.joblib"
        # model = joblib.load(model_path)
        # input = numpy.array(array).reshape(1,-1)
        # prediction = model.predict(input)
        # return prediction
        return array
    else:
        print("Error connecting to website")
        return "Error connecting to website"

# def run_gui():
#     def check_phishing():
#         # Get input from the text area
#         input_text = text_input.get("1.0", tk.END).strip()
#         output_text = "Checking..."
#         # Do some processing on the input
#         phishingResult = getPhishing(input_text)
#         if isinstance(phishingResult, (list, tuple)):
#             phishingResult = phishingResult[0]
#
#         if phishingResult==0:
#             output_text = "Legitimate!"
#         elif phishingResult==1:
#             output_text = "Phishing :("
#         else:
#             output_text = phishingResult
#
#         # Update the output label with the result
#         output_label.config(text=output_text)
#
#     # Create the main window
#     window = tk.Tk()
#     window.title("Phishing Website Checker")
#
#     #Vars
#     backgroundColor = "#a4ebe2"
#     my_font = ("Cascadia Code", 20)
#     my_font_small = ("Cascadia Code", 16)
#
#     window.configure(bg=backgroundColor)
#
#     # Create the Header label
#     header_label = tk.Label(window,bg=backgroundColor,font=my_font, text="Input your phishing website below and press the run button")
#     desc_label = tk.Label(window,bg=backgroundColor,font=my_font_small, text="Should be in the format: 'https://website.com' ")
#
#     # Create the input text area
#     text_input = tk.Text(window,height=1,width=50,padx=20, pady=20,font=my_font_small)
#
#     # Create the run button
#     run_button = tk.Button(window,height=2,width=8, text="Run", command=check_phishing)
#
#     # Create the output label
#     output_label = tk.Label(window,bg=backgroundColor,font=my_font, text="")
#
#     header_label.pack(pady=8,padx=40)
#     desc_label.pack(pady=4)
#     text_input.pack(pady=20,padx=20)
#     run_button.pack(pady=8)
#     output_label.pack()
#
#     # Start the main event loop
#     window.mainloop()
#
# run_gui()