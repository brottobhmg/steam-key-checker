
import json
import random
import time
import telebot
import steam.webauth as wa

TELEGRAM_TOKEN=""
TELEGRAM_CHATID=""
STEAM_USERNAME=""
STEAM_PASSWORD=""

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)
user = wa.WebAuth(STEAM_USERNAME,STEAM_PASSWORD)

symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
           'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4',
           '5', '6', '7', '8', '9']

def genKey():
    
    x = 0
    newKey = ""
    while x < 17:
        digit = random.randint(0, 34)
        if x == 5 or x == 11:
            newKey += '-'
        else:
            newKey += symbols[digit]
        x += 1
    return newKey

try:
	user.login()
except wa.CaptchaRequired:
	print(user.captcha_url)
	code = input("Please follow the captcha url, enter the code below:\n")
	user.login(captcha=code)
except wa.EmailCodeRequired:
	code = input("Please enter emailed 2FA code:\n")
	user.login(email_code=code)
except wa.TwoFactorCodeRequired:
	code = input("Please enter 2FA code from the Steam app on your phone:\n")
	user.login(twofactor_code=code)

sessionID = user.session.cookies.get_dict()["sessionid"]
print("SessionID: "+sessionID)

while True:
	key=genKey()
	print(key)
	r = user.session.post('https://store.steampowered.com/account/ajaxregisterkey/', data={'product_key' : key, 'sessionid' : sessionID})
	blob = json.loads(r.text)
	#a=open("log.txt","a")
	#a.write(key+" "+json.dumps(blob)+"\n")
	#a.close()

	try:
		errorCode = blob["purchase_result_details"]
		if errorCode==9:
			for item in blob["purchase_receipt_info"]["line_items"]:
				print(key)
				print(item["line_item_description"])
				bot.send_message(TELEGRAM_CHATID,key)
				bot.send_message(TELEGRAM_CHATID,item["line_item_description"])

		# Error codes from https://steamstore-a.akamaihd.net/public/javascript/registerkey.js?v=qQS85n3B1_Bi&l=english
		sErrorMessage = ""
		if errorCode == 14:
			sErrorMessage = 'The product code you\'ve entered is not valid. Please double check to see if you\'ve mistyped your key. I, L, and 1 can look alike, as can V and Y, and 0 and O.'
		elif errorCode == 15:
			sErrorMessage = 'The product code you\'ve entered has already been activated by a different Steam account. This code cannot be used again. Please contact the retailer or online seller where the code was purchased for assistance.'
		elif errorCode == 53:
			sErrorMessage = 'There have been too many recent activation attempts from this account or Internet address. Please wait and try your product code again later.'
		elif errorCode == 13:
			sErrorMessage = 'Sorry, but this product is not available for purchase in this country. Your product key has not been redeemed.'
		elif errorCode == 9:
			sErrorMessage = 'This Steam account already owns the product(s) contained in this offer. To access them, visit your library in the Steam client.'
		elif errorCode == 24:
			sErrorMessage = 'The product code you\'ve entered requires ownership of another product before activation.\n\nIf you are trying to activate an expansion pack or downloadable content, please first activate the original game, then activate this additional content.'
		elif errorCode == 36:
				sErrorMessage = 'The product code you have entered requires that you first play this game on the PlayStation®3 system before it can be registered.\n\nPlease:\n\n- Start this game on your PlayStation®3 system\n\n- Link your Steam account to your PlayStation®3 Network account\n\n- Connect to Steam while playing this game on the PlayStation®3 system\n\n- Register this product code through Steam.'
		elif errorCode == 50: 
			sErrorMessage = 'The code you have entered is from a Steam Gift Card or Steam Wallet Code. Browse here: https://store.steampowered.com/account/redeemwalletcode to redeem it.'
		else:
			sErrorMessage = 'An unexpected error has occurred.  Your product code has not been redeemed.  Please wait 30 minutes and try redeeming the code again.  If the problem persists, please contact <a href="https://help.steampowered.com/en/wizard/HelpWithCDKey">Steam Support</a> for further assistance.';
		print("[ Error ]", sErrorMessage)
		if errorCode==53:
			print("Sleeping 10 minuts...")
			time.sleep(10*60)
	except Exception as e:
		print(e)
