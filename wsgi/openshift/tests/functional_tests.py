
# http://chimera.labs.oreilly.com/books/1234000000754/ch01.html#_obey_the_testing_goat_do_nothing_until_you_have_a_test
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert '8000' in browser.title



browser.quit()
