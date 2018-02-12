from selenium import webdriver
from bs4 import BeautifulSoup
from Tkinter import *
import time

# open chorme browswer
driver = webdriver.Chrome('D:\chromedriver_win32\chromedriver')

# open onlinetichu.com
driver.get("http://www.onlinetichu.com/Site/Account/Login")

# log-in
driver.find_element_by_name('loginModel.UserName').send_keys('planteras')
driver.find_element_by_name('loginModel.Password').send_keys('ilfq8732')
driver.find_element_by_xpath('//*[@id="loginForm"]/form/div/div/div/button').click()

# click 'Play Now!'
driver.find_element_by_xpath('//*[@id="quickPlay"]/span').click()


cardList = [[0 for i in range(4)] for j in range(14)]

# Drawing part
root = Tk()
root.title("Tichu Helper")
bgcolor = root.cget('bg')

BG_COLORS = ["Dim Gray", "Cornflower Blue", "Lime Green", "Red"]
COLORS = ["Black", "Blue", "Green", "Red"]
VALUES = ["-","A","K","Q","J","10","9","8","7","6","5","4","3","2"]
labels = []
cardList = [[0 for i in range(4)] for j in range(14)]
running = False

for i in range(len(VALUES)):
	row = []
	for j in range(len(COLORS)):
		label = Label(root, text = COLORS[j] + "-" + VALUES[i])
		label.grid(row = i, column = j, sticky=("N", "S", "E", "W"))
		row.append(label)
	labels.append(row)

labels[0][0].config(text =  "Dragon")
labels[0][1].config(text =  "Phynix")
labels[0][2].config(text =  "MahJong")
labels[0][3].config(text =  "--")

startButton = Button(root, text="Start")
resetButton = Button(root, text="Reset")

startButton.grid(columnspan = 14)
resetButton.grid(columnspan = 15)



def cardReset(event):
	global cardList
	cardList = [[0 for i in range(4)] for j in range(14)]


def cardPop(cardname):
	card = cardname[1:].split("-")
	if card[0] == '6':
		card[0] = '0'
	elif card[0] == '7':
		card[0] = '1'
	elif card[0] == '4':
		card[0] = '2'
	if card[1] == '0':
		card[1] = '15'
	elif card[1] == '1':
		card[1] = '15'

	cardList[eval(card[1]) - 2][eval(card[0])] = 1

def draw():
	for i in range(14):
		for j in range(4):
			if list(reversed(cardList))[i][j] == 1:
				labels[i][j].config(bg = BG_COLORS[j])
			else:
				labels[i][j].config(bg = bgcolor)


def refresh():
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')

	gameField = soup.find("div", id="gameField")
	if gameField:
		tableCards = gameField.find("ul", id="tableCards")

		for card in tableCards.find_all("li"):
			cardPop(card.get('id'))
	draw()

def start(event):
	global running
	if not running:
		running = True
		startButton.config(text = "Running...")
	else:
		running = False
		startButton.config(text = "Start")

startButton.bind("<Button-1>", start)
resetButton.bind("<Button-1>", cardReset)

while(True):
	if running:
		refresh()
	root.update_idletasks()
	root.update()
	time.sleep(0.5)
"""
while(True):
	start = raw_input("Go?")
	if start == 'r':
		cardReset()

	else:
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')

		gameField = soup.find("div", id="gameField")
		if gameField:
			tableCards = gameField.find("ul", id="tableCards")

			for card in tableCards.find_all("li"):
				cardPop(card.get('id'))
			print(cardList)
"""