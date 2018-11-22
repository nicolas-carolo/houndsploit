from selenium import webdriver

# The user open the browser and go to the home page
browser = webdriver.Firefox()
browser.get('http://localhost:8000')

# Check if the page title is equal to 'HoundSploit'
assert 'HoundSploit' in browser.title

# Close the browser
browser.quit()