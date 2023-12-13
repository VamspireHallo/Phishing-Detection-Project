### Overview
Phishing is a cyber attack usually initiated through sending an email to deceive recipients into sharing sensitive information, download malware, or partake in other harmful actions. The idea of a phishing attack is to deceive victims into giving their personal or valuable information. The information gained is then used by the attackers for their own personal gain or objective. It is one of the most prominent cyber attacks today with over 3.4 billion phishing emails sent daily.

There are many variations of phishing attacks, but all are emails sent to deceive its recipient. The purpose of a phishing attack is to attain sensitive information or download malware on the recipient's device. Attackers spoof email addresses and set up fake websites that the recipients may recognize and trust leading them to input their information. Getting recipients to log into fake versions of popular websites is among the most infamous phishing attacks. These types of phishing emails are sent to millions of recipients in hopes to trick them. Spear phishing is more directed where attackers send emails to a specific individual. Whale phishing is a type of spear phishing that targets high-value individuals, such as CEOs.

Attackers send emails that seem trusted so the victim can act upon what is in the email. These email addresses may be spoofed to look like known trusted companies and set up fake websites to further gain the trust of the victim.

In 2022, there were around 300,000 phishing victims with a total loss of 52 million dollars in the US alone. 

The increasing prevalence of phishing attacks poses a severe threat to an individual’s online security. Phishing and smishing are techniques employed by malicious actors to deceive users and retrieve valuable information by gaining the trust of the victims. These attacks have become more sophisticated and harder to detect, making it crucial to develop robust detection mechanisms to safeguard against them.

### Objective
This project aims to address phishing attacks' pressing needs and problems by developing a program to detect phishing and smishing attacks. Further, this project will as well go into exploring innovative approaches to counter these threats from multiple angles.

Our approach to combat this problem is to detect these emails using trained Machine Learning models to determine whether it believes it’s a phishing email or not. The program will primarily focus on phishing attacks, as other forms, be it smishing for example, will be a topic we will hopefully tackle at a later date for development.

### Live Demo
Live Demo Video: [https://www.youtube.com/watch?v=](https://youtu.be/yj_bCdpq26Q)https://youtu.be/yj_bCdpq26Q

The live demo for the program begins with the prerequisite need to get an .eml file, which can be taken from any email provider you can find and use.

For this example, we have two test .eml files, the first one “safe email.eml”  which has no signs of phishing, while the other file “sign_up.eml” has a recent scam url link which makes it a phishing email.

The phishing detection application basically has you select the browse button to find the .eml file in the directory and once you have the file, you begin the phish check which will go through the information found in the email, specifically the plain text and url content found in the email body, to determine if it is a legitimate or phishing email.

As you can see through the results of the program for safe email, the .eml file is found to be unlikely to be a phishing email. While browsing through the directory for the sign_up email, the phish check

We returns that the url is 100% a phishing link, which the program accurately determines that the email is a phishing attack.

