from instagrapi import Client
import requests
import pprint

ACCOUNT_USERNAME = "vladtit81@gmail.com"
ACCOUNT_PASSWORD = "035184951sS"



def get_token():
    res = requests.get("https://graph.facebook.com/oauth/access_token?"
                 "client_id=642307266875582&"
                 "client_secret=f9e2c372f61afda2049f5f22da66d358&"
                 "grant_type=client_credentials")
    print(res.text)
    return res.json()["access_token"]

if __name__ == "__main__":
    #token = get_token()
    # accounts https://graph.facebook.com/v13.0/me/messages?
    result = requests.post("https://graph.facebook.com/v13.0/me/messages?",
                  json={
                      "access_token": "EAAQ2VMre1SgBANydbtWCJZCUZCdoPS08O3DyO0aZAQHqWEXhIPTRKQVmbtGUrW4t1YSrMcoOsYIIIByZAhoHa1ZCPBlRQ6Lo6Ov8CU7Bp4kW6Eh02c1ozeLgDbvbsmh36MrIZBcYU1QI0M9WYBw8RKGdzv4L8A9Kadh7r21MARamJ61tk1Vus5oZCJo0OBtYR9lCkxGKtruqAZDZD",
                      "recipient": {
                          "id": "6182305963"
                      },
                      "message": {
                          "text": "Test"
                      },
                  })
    # f9e2c372f61afda2049f5f22da66d358 секрет
    # 642307266875582|EIUReRSrS8OpFwvPYfEVYotrQ0M
    # 642307266875582|ddb3b9bcdd13650329068c17561586bc
    # EAAJILNB6kL4BALTj4d2t3vZAPgcp3Pa0E9rmCUAKnZA8F850hkZAnff3zX37HujnoZAB2LpwV5FT6ft2lgS2y9HzdVmTG1LorBZAopWHVPROOTny7ZCAuZBCCZBzHcusPbnfRv5ju4RiWUxhxtLUMfrVsWvpWQqr82TuDu1ihOlnmtYOMLfnYOZBTRzfbvMvyjaZCSwUaZAxkBZCwGVYFfG34E937f9y1V66cTAZD
    # 155589884806869 2 https://graph.facebook.com/v9.0/1555898848068692/conversations?platform=instagram&access_token=EAAJILNB6kL4BALTj4d2t3vZAPgcp3Pa0E9rmCUAKnZA8F850hkZAnff3zX37HujnoZAB2LpwV5FT6ft2lgS2y9HzdVmTG1LorBZAopWHVPROOTny7ZCAuZBCCZBzHcusPbnfRv5ju4RiWUxhxtLUMfrVsWvpWQqr82TuDu1ihOlnmtYOMLfnYOZBTRzfbvMvyjaZCSwUaZAxkBZCwGVYFfG34E937f9y1V66cTAZD

    resu = requests.get("https://graph.facebook.com/v13.0/1555898848068692/conversations?platform=instagram&access_token=EAAQ2VMre1SgBANydbtWCJZCUZCdoPS08O3DyO0aZAQHqWEXhIPTRKQVmbtGUrW4t1YSrMcoOsYIIIByZAhoHa1ZCPBlRQ6Lo6Ov8CU7Bp4kW6Eh02c1ozeLgDbvbsmh36MrIZBcYU1QI0M9WYBw8RKGdzv4L8A9Kadh7r21MARamJ61tk1Vus5oZCJo0OBtYR9lCkxGKtruqAZDZD")
    print(resu.text)

    messages = resu.json()["data"]

    resu = requests.get(
        f"https://graph.facebook.com/v13.0/1555898848068692/conversations/{messages[0]['id']}?platform=instagram&fields=messages&access_token=EAAQ2VMre1SgBANydbtWCJZCUZCdoPS08O3DyO0aZAQHqWEXhIPTRKQVmbtGUrW4t1YSrMcoOsYIIIByZAhoHa1ZCPBlRQ6Lo6Ov8CU7Bp4kW6Eh02c1ozeLgDbvbsmh36MrIZBcYU1QI0M9WYBw8RKGdzv4L8A9Kadh7r21MARamJ61tk1Vus5oZCJo0OBtYR9lCkxGKtruqAZDZD")
    print(pprint.pprint(resu.json()))

    message_id = resu.json()["data"][0]["messages"]["data"][0]["id"]
    resu1 = requests.get(
        f"https://graph.facebook.com/v13.0/1555898848068692/conversations/{message_id}?platform=instagram&access_token=EAAQ2VMre1SgBANydbtWCJZCUZCdoPS08O3DyO0aZAQHqWEXhIPTRKQVmbtGUrW4t1YSrMcoOsYIIIByZAhoHa1ZCPBlRQ6Lo6Ov8CU7Bp4kW6Eh02c1ozeLgDbvbsmh36MrIZBcYU1QI0M9WYBw8RKGdzv4L8A9Kadh7r21MARamJ61tk1Vus5oZCJo0OBtYR9lCkxGKtruqAZDZD")
    print(pprint.pprint(resu1.json()))
    #print(result.text)

    # res = requests.get("https://graph.facebook.com/oauth/access_token?"
    #              "client_id=642307266875582&"
    #              "client_secret=f9e2c372f61afda2049f5f22da66d358&"
    #              "grant_type=client_credentials")
    # print(res.text)


    # cl = Client()
    # cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
    #
    # user_id = cl.user_id_from_username("priem_mirea")
    # print(user_id)
    # medias = cl.user_medias(user_id, 20)
    # print(medias)

    # threads = cl.direct_threads()
    # print(threads)
    # #self.assertTrue(len(threads) > 0)
    # thread = threads[0]
    # messages = cl.direct_messages(thread.id, 2)
    # print(messages)

