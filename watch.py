import time
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

# 日志配置
logging.basicConfig(filename='watch_scraper.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

# 邮件配置
EMAIL_ADDRESS = '1175441676@qq.com'
EMAIL_PASSWORD = 'bebdgvjynqfoihii'
TO_EMAIL = '1175441676@qq.com'
SMTP_SERVER = 'smtp.qq.com'
SMTP_PORT = 587

# EdgeDriver路径
service = Service('D:\\360data\\重要数据\\桌面\\edgedriver_win64\\msedgedriver.exe')

# 配置Edge浏览器选项
edge_options = Options()
edge_options.add_argument("--headless")  # 以无头模式运行浏览器
edge_options.add_argument("--ignore-certificate-errors")  # 忽略SSL错误
edge_options.add_argument("--ignore-ssl-errors=yes")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0")

# 设置发送邮件的函数
def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to_email, text)
        logging.info(f"Email sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
    finally:
        server.quit()

# 创建WebDriver对象
driver = webdriver.Edge(service=service, options=edge_options)

def get_apple_watch_info():
    url = 'https://www.apple.com.cn/shop/refurbished/watch/apple-watch-se-apple-watch-series-9'
    try:
        driver.get(url)
        time.sleep(10)  # 增加等待时间，确保页面完全加载

        soup = BeautifulSoup(driver.page_source, 'lxml')
        products = soup.find_all('li')

        watch_info_list = []

        for product in products:
            title_element = product.find('h3')
            price_element = product.find('div', class_='as-price-currentprice as-producttile-currentprice')
            if title_element and price_element:
                title = title_element.text.strip()
                price = price_element.text.strip()
                watch_info_list.append({'name': title, 'price': price})

        logging.info(f"Scraped {len(watch_info_list)} products")
        return watch_info_list
    except Exception as e:
        logging.error(f"Error while scraping: {e}")
        return []

def generate_html_table(data):
    html = '<html><body>'
    html += '<h2>Apple Watch Info</h2>'
    html += '<table border="1" style="border-collapse: collapse; width: 100%;">'
    html += '<tr><th>商品名</th><th>价格</th></tr>'
    for item in data:
        html += f"<tr><td>{item['name']}</td><td>{item['price']}</td></tr>"
    html += '</table></body></html>'
    return html

def monitor_website(interval=60):
    known_products = get_apple_watch_info()
    send_email("Initial Apple Watch Info", generate_html_table(known_products), TO_EMAIL)

    while True:
        time.sleep(interval)
        current_products = get_apple_watch_info()
        
        new_products = [product for product in current_products if product not in known_products]
        
        if new_products:
            send_email("New Apple Watch Available", generate_html_table(new_products), TO_EMAIL)
            known_products.extend(new_products)

try:
    # 运行监视程序
    monitor_website()
except KeyboardInterrupt:
    logging.info("Script terminated by user")
finally:
    driver.quit()
    logging.info("Driver closed")
