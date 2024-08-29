import time
import logging
import datetime
import requests
from xodapi.constants import *
from xodapi.driver_tools import driver_init, CHROME_PATH, CHROME_BIN
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger("XodaAPI")


class XodaWindow:
    def __init__(self, username, password, driver=None):
        self.username = username
        self.password = password
        if not driver:
            self.driver = driver_init(CHROME_PATH=CHROME_PATH, CHROME_BIN=CHROME_BIN)
        else:
            self.driver = driver

        # First Timer Report
        self.trial_present_sessions = {}

    def login(self):
        try:
            logger.info("--- Starting to login ---")
            self.driver.get(XODA_LOGIN_URL)

            # Wait for and find the email input field
            email_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="email"]'))
            )
            password_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

            # Enter email and password
            email_field.send_keys(self.username)
            password_field.send_keys(self.password)

            # Click the login button
            login_button.click()

            # Wait for the user to be visible
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'MuiAvatar-root'))  # Adjust class name if necessary
            )
            logger.info("--- Login completed ---")
        except Exception as e:
            logger.error(f"Error during login: {e}")

    def plan_validation(self, plan_start_type=None, day=None, month=None, year=None):
        plan_start_allowed_types = ["IMMEDIATE", "NEXT_BILLING", "FUTURE_DATE"]
        if plan_start_type not in plan_start_allowed_types:
            raise Exception(f"Did not specify allowed plan start types {str(plan_start_allowed_types)}, received {plan_start_type}")
        if plan_start_type == "FUTURE_DATE":
            if not day or not month or not year:
                raise Exception("Date not specified, even though wanting to start in the future date")
        return True

    def pos_add_plan(self, plan_start_type, plan_type, day=None, month=None, year=None, immediate_activation=False):
        if not self.plan_validation(plan_start_type, day, month, year):
            raise Exception("Did not pass validation while adding plan in POS")
        try:
            logger.info("--- Starting to navigate to POS and select options ---")
            self.driver.get(XODA_POS_URL)

            # Click on the type dropdown item
            type_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mui-component-select-type"]')))
            type_dropdown.click()

            # Select the item labelled "Plan"
            plan_item = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-value="plan"]'))
            )
            plan_item.click()

            if plan_start_type == "FUTURE_DATE":
                # Select the radio button labelled "Future Date"
                future_date_radio = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="add-pos-form"]/div[1]/div[2]/div/div/label/span[1]'))
                )
                future_date_radio.click()

                # Select the date selector
                date_selector = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="add-pos-form"]/div[1]/div[2]/div/div[2]/div/div'))
                )
                date_selector.click()

                # Wait for the calendar to be visible
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.MuiDialogContent-root.MuiPickersModal-dialog')))

                # Click to select the year
                year_button = self.driver.find_element(By.XPATH, '//button[@class="MuiButtonBase-root MuiButton-root MuiButton-text MuiPickersToolbarButton-toolbarBtn"]//h6[@class="MuiTypography-root MuiPickersToolbarText-toolbarTxt MuiTypography-subtitle1"]')
                year_button.click()

                # Select the correct year
                year_to_select = self.driver.find_element(By.XPATH, f'//div[@role="button" and text()="{year}"]')
                year_to_select.click()
                time.sleep(1)

                # Verify the month and navigate if necessary
                while True:
                    month_text = self.driver.find_element(By.CSS_SELECTOR, 'div.MuiPickersSlideTransition-transitionContainer.MuiPickersCalendarHeader-transitionContainer > p')
                    current_month_year = month_text.text.split()
                    current_month = current_month_year[0]
                    current_month_num = datetime.datetime.strptime(current_month, "%B").month
                    current_year = int(current_month_year[1])

                    if current_year == year:
                        # Compare months, assuming month is provided as an integer (1 for January, etc.)
                        if current_month_num == month:
                            break
                        elif current_month_num > month:
                            logger.error("Given month is in the past")
                            return
                        else:
                            next_button = self.driver.find_element(By.CSS_SELECTOR, 'button.MuiButtonBase-root.MuiIconButton-root.MuiPickersCalendarHeader-iconButton[tabindex="0"]')
                            next_button.click()
                            WebDriverWait(self.driver, 5).until(EC.staleness_of(month_text))
                    else:
                        logger.error("Year navigation error")
                        return

                day_to_select_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f'//button[.="{day}"]'))
                    # Assuming the dates are buttons and selectable by text
                )
                day_to_select_element.click()

                # Click the OK button
                ok_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[text()="OK"]'))
                )
                ok_button.click()

                # Click immediate Activation
                if immediate_activation:
                    # Click on the checkbox based on name
                    checkbox = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, 'input[name="is_future_plan_date_activate_imediatly"]'))
                    )
                    checkbox.click()

            if plan_start_type == "IMMEDIATE":
                # Select the radio button labelled "Activate Immediately"
                immediate_radio = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="add-pos-form"]/div[1]/div[2]/label[1]/span[1]'))
                )
                immediate_radio.click()
            if plan_start_type == "NEXT_BILLING":
                # Select the radio button labelled "Next Billing date"
                next_billing_radio = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="add-pos-form"]/div[1]/div[2]/label[2]/span[1]'))
                )
                next_billing_radio.click()

            # Select the plan type from dropdown
            plan_type_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mui-component-select-type_id"]')))
            plan_type_dropdown.click()

            plan_type_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//li[text()="{plan_type}"]'))
            )
            plan_type_option.click()

            # Click the submit button
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary[type="submit"]')))
            submit_button.click()

            logger.info("--- Plan and date selection completed ---")
        except Exception as e:
            logger.error(f"Error during plan and date selection: {e}")


class XodaAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None

    def login(self):
        try:
            logger.info("--- Starting to login ---")
            login_data = {
                "email": self.username,
                "password": self.password
            }

            headers = {
                "Content-Type": "application/json"
            }

            # Perform POST request to login and retrieve token
            response = requests.post(XODA_API_LOGIN_URL, json=login_data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the JSON response to extract the token
            response_json = response.json()
            self.token = response_json.get("token")

            if self.token:
                logger.info("--- Login successful, token acquired ---")
            else:
                logger.error("--- Login failed, no token found ---")
                logger.error(f"Response content: {response.text}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error during login: {e}")
            logger.error(f"Response content: {response.text}")

    def make_api_request(self, endpoint, method='GET', data=None):
        if not self.token:
            self.login()

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        url = f"{XODA_API_BASE_URL}{endpoint}"

        response = requests.request(method, url, headers=headers, json=data)

        if response.status_code == 401 and response.json().get(
                "message") == "Session expired. Please logout then login again.":
            logger.info("--- Token expired, reauthenticating ---")
            self.reauth()
            return self.make_api_request(endpoint, method, data)  # Retry the request

        return response

    def reauth(self):
        logger.info("--- Reauthenticating ---")
        self.login()

    def get_members(self, email=None, first_name=None, phone_number=None, user=True):
        try:
            logger.info("--- Fetching members ---")
            response = self.make_api_request('/api/messages/all-contacts?gym_id=163')

            if response.status_code == 200:
                logger.info("--- Members fetched successfully ---")
                members = response.json()

                if email:               # Filter based on email
                    members = [member for member in members if member.get("email") == email]
                if first_name:          # Filter based on first_name
                    members = [member for member in members if member.get("first_name") == first_name]
                if phone_number:        # Filter based on phone_number (mobile)
                    members = [member for member in members if member.get("mobile") == phone_number]
                if user:                # Filter based on role if user is True
                    members = [member for member in members if member.get("role") == "user"]

                return members
            else:
                logger.error(f"Failed to fetch members, status code: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error during fetching members: {e}")
            return None

    def pause_membership(self, member_id, start_date, end_date, reason="Unable to attend", suspension_fee=0):
        try:
            logger.info(f"--- Pausing membership for member_id: {member_id} ---")

            # Define the URL endpoint with the specific member_id
            endpoint = f'/api/members/{member_id}'

            # Define the payload
            payload = {
                "hold_membership": False,
                "plan_lock_in_fee": [{"id": 113560, "reasonsType": "suspension", "value": suspension_fee}],
                "suspension_end_date": end_date,
                "suspension_reason": reason,
                "suspension_start_date": start_date
            }

            # Make the PUT request
            response = self.make_api_request(endpoint, method='PUT', data=payload)

            if response.status_code == 200:
                logger.info(f"--- Membership paused successfully for member_id: {member_id} ---")
                return response.json()
            else:
                logger.error(f"Failed to pause membership, status code: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error during pausing membership for member_id {member_id}: {e}")
            return None
