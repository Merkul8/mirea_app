import aiosmtplib
from email.message import EmailMessage
import ssl
import config


class Sender:
    @staticmethod
    async def send(
            subject: str,
            to_email: str,
            content: str,
    ) -> bool:
        # Получаем данные из конфига
        smtp_config = config.smtp_data()

        # Создаем сообщение
        message = EmailMessage()
        message["From"] = smtp_config["login"]
        message["To"] = to_email
        message["Subject"] = subject

        # Устанавливаем содержимое (можно использовать HTML)
        message.set_content(content)

        # Настройки SSL контекста
        ssl_context = ssl.create_default_context()

        try:
            # Подключаемся к SMTP серверу Gmail
            smtp_client = aiosmtplib.SMTP(
                hostname="smtp.gmail.com",
                port=465,
                use_tls=True,
                tls_context=ssl_context
            )

            await smtp_client.connect()

            # Переходим в TLS режим (обязательно для Gmail)
            # await smtp_client.starttls()

            # Логинимся
            await smtp_client.login(
                smtp_config["login"],
                smtp_config["password"]
            )

            # Отправляем письмо
            await smtp_client.send_message(message)

            # Закрываем соединение
            await smtp_client.quit()

            return True

        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")
            return False