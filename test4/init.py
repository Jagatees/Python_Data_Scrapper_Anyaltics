# Stuff to fix
# 1) auto create the page_scrape folder (99co)
# 2) fix big on renting room deep crawl only get 115 page even those got 1k rooms seems werid
# 3) Add in deep crawling from 99co (PENDING)
# 4) Start making simple website design for dashboard UI
    # like this kind style - https://codepen.io/ed-demircioglu/pen/PodpLoj
# 5) merger the two json file into one big one , RIS + 99co (merger scrapping / deep crawling)
# 6) loading bar on website
# 7) add docker so everyone can run the project due to selium



from flask import Flask, render_template, request

import scripts.rentingSingpoare.main_page_scrapping as mainone
import scripts.rentingSingpoare.scraperr_multi_threading as maintwo

# 99co - Scrapping
import scripts.co.getpagecount as co_firstpage
import scripts.co.getHTMLfromPage as co_secondpage
import scripts.co.rename_folder as co_thirdpage
import scripts.co.scrap_website as co_fourpage

# 99co - Deep Crawling (PENDING)



app = Flask(__name__)
app.secret_key = 'some key that you will never guess'


user_input_page_count = 0
timer_scrapping_ris = ''
user_input_page_count_co = 0


# DO NOT DELETE THIS HELLO WORLD
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    print('hello world')
    return render_template('index.html')

# Get Value from dropdown
@app.route('/website', methods=['GET', 'POST'])
def website():
    if request.method == 'POST':
        # Get user choices
        selected_option = request.form['my_dropdown']
        # RENTinSINGAPORE
        if selected_option == '1':
            return render_template('index.html', value=mainone.pageCount())
        elif selected_option == '2':
            return render_template('index.html', valueFive=co_firstpage.main())
        
# Get Number from Dropdown 
@app.route('/get_page_count', methods=['POST'])
def get_page_count():
    global user_input_page_count
    selected_option = request.form['my_page']
    user_input_page_count = selected_option
    print(selected_option)  # Print the selected option for debugging
    return render_template('index.html')

# Scrapp Rent in Singapore
@app.route('/scrappingRIS', methods = ['GET', 'POST'])
def scrap_ris():
    global user_input_page_count
    global timer_scrapping_ris
    x = mainone.main(int(user_input_page_count))
    timer_scrapping_ris = x
    return render_template('index.html', valueTwo = x)

# Deep Crawling Rent in Singapore
@app.route('/deepcrawlingRIS', methods = ['GET', 'POST'])
def deepcrawl_ris():
    return render_template('index.html', valueTwo = timer_scrapping_ris, valueThree = maintwo.main())

# get page count 
@app.route('/get_page_count_co', methods=['POST'])
def get_page_count_co():
    global user_input_page_count_co
    selected_option = request.form['my_page_co']
    user_input_page_count_co = selected_option
    print(selected_option)  # Print the selected option for debugging
    return render_template('index.html')

@app.route('/scrapping_co', methods = ['GET', 'POST'])
def scrapping_co():
    global user_input_page_count_co
    x = co_secondpage.main(int(user_input_page_count_co))
    co_thirdpage.renameFiles('page_scrape')
    co_fourpage.main('page_scrape')
    return render_template('index.html', valueSix = x)


if __name__ == "__main__":
    app.run('127.0.0.1', 5003, debug=True)



