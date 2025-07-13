import logging
from django.db import close_old_connections, transaction
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from django.db.models import Count, Q
from account.models import UnsentLetter, LetterArchive, GamAccount
import requests
from django.conf import settings
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

# Initialize Fernet cipher for password encryption
cipher_suite = Fernet(settings.ENCRYPTION_KEY)


def letter_delivery():
    """Deliver unsent letters and send notifications"""
    user_data = GamAccount.objects.annotate(
        letter_count=Count('user_letter', filter=Q(user_letter__sent=False))
    ).filter(letter_count__gt=0)

    if not user_data:
        return "No pending notifications"

    user_info = []
    for user in user_data:
        user_info.append({
            "username": user.username,
            "letter_count": user.letter_count,
            "desktop_ip": user.desktop_ip,
            "user_id": user.id
        })

    success_users = []
    for user in user_info:
        try:
            response = requests.post(
                f"http://{user['desktop_ip']}:5000/notify",
                json={
                    'letter_count': user['letter_count'],
                    'username': user['username']
                },
                timeout=10
            )
            response.raise_for_status()
            success_users.append(user['user_id'])
            logger.info(f"Notification sent to {user['username']}")
        except requests.RequestException as e:
            logger.error(f"Notification failed for {user['username']}: {str(e)}")

    # Mark as sent only for successful notifications
    if success_users:
        with transaction.atomic():
            UnsentLetter.objects.filter(
                user_id__in=success_users,
                sent=False
            ).update(sent=True)

    return f"Notifications sent: {len(success_users)}/{len(user_info)}"


def scrape_letters_for_user(user_id):
    """Scrape letters for a single user"""
    try:
        user = GamAccount.objects.get(id=user_id, is_active=True)
        encrypted_pw = user.encrypted_password
        password = cipher_suite.decrypt(encrypted_pw).decode()
    except GamAccount.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return {"status": "error", "message": "User not found"}
    except Exception as e:
        logger.error(f"Password decryption failed for user {user_id}: {str(e)}")
        return {"status": "error", "message": "Decryption error"}

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.binary_location = "/usr/bin/firefox"

    try:
        service = Service(executable_path="/usr/local/bin/geckodriver")
    except Exception as e:
        logger.error(f"WebDriver init failed for {user.username}: {str(e)}")
        return {"status": "error", "message": "Browser setup failed"}

    try:
        # Login process
        wd.get("http://kitgam.kharazmico.com")
        WebDriverWait(wd, 30).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys(user.username)
        wd.find_element(By.ID, "password").send_keys(password)
        wd.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Navigation
        WebDriverWait(wd, 30).until(EC.url_contains("Index.do"))
        WebDriverWait(wd, 30).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "content"))
        )
        WebDriverWait(wd, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='ارجاعات جدید']"))
        ).click()

        # Switch to content frame
        WebDriverWait(wd, 30).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[id^='UIComponent_'][id$='_contentFrame']")
            )
        )

        # Get total pages
        try:
            total_pages = int(wd.find_element(
                By.CSS_SELECTOR, "div.x-paging-info"
            ).text.split()[-1])
        except:
            total_pages = 1

        letters_data = []
        current_page = 1

        while current_page <= total_pages:
            # Page navigation
            if current_page > 1:
                page_input = WebDriverWait(wd, 20).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'x-tbar-page-number'))
                )
                page_input.clear()
                page_input.send_keys(str(current_page))
                page_input.send_keys(Keys.RETURN)
                WebDriverWait(wd, 20).until(
                    EC.staleness_of(wd.find_element(By.ID, "ext-gen100"))
                )

            # Scrape page data
            receivers = WebDriverWait(wd, 30).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.x-grid3-col-dlrFullName")
                )
            )
            letter_ids = wd.find_elements(
                By.CSS_SELECTOR, "div.x-grid3-col-letId"
            )
            senders = wd.find_elements(
                By.CSS_SELECTOR, "div.x-grid3-col-dlvSenderFullName"
            )
            times = wd.find_elements(
                By.CSS_SELECTOR, "div.x-grid3-col-dlvDate"
            )

            for i in range(len(letter_ids)):
                letters_data.append({
                    "letter_id": letter_ids[i].text,
                    "sender": senders[i].text,
                    "receiver": receivers[i].text,
                    "sent_time": times[i].text,
                })

            current_page += 1

        # Bulk create unsent letters
        unsent_letters = []
        for item in letters_data:
            if not UnsentLetter.objects.filter(
                    letter_id=item['letter_id'],
                    sent_time=item['sent_time']
            ).exists():
                unsent_letters.append(
                    UnsentLetter(
                        letter_id=item['letter_id'],
                        user=user,
                        sender=item['sender'],
                        receiver=item['receiver'],
                        sent_time=item['sent_time']
                    )
                )

        if unsent_letters:
            UnsentLetter.objects.bulk_create(unsent_letters, batch_size=50)
            logger.info(f"Created {len(unsent_letters)} letters for {user.username}")

        return {"status": "success", "count": len(unsent_letters)}

    except Exception as e:
        logger.exception(f"Scraping failed for {user.username}:")
        return {"status": "error", "message": str(e)}

    finally:
        try:
            wd.quit()
        except:
            pass
        close_old_connections()


def scrape_all_users():
    """Orchestrate scraping for all active users"""
    user_ids = GamAccount.objects.filter(
        is_active=True
    ).values_list('id', flat=True)

    results = []
    for user_id in user_ids:
        results.append(scrape_letters_for_user(user_id))

    letter_delivery()
    archive_sent_letters()

    success_count = sum(1 for r in results if r.get('status') == 'success')
    return f"Completed: {success_count}/{len(user_ids)} users"


def archive_sent_letters():
    """Archive sent letters and clean up"""
    with transaction.atomic():
        # Get sent letters
        sent_letters = UnsentLetter.objects.filter(sent=True)
        if not sent_letters:
            return "No letters to archive"

        # Create archive records
        archive_entries = [
            LetterArchive(
                user=letter.user,
                letter_id=letter.letter_id,
                sender=letter.sender,
                receiver=letter.receiver,
                sent_time=letter.sent_time
            ) for letter in sent_letters
        ]

        # Bulk operations
        LetterArchive.objects.bulk_create(archive_entries)
        sent_letters.delete()

    logger.info(f"Archived {len(archive_entries)} letters")
    return f"Archived {len(archive_entries)} letters"
