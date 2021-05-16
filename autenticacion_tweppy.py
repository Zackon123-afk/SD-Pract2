import tweepy

'''
Función utilizada para utilizar la Api de Twitter
'''
def get_auth():
    auth = tweepy.OAuthHandler("G7oVPMZP776iDbfLW6KRIlvg6", "MnH3qXuRHfoJXSzXSPdtneAvLCJ2MslvKskHHq0qvrAdNiUyox")
    auth.set_access_token("1059931089999945729-AAimzlFRpPy6RSQqESCM1XJJZAmtbn", "4Sq5Ga0aLC2PIgdzWWIp5ISY4iNFg6cRshJJpQUv12j9u")
    return auth