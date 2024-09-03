from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from multiprocessing import Pool, Manager, cpu_count
from tools.file import FileManager
from market_research.scraper._scraper_scheme import Scraper

class SonyModelScraper(Scraper):
    def __init__(self, headless=True, output_prefix="sony_model_info", input_dir="input", output_dir="results", verbose=False, wait_time=2):
        """
        Initialize the SonyModelScraper.

        Parameters:
        - headless (bool): Run the browser in headless mode.
        - output_prefix (str): Prefix for the output file name.
        - input_dir (str): Directory for input files.
        - output_dir (str): Directory for output files.
        - verbose (bool): Enable verbose logging.
        - wait_time (int): Time to wait for pages to load (in seconds).
        """
        super().__init__(enable_headless=headless, export_prefix=output_prefix, input_folder_path=input_dir, output_folder_path=output_dir)
        self.verbose = verbose
        self.wait_time = wait_time
        self.file_manager = FileManager
        self.log_dir = "logs/sony/models"
        if self.verbose:
            FileManager.delete_dir(self.log_dir)
            FileManager.make_dir(self.log_dir)

    def scrape_model_data(self, return_as_dataframe=True, mark_missing_year=True):
        series_url_dict = Manager().dict()
        model_info_dict = {}
        series_urls = self._collect_series_urls()

        print(f"Collecting models using {cpu_count()} processes.")
        print("Website scan completed.")
        print(f"Total series found: {len(series_urls)}")

        with Pool(cpu_count()) as pool:
            # Series URLs에서 모델 URL을 수집합니다.
            pool.starmap(self._collect_models_from_series, [(url, series_url_dict) for url in series_urls])

            print(f"Total models found: {len(series_url_dict)}")
            print("Collecting specifications...")

            # 모델 스펙을 수집합니다.
            pool.starmap(self._collect_model_specs, [(model_url, model_info_dict, series_name) for series_name, model_url in series_url_dict.items()])

        if self.verbose:
            print("\n")
            for model_name, url in model_info_dict.items():
                print(f"{model_name}: {url}")

        if return_as_dataframe:
            df_models = pd.DataFrame.from_dict(model_info_dict).T
            if mark_missing_year:
                df_models['year'] = df_models['year'].fillna("2024")
            df_models.to_json(self.output_folder / 's_scrape_model_data.json', orient='records', lines=True)
            FileManager.df_to_excel(df_models.reset_index(), file_name=self.output_xlsx_name, sheet_name="raw_na", mode='w')
            return df_models
        else:
            return model_info_dict
        

    def _collect_series_urls(self) -> set:
        """
        Scroll the main page to collect series URLs.

        Returns:
        - set: A set of series URLs.
        """
        base_url = "https://electronics.sony.com/tv-video/televisions/c/all-tvs/"
        url_prefix = "https://electronics.sony.com/"
        scroll_increment = 200
        series_urls = set()
        max_attempts = 5

        for _ in range(2):  # Number of page scan iterations
            for attempt in range(max_attempts):
                driver = self.web_driver.get_chrome()
                try:
                    driver.get(url=base_url)
                    time.sleep(self.wait_time)
                    total_scroll_height = self.web_driver.get_scroll_distance_total()
                    current_scroll_position = 0

                    while current_scroll_position < total_scroll_height:
                        page_source = driver.page_source
                        soup = BeautifulSoup(page_source, 'html.parser')
                        product_links = soup.find_all('a', class_="custom-product-grid-item__product-name")

                        for link in product_links:
                            series_urls.add(url_prefix + link['href'].strip())

                        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
                        time.sleep(self.wait_time)
                        current_scroll_position += scroll_increment
                    break
                except Exception as e:
                    if self.verbose and attempt + 1 == max_attempts:
                        print(f"Failed to collect base URLs: {base_url}")
                finally:
                    driver.quit()
        return series_urls

    def _collect_models_from_series(self, series_url: str, model_urls_dict):
        """
        Extract all model URLs from a given series URL.

        Parameters:
        - series_url (str): The URL of the series.
        - model_urls_dict (dict): Dictionary to store model URLs.
        """
        series_name = self.file_manager.get_name_from_url(series_url)
        model_dir = f"{self.log_dir}/{series_name}"
        timestamp_today = self.file_manager.get_datetime_info(include_time=False)
        url_timestamp = self.file_manager.get_name_from_url(series_url)
        max_attempts = 5

        models = {}
        for attempt in range(max_attempts):
            driver = self.web_driver.get_chrome()
            try:
                driver.get(url=series_url)
                time.sleep(self.wait_time)

                model_elements = driver.find_element(By.XPATH, '//*[@id="PDPOveriewLink"]/div[1]/div/div/div[2]/div/app-custom-product-summary/div[2]/div/div[1]/app-custom-product-variants/div/app-custom-variant-selector/div/div[2]')
                url_elements = model_elements.find_elements(By.TAG_NAME, 'a')

                for element in url_elements:
                    model_url = element.get_attribute('href')
                    model_name = self.file_manager.get_name_from_url(model_url)
                    models[model_name] = model_url.strip()
                break
            except Exception as e:
                if self.verbose and attempt + 1 == max_attempts:
                    print(f"Failed to collect models for series: {series_url}")
                    self.file_manager.make_dir(model_dir)
                    driver.save_screenshot(f"./{model_dir}/{url_timestamp}_SeriesCollectionError_{timestamp_today}.png")
            finally:
                driver.quit()

        if self.verbose:
            print(f"SONY {series_name[4:]} series: {len(models)} models found")

        for model, url in models.items():
            if self.verbose:
                print(f'{model}: {url}')

        model_urls_dict.update(models)

    def _collect_model_specs(self, model_url: str, model_data_dict: dict, model_name: str):
        """
        Extract global specifications from a given model URL.

        Parameters:
        - model_url (str): The URL of the model.
        - model_data_dict (dict): Dictionary to store model specifications.
        - model_name (str): The name of the model.
        """
        max_attempts = 10
        driver = None

        if self.verbose:
            print("Connecting to:", model_url)

        for attempt in range(max_attempts):
            try:
                driver = self.web_driver.get_chrome()
                driver.get(url=model_url)
                series_name = self.file_manager.get_name_from_url(model_url)
                model_dir = f"{self.log_dir}/{series_name}"
                timestamp_today = self.file_manager.get_datetime_info(include_time=False)
                url_timestamp = self.file_manager.get_name_from_url(model_url)

                if self.verbose:
                    self.file_manager.make_dir(model_dir)
                    driver.save_screenshot(f"./{model_dir}/{url_timestamp}_0_Model_{timestamp_today}.png")
                time.sleep(2)

                try:
                    model_name = driver.find_element(By.XPATH, '//*[@id="cx-main"]/app-product-details-page/div/app-custom-product-intro/div/div/div[1]/div/span').text.split(":")[-1].strip()
                except Exception as e:
                    if self.verbose and attempt + 1 == max_attempts:
                        print(f"Failed to extract model name: {model_url}")
                        self.file_manager.make_dir(model_dir)
                        driver.save_screenshot(f"./{model_dir}/{url_timestamp}_ModelNameError_{timestamp_today}.png")

                try:
                    description = driver.find_element(By.XPATH, '//*[@id="PDPOveriewLink"]/div[1]/div/div/div[2]/div/app-custom-product-summary/div[2]/div/div[1]/app-custom-variant-selector/div/app-custom-variant-description').text.strip()
                except Exception as e:
                    if self.verbose and attempt + 1 == max_attempts:
                        print(f"Failed to extract description: {model_url}")
                        self.file_manager.make_dir(model_dir)
                        driver.save_screenshot(f"./{model_dir}/{url_timestamp}_DescriptionError_{timestamp_today}.png")
                    description = ""

                try:
                    price = driver.find_element(By.XPATH, '//*[@id="PDPOveriewLink"]/div[1]/div/div/div[2]/div/app-custom-product-summary/div[2]/div/div[1]/app-custom-product-price/div/div[2]').text.strip()
                except Exception as e:
                    if self.verbose and attempt + 1 == max_attempts:
                        print(f"Failed to extract price: {model_url}")
                        self.file_manager.make_dir(model_dir)
                        driver.save_screenshot(f"./{model_dir}/{url_timestamp}_PriceError_{timestamp_today}.png")
                    price = ""

                try:
                    images = driver.find_element(By.XPATH, '//*[@id="PDPOveriewLink"]/div[1]/div/div/div[2]/div/app-custom-product-summary/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/a').get_attribute('href').strip()
                except Exception as e:
                    if self.verbose and attempt + 1 == max_attempts:
                        print(f"Failed to extract images: {model_url}")
                        self.file_manager.make_dir(model_dir)
                        driver.save_screenshot(f"./{model_dir}/{url_timestamp}_ImageError_{timestamp_today}.png")
                    images = ""

                model_specs = {
                    'name': model_name,
                    'description': description,
                    'price': price,
                    'images': images
                }
                model_data_dict[model_name] = model_specs
                break

            except Exception as e:
                if self.verbose and attempt + 1 == max_attempts:
                    print(f"Failed to collect specifications: {model_url}")
            finally:
                if driver:
                    driver.quit()
        return model_data_dict



# from bs4 import BeautifulSoup
# import pickle
# import time
# import pandas as pd
# from tqdm import tqdm
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from multiprocessing import Process, Manager, cpu_count
# from tools.file import FileManager
# from market_research.scraper._scaper_scheme import Scraper

# class ModelScraper_s(Scraper):
#     def __init__(self, enable_headless=True,
#                  export_prefix="sony_model_info_web", intput_folder_path="input",  output_folder_path="results",
#                  verbose: bool = False, wait_time=2):
#         """
#         Initialize the instance with the specified configuration.

#         Parameters:
#         enable_headless (bool): Whether to run the browser in headless mode. Default is True.
#         export_prefix (str): Prefix for export file names. Default is "sony_model_info_web".
#         intput_folder_path (str): Path to the input folder. Default is "input".
#         output_folder_path (str): Path to the output folder. Default is "results".
#         verbose (bool): If True, enables tracking logs. Default is False.
#         wait_time (int): Time to wait for page load in seconds. Default is 1.

#         If tracking_log is enabled:
#         Deletes the existing log directory and creates a new one.
#         """

#         super().__init__(enable_headless=enable_headless, export_prefix=export_prefix,  intput_folder_path=intput_folder_path, output_folder_path=output_folder_path)

#         self.tracking_log = verbose
#         self.wait_time = wait_time
#         self.file_manager = FileManager
#         self.log_dir = "logs/sony/models"
#         if self.tracking_log:
#             FileManager.delete_dir(self.log_dir)
#             FileManager.make_dir(self.log_dir)

#     def get_models_info(self, format_df:bool=True, temporary_year_marking=False):
#         """
#         Collect model information from URLs and return the data in the desired format.

#         Parameters:
#         format_df (bool): If True, return the result as a DataFrame and save it to an Excel file. Default is True.
#         fastmode (bool): If True, skips collecting global specifications for faster processing. Default is False.
#         temporary_year_marking (bool): If True, temporarily mark the year as "2024" for models without a year. Default is False.

#         Returns:
#         pd.DataFrame or dict: A DataFrame of model information if format_df is True, otherwise a dictionary.
#         """
        
#         url_series_dict = {}
#         visit_url_dict = {}   
#         processes = []
#         max_processes = cpu_count()
#         manager = Manager()
#         dict_models = manager.dict()
#         url_series_dict = manager.dict()
        
#         print(f"collecting models with {max_processes} processes")
#         url_series_set = self._get_url_series()
#         print("The website scan has been completed.")
#         print(f"number of total series: {len(url_series_set)}")
        
#         for url in url_series_set:
#             if len(processes) >= max_processes:
#                 for process in processes:
#                     process.join()
#                 processes = []
#             process = Process(target=self._get_models, args=(url, url_series_dict))
#             processes.append(process)
#             process.start()
            
#         print("number of total model:", len(url_series_dict)) 
#         print("collecting spec")

#         for key, url_model in tqdm(url_series_dict.items()):          
#             visit_url_dict[key] = url_model

#             if len(processes) >= max_processes:
#                 for process in processes:
#                     process.join()
#                 processes = []
#             process = Process(target=self._get_global_spec, args=(url_model, dict_models, key))
#             processes.append(process)
#             process.start()
#         for process in processes:
#             process.join()
            
#         if self.tracking_log:
#             print("\n")
#             for model, url in visit_url_dict.items():  print(f"{model}: {url}")

#         if format_df:
#             df_models = pd.DataFrame.from_dict(dict_models).T
#             if temporary_year_marking:
#                 df_models['year'] = df_models['year'].fillna("2024") ## 임시
#             FileManager.df_to_excel(df_models.reset_index(), file_name=self.output_xlsx_name, sheet_name="raw_na", mode='w')
#             return df_models
#         else:
#             return dict_models


#     def _get_url_series(self) -> set:
#         """
#         Get the series URLs by scrolling down the main page.
#         """
#         url = "https://electronics.sony.com/tv-video/televisions/c/all-tvs/"
#         prefix = "https://electronics.sony.com/"
#         step = 200
#         url_series = set()
#         try_total = 5
#         for _ in range(2): #page_checker
#             for cnt_try in range(try_total):
#                 driver = self.web_driver.get_chrome()
#                 try:
#                     driver.get(url=url)
#                     time.sleep(self.wait_time)
#                     scroll_distance_total = self.web_driver.get_scroll_distance_total()
#                     scroll_distance = 0
#                     while scroll_distance < scroll_distance_total:
#                         for _ in range(2):
#                             html = driver.page_source
#                             soup = BeautifulSoup(html, 'html.parser')
#                             elements = soup.find_all('a', class_="custom-product-grid-item__product-name")
#                             for element in elements:
#                                 url_series.add(prefix + element['href'].strip())
#                             driver.execute_script(f"window.scrollBy(0, {step});")
#                             time.sleep(self.wait_time)
#                             scroll_distance += step
#                     break
#                 except Exception as e:
#                     if self.tracking_log:
#                         if cnt_try + 1 == try_total:
#                             print(f"collecting primary url error from {url}")
#                 finally:
#                     driver.quit()
#         return url_series

#     def _get_models(self, url: str, url_series_dict) -> dict:
#         """
#         Extract all model URLs from a given series URL.
#         """
#         model = self.file_manager.get_name_from_url(url)
#         dir_model = f"{self.log_dir}/{model}"
#         stamp_today = self.file_manager.get_datetime_info(include_time=False)
#         stamp_url = self.file_manager.get_name_from_url(url)
        
#         try_total = 5
#         dict_url_models = {}
#         for cnt_try in range(try_total):
#             driver = self.web_driver.get_chrome()
#             driver.get(url=url)
#             time.sleep(self.wait_time)
#             try:
#                 elements = driver.find_element(By.XPATH,
#                                                       '//*[@id="PDPOveriewLink"]/div[1]/div/div/div[2]/div/app-custom-product-summary/div[2]/div/div[1]/app-custom-product-variants/div/app-custom-variant-selector/div/div[2]')

#                 url_elements = elements.find_elements(By.TAG_NAME, 'a')

#                 for url_element in url_elements:
#                     url = url_element.get_attribute('href')
#                     label = self.file_manager.get_name_from_url(url)
#                     dict_url_models[label] = url.strip()
#                 break
#             except Exception as e:
#                 if cnt_try + 1 == try_total:
#                         print(f"Getting series error from {url}")
#                         if self.tracking_log:
#                             self.file_manager.make_dir(dir_model)
#                             driver.save_screenshot(f"./{dir_model}/{stamp_url}_Getting series error_{stamp_today}.png")
#             finally:
#                 driver.quit()
#         if self.tracking_log:
#             print(f"SONY {self.file_manager.get_name_from_url(url)[4:]} series: {len(dict_url_models)}")
#         for key, value in dict_url_models.items():
#             if self.tracking_log:
#                 print(f'{key}: {value}')
                
#         url_series_dict.update(dict_url_models)

#     def _get_global_spec(self, url: str, dict_models:dict, key:str):
#         """
#         Extract global specifications from a given model URL.
#         """
#         try_total = 10
#         driver = None
#         if self.tracking_log:  print(" Connecting to", url)
#         for cnt_try in range(try_total):
#             try:
#                 dict_spec = {}
#                 driver = self.web_driver.get_chrome()
#                 driver.get(url=url)
#                 model = self.file_manager.get_name_from_url(url)
#                 dir_model = f"{self.log_dir}/{model}"
#                 stamp_today = self.file_manager.get_datetime_info(include_time=False)
#                 stamp_url = self.file_manager.get_name_from_url(url)

#                 if self.tracking_log:
#                     self.file_manager.make_dir(dir_model)
#                     driver.save_screenshot(f"./{dir_model}/{stamp_url}_0_model_{stamp_today}.png")
#                 time.sleep(2)
                
#                 try:
#                     model = driver.find_element(By.XPATH,
#                                                 '//*[@id="cx-main"]/app-product-details-page/div/app-custom-product-intro/div/div/div[1]/div/span').text
#                     model = model.split(":")[-1].strip()
#                 except Exception as e:                    
#                     if self.tracking_log:
#                         if cnt_try + 1 == try_total:
#                             print(f"Model extraction failed from {url}")
#                             self.file_manager.make_dir(dir_model)
#                             driver.save_screenshot(f"./{dir_model}/{stamp_url}_Model extraction failed_{stamp_today}.png")
#                     pass
                
#                 try:
#                     description = driver.find_element(By.XPATH, '//*[@id="cx-main"]/app-product-details-page/div/app-custom-product-intro/div/div/div[1]/h1/p').text
#                 except:
#                     description = ""
#                     if self.tracking_log:
#                         print(f"description extraction failed from {url}")
                    
#                 # Extract price
#                 try:
#                     price_now = driver.find_element(By.XPATH,
#                                                     '//*[@id="PDPOveriewLink"]/div[1]/div/div/div[2]/div/app-custom-product-summary/app-product-pricing/div/div[1]/p[1]').text
#                     price_original = driver.find_element(By.XPATH,
#                                                          '//*[@id="PDPOveriewLink"]/div[1]/div/div/div[2]/div/app-custom-product-summary/app-product-pricing/div/div[1]/p[2]').text
#                     price_now = float(price_now.replace('$', '').replace(',', ''))
#                     price_original = float(price_original.replace('$', '').replace(',', ''))
#                     price_gap = price_original - price_now
#                 except:
#                     try:
#                         price_now = driver.find_element(By.XPATH,
#                                                         '//*[@id="PDPOveriewLink"]/div[1]/div/div/div[2]/div/app-custom-product-summary/app-product-pricing/div/div[1]/p').text
#                         price_now = float(price_now.replace('$', '').replace(',', ''))
#                         price_original = price_now
#                         price_gap = 0.0
#                     except:
#                         if self.tracking_log:
#                             print(f"Price extraction failed from {url}")
#                             self.file_manager.make_dir(dir_model)
#                             driver.save_screenshot(f"./{dir_model}/{stamp_url}_Model extraction failed_{stamp_today}.png")
#                         price_now = float('nan')
#                         price_original = float('nan')
#                         price_gap = float('nan')

#                 dict_spec.update({
#                     "model": model,
#                     "description": description,
#                     "price": price_now,
#                     "price_original": price_original,
#                     "price_gap": price_gap,
#                 })
                
#                 dict_spec.update(self._extract_model_info(dict_spec.get("model")))
                
#                 element_spec = driver.find_element(By.XPATH, '//*[@id="PDPSpecificationsLink"]')
#                 self.web_driver.move_element_to_center(element_spec)
#                 if self.tracking_log:
#                     driver.save_screenshot(f"./{dir_model}/{stamp_url}_1_move_to_spec_{stamp_today}.png")
#                 time.sleep(self.wait_time)
#                 element_click_spec = driver.find_element(By.XPATH, '//*[@id="PDPSpecificationsLink"]/cx-icon')
#                 element_click_spec.click()
#                 time.sleep(self.wait_time)
#                 if self.tracking_log:
#                     driver.save_screenshot(
#                         f"./{dir_model}/{stamp_url}_2_after_click_specification_{stamp_today}.png")
                    
#                 for _ in range(3):
#                     try:
#                         # 팝업 닫기 버튼을 기다렸다가 클릭
#                         close_button = driver.find_element(By.XPATH, '//*[@id="contentfulModalClose"]')
#                         close_button.click()
#                         break
#                     except Exception as e:
#                         pass
                    
                        
#                 try:
#                     element_see_more = driver.find_element(By.XPATH,'//*[@id="cx-main"]/app-product-details-page/div/app-product-specification/div/div[2]/div[3]/button')
#                     self.web_driver.move_element_to_center(element_see_more)
#                     if self.tracking_log:
#                         driver.save_screenshot(f"./{dir_model}/{stamp_url}_3_after_click_see_more_{stamp_today}.png")
#                     element_see_more.click()
#                 except:
#                     try:
#                         element_see_more = driver.find_element(By.XPATH,
#                                                                '//*[@id="cx-main"]/app-product-details-page/div/app-product-specification/div/div[2]/div[2]/button')
#                         self.web_driver.move_element_to_center(element_see_more)
#                         if self.tracking_log:
#                             driver.save_screenshot(
#                                 f"./{dir_model}/{stamp_url}_3_after_click_see_more_{stamp_today}.png")
#                         element_see_more.click()
#                     except:
#                         if self.tracking_log:
#                             print("Cannot find the 'see more' button on the page")
#                 time.sleep(self.wait_time)
#                 driver.find_element(By.ID, "ngb-nav-0-panel").click()
#                 for _ in range(15):
#                     elements = driver.find_elements(By.CLASS_NAME,"full-specifications__specifications-single-card__sub-list")
#                     for element in elements:
#                         soup = BeautifulSoup(element.get_attribute("innerHTML"), 'html.parser')
#                         dict_spec.update(self._soup_to_dict(soup))
#                     ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
#                 if self.tracking_log:
#                     driver.save_screenshot(f"./{dir_model}/{stamp_url}_4_end_{stamp_today}.png")
#                 if self.tracking_log:
#                     print(f"Received information from {url}")
#                 dict_models[key] = dict_spec
#                 break
#             except Exception as e:
#                 if self.tracking_log:
#                     if cnt_try + 1 == try_total:
#                         print(f"An error occurred on page 3rd : {model}")

#             finally:
#                 driver.quit()
                
#     def _extract_model_info(self, model):
#         """
#         Extract additional information from the model name.
#         """
#         dict_info = {}
#         dict_info["year"] = model.split("-")[1][-1]
#         dict_info["series"] = model.split("-")[1][2:]
#         dict_info["size"] = model.split("-")[1][:2]
#         dict_info["grade"] = model.split("-")[0]

#         year_mapping = {
#             'L': "2023",
#             'K': "2022",
#             'J': "2021",
#             # Add additional mappings as needed
#         }

#         try:
#             dict_info["year"] = year_mapping.get(dict_info.get("year"))
#         except:
#             dict_info["year"] = None

#         return dict_info

#     def _soup_to_dict(self, soup):
#         """
#         Convert BeautifulSoup soup to dictionary.
#         """
#         try:
#             h4_tag = soup.find('h4').text.strip()
#             p_tag = soup.find('p').text.strip()
#         except :
#             try:
#                 h4_tag = soup.find('h4').text.strip()
#                 p_tag = ""
#             except Exception as e:
#                 print("Parser error", e)
#                 h4_tag = "Parser error"
#                 p_tag = "Parser error"
#         return {h4_tag: p_tag}