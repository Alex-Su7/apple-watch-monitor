import os
import time
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 日志配置
logging.basicConfig(filename='watch_scraper.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

# 邮件配置（使用环境变量以避免硬编码凭据）
EMAIL_ADDRESS = os.getenv("WATCH_EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("WATCH_EMAIL_PASSWORD", "")
TO_EMAIL = os.getenv("WATCH_TO_EMAIL", "")
SMTP_SERVER = os.getenv("WATCH_SMTP_SERVER", "smtp.qq.com")
SMTP_PORT = int(os.getenv("WATCH_SMTP_PORT", "587"))

# EdgeDriver路径（可通过环境变量配置）
driver_path = os.getenv("EDGEDRIVER_PATH")
log_path = "NUL" if os.name == "nt" else "/dev/null"
service = Service(executable_path=driver_path, log_path=log_path) if driver_path else Service(log_path=log_path)

# 配置Edge浏览器选项
edge_options = Options()
edge_options.add_argument("--headless=new")  # 以无头模式运行浏览器
edge_options.add_argument("--ignore-certificate-errors")  # 忽略SSL错误
edge_options.add_argument("--ignore-ssl-errors=yes")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0")
edge_options.add_argument("--log-level=3")  # 仅输出严重错误

# 设置发送邮件的函数
def send_email(subject, body, to_email):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not to_email:
        logging.error("Email credentials or recipient are not configured. Set WATCH_EMAIL_ADDRESS, "
                      "WATCH_EMAIL_PASSWORD, and WATCH_TO_EMAIL.")
        return

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_ADDRESS, to_email, text)
            logging.info(f"Email sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# 创建WebDriver对象
driver = webdriver.Edge(service=service, options=edge_options)

def normalize_text(text):
    return " ".join(text.split())


def get_apple_watch_info():
    url = 'https://www.apple.com.cn/shop/refurbished/watch/apple-watch-se-apple-watch-series-9'
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.as-producttile"))
        )

        soup = BeautifulSoup(driver.page_source, 'lxml')
        products = soup.select('li.as-producttile')

        watch_info = {}

        for product in products:
            title_element = product.select_one('h3')
            price_element = product.select_one('div.as-price-currentprice')
            if title_element and price_element:
                title = normalize_text(title_element.text)
                price = normalize_text(price_element.text)
                watch_info[title] = price

        logging.info(f"Scraped {len(watch_info)} products")
        return watch_info
    except Exception as e:
        logging.error(f"Error while scraping: {e}")
        return {}

def generate_html_table(title, data):
    html = f'<h3>{title}</h3>'
    html += '<table border="1" style="border-collapse: collapse; width: 100%;">'
    html += '<tr><th>商品名</th><th>价格</th></tr>'
    for item in data:
        html += f"<tr><td>{item['name']}</td><td>{item['price']}</td></tr>"
    html += '</table>'
    return html


def generate_html_report(initial=None, new=None, changed=None, removed=None):
    sections = []
    if initial:
        sections.append(generate_html_table("当前在售产品", initial))
    if new:
        sections.append(generate_html_table("新增产品", new))
    if changed:
        sections.append(generate_html_table("价格变动", changed))
    if removed:
        sections.append(generate_html_table("下架产品", removed))
    if not sections:
        sections.append("<p>暂无更新。</p>")
    return "<html><body>" + "".join(sections) + "</body></html>"

def print_statistics():
    watch_info = get_apple_watch_info()
    se_count = sum('SE' in name for name in watch_info)
    s9_count = sum('Series 9' in name for name in watch_info)
    print(f"当前商城内的翻新SE手表总数量为：【{se_count}】，当前商城内的翻新S9手表总数量为：【{s9_count}】")

def monitor_website(interval=60):
    known_products = get_apple_watch_info()
    initial_rows = [{'name': name, 'price': price} for name, price in known_products.items()]
    send_email("Initial Apple Watch Info", generate_html_report(initial=initial_rows), TO_EMAIL)

    count = 0
    while True:
        time.sleep(interval)
        current_products = get_apple_watch_info()
        new_products = []
        changed_products = []
        removed_products = []

        for name, price in current_products.items():
            if name not in known_products:
                new_products.append({'name': name, 'price': price})
            elif known_products[name] != price:
                changed_products.append({'name': name, 'price': price})

        for name, price in known_products.items():
            if name not in current_products:
                removed_products.append({'name': name, 'price': price})

        if new_products or changed_products or removed_products:
            report = generate_html_report(
                new=new_products,
                changed=changed_products,
                removed=removed_products,
            )
            send_email("Apple Watch Inventory Update", report, TO_EMAIL)
            known_products = current_products

        count += interval
        if count % 300 == 0:  # 每5分钟统计一次
            print_statistics()

try:
    # 运行监视程序
    monitor_website()
except KeyboardInterrupt:
    logging.info("Script terminated by user")
finally:
    driver.quit()
    logging.info("Driver closed")
