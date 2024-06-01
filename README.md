# Apple Watch Refurbished Monitor

## Description

This script monitors the Apple Store for refurbished Apple Watch SE and Apple Watch Series 9 listings. It scrapes the webpage for product information and sends an email notification when new products are available.

## Features

- Scrapes product name and price from the specified Apple Store page.
- Sends an email notification with the product information.
- Continuously monitors the webpage for new products and sends notifications when new products are found.
- Includes error handling and logging for better debugging and maintenance.

## Requirements

- Python 3.x
- `selenium` library
- `beautifulsoup4` library
- `lxml` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/apple-watch-monitor.git
    cd apple-watch-monitor
    ```

2. Install required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Download the Edge WebDriver from [here](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) and place it in your desired directory.

## Configuration

1. Update the email configuration in the script:
    ```python
    EMAIL_ADDRESS = 'your_email@example.com'
    EMAIL_PASSWORD = 'your_email_password'
    TO_EMAIL = 'recipient_email@example.com'
    SMTP_SERVER = 'smtp.your_email_provider.com'
    SMTP_PORT = 587
    ```

2. Update the Edge WebDriver path:
    ```python
    service = Service('path_to_your_msedgedriver.exe')
    ```

## Usage

Run the script:
```sh
python watch.py
```

The script will start monitoring the Apple Store for refurbished Apple Watch SE and Apple Watch Series 9. It will send an email notification with the product information when it finds new products.

## Logging

Logs are written to `watch_scraper.log`. It contains information about the script's operation and errors for debugging purposes.

## License

This project is licensed under the MIT License.

---

# Apple Watch 翻新产品监控

## 描述

此脚本监控 Apple Store 上的翻新 Apple Watch SE 和 Apple Watch Series 9 列表。它抓取网页上的产品信息，并在有新产品可用时发送电子邮件通知。

## 特点

- 从指定的 Apple Store 页面抓取产品名称和价格。
- 发送包含产品信息的电子邮件通知。
- 持续监控网页上的新产品，并在发现新产品时发送通知。
- 包含错误处理和日志记录，以便更好地调试和维护。

## 需求

- Python 3.x
- `selenium` 库
- `beautifulsoup4` 库
- `lxml` 库

## 安装

1. 克隆仓库：
    ```sh
    git clone https://github.com/yourusername/apple-watch-monitor.git
    cd apple-watch-monitor
    ```

2. 安装所需的软件包：
    ```sh
    pip install -r requirements.txt
    ```

3. 从 [这里](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) 下载 Edge WebDriver，并将其放置在所需的目录中。

## 配置

1. 更新脚本中的电子邮件配置：
    ```python
    EMAIL_ADDRESS = 'your_email@example.com'
    EMAIL_PASSWORD = 'your_email_password'
    TO_EMAIL = 'recipient_email@example.com'
    SMTP_SERVER = 'smtp.your_email_provider.com'
    SMTP_PORT = 587
    ```

2. 更新 Edge WebDriver 路径：
    ```python
    service = Service('path_to_your_msedgedriver.exe')
    ```

## 使用

运行脚本：
```sh
python watch.py
```

脚本将开始监控 Apple Store 上的翻新 Apple Watch SE 和 Apple Watch Series 9。当发现新产品时，它会发送包含产品信息的电子邮件通知。

## 日志

日志记录在 `watch_scraper.log` 文件中。它包含脚本操作和错误信息，以便调试使用。

## 许可证

此项目是根据 MIT 许可证授权的。
