from selenium import webdriver

# Set the path to the Chrome WebDriver executable
chrome_driver_path = '/Users/jagatees/Downloads/chromedriver'

# Create a Chrome WebDriver instance
driver = webdriver.Chrome()

# Open YouTube
driver.get('https://www.99.co/singapore/s/rent?bathrooms=any&building_age=any&composite_floor_level=any&composite_furnishing=any&composite_views=any&features_and_amenities=any&has_floor_plan=false&isFilterUnapplied=false&listing_type=rent&main_category=all&map_bounds=1.5827095153768858%2C103.49449749970108%2C1.1090706240313446%2C104.12483807587296&page_num=1&page_size=35&path=%2Fsingapore%2Frent&period_of_availability=any&property_segments=residential&query_coords=1.3039947%2C103.8298507&query_limit=radius&query_type=city&rental_type=all&rooms=any&show_cluster_preview=true&show_description=true&show_future_mrts=true&show_internal_linking=true&show_meta_description=true&show_nearby=true&zoom=11')
