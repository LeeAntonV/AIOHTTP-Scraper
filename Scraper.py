import asyncio
import aiohttp
import csv
import time #imported to check time complexity

from bs4 import BeautifulSoup


dict_product = [] 
start_time = time.time()

#Function that exctracts data from website 
async def get_page_data(session,page):
        url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page={page}"

        headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
                }
        async with session.get(url=url, headers=headers) as response:
                
                response_text = await response.text()


                soup = BeautifulSoup(response_text, "lxml")  
                             

                product_card = soup.find_all(class_="col-sm-4 col-lg-4 col-md-4")

 
                for card in product_card:
                    card_title = card.find(class_ = "title").string
                    card_price = card.find(class_ = "pull-right price").string
                    card_caption = card.find("p",class_ = "description").string
                    card_review = card.find("p",class_ = "pull-right").string
                    card_href = "https://webscraper.io" + card.find(class_ = "title").get("href") 
										#storing data into dict
                    dict_product.append({
                          "Name":card_title,
                          "Price":card_price,
                          "Caption":card_caption,
                          "Review":card_review,
                          "Link":card_href
                    })                      
                    print(f"Page:{page}")   

#Function that allows to work with pagination
async def gather_data():
            url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops?"

            headers = {
                    'user-agent': 'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/91.0.4472.77 safari/537.36',
                }

            async with aiohttp.ClientSession() as session:         

                 response = await session.get(url,headers=headers)
                 soup = BeautifulSoup(await response.text(), "lxml")

                 page_count  = soup.find('ul',class_="pagination").find_all('a')[-2]           
                 s = [item for item in page_count]
                 string = " ".join(s)
                 page_num = int(string)

                 tasks = []

                 for page in range(1,page_num +1):
                        task = asyncio.create_task(get_page_data(session,page))
                        tasks.append(task)
                        

                 await asyncio.gather(*tasks)

#Main function that writes all stored data into csv file
def main():
    asyncio.run(gather_data())

    with open("csvfile.csv","w") as file:
            fieldnames = ['Name', 'Price', 'Caption', 'Review','Link']
            writer = csv.writer(file,delimiter = ';',quotechar=' ')
            head_writer = csv.DictWriter(file, delimiter=";", fieldnames = fieldnames)
            head_writer.writeheader()
            for product in dict_product :
                writer.writerow(
                     ( product["Name"], 
                      product["Price"],
                      product["Caption"],
                      product["Review"],
                      product["Link"]
                      )
                )

            finish_time = time.time() - start_time
            print(f"TIME:{finish_time}")   
            input("Press <Enter> to close window")          

if __name__=="__main__":
    main()
