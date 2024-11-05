from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time


driver = webdriver.Chrome()

def get_table_data(url, file_name):
	try:
		driver.get(url)

		iframe = WebDriverWait(driver, 15).until(
			EC.presence_of_element_located((By.TAG_NAME, "iframe"))
		)
		driver.switch_to.frame(iframe)

		content_div = WebDriverWait(driver, 15).until(
			EC.presence_of_element_located((By.ID, "content"))
		)

		selectAll_btns = driver.find_elements(By.CLASS_NAME, "variableselector_valuesselect_select_all_imagebutton")

		for btn in selectAll_btns:
			btn.click()

		dropdown = driver.find_element(By.CLASS_NAME, "variableselector_outputformats_dropdown")

		dropdown.click()

		option = dropdown.find_element(By.XPATH, "//option[@value='tableViewSorted']")

		option.click()

		continue_btn = driver.find_element(By.CLASS_NAME, "variableselector_continue_button")

		continue_btn.click()

		time.sleep(5)

		table = driver.find_element(By.ID, "ctl00_ctl00_ContentPlaceHolderMain_cphMain_Table_Table_DataTable")

		headers = [header.text for header in table.find_elements(By.TAG_NAME, "th")]

		rows = []
		for row in table.find_elements(By.TAG_NAME, "tr")[1:]:
				cells = row.find_elements(By.TAG_NAME, "td")
				if cells:
						row_data = [cell.text for cell in cells]
						rows.append(row_data)

		# Write to CSV
		with open(f'{file_name}.csv', 'w', newline='', encoding='utf-8') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow(headers)
				writer.writerows(rows)

		print(f"Table data has been written to '{file_name}.csv'.")

	finally:
		driver.quit()


if __name__ == "__main__":
	url1 = "https://www.gso.gov.vn/px-web-2/?pxid=V0201&theme=D%C3%A2n%20s%E1%BB%91%20v%C3%A0%20lao%20%C4%91%E1%BB%99ng"
	url2 = "https://www.gso.gov.vn/px-web-2/?pxid=V0212-14&theme=D%C3%A2n%20s%E1%BB%91%20v%C3%A0%20lao%20%C4%91%E1%BB%99ng"

	get_table_data(url1, "data_1")
	get_table_data(url2, "data_2")