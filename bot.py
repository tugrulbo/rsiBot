import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from binance.client import Client
import talib as ta
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import math
import json


liste = ['BTCBUSD', 'ETHBUSD', 'BNBBUSD','NEOBUSD', 'LTCBUSD', 'QTUMBUSD', 'ADABUSD', 'XRPBUSD', 'EOSBUSD', 'IOTABUSD', 'XLMBUSD', 'ONTBUSD', 'TRXBUSD', 'ETCBUSD', 'ICXBUSD', 'VETBUSD', 'PAXBUSD', 'LINKBUSD', 'WAVESBUSD', 'BTTBUSD', 'HOTBUSD', 'ZILBUSD', 'ZRXBUSD','BATBUSD', 'XMRBUSD', 'ZECBUSD', 'IOSTBUSD', 'DASHBUSD', 'NANOBUSD', 'OMGBUSD', 'ENJBUSD', 'MATICBUSD', 'ATOMBUSD', 'ONEBUSD', 'ALGOBUSD', 'DOGEBUSD', 'TOMOBUSD', 'CHZBUSD', 'BANDBUSD', 'XTZBUSD', 'RVNBUSD', 'HBARBUSD', 'BCHBUSD', 'WRXBUSD', 'BNTBUSD', 'DATABUSD','SOLBUSD', 'CTSIBUSD', 'KNCBUSD', 'REPBUSD', 'LRCBUSD', 'COMPBUSD', 'SNXBUSD', 'DGBBUSD', 'GBPBUSD', 'SXPBUSD', 'MKRBUSD', 'MANABUSD', 'AUDBUSD', 'YFIBUSD', 'BALBUSD', 'JSTBUSD', 'SRMBUSD', 'ANTBUSD', 'CRVBUSD', 'SANDBUSD', 'OCEANBUSD', 'NMRBUSD', 'DOTBUSD', 'LUNABUSD', 'RSRBUSD', 'TRBBUSD', 'BZRXBUSD', 'SUSHIBUSD', 'YFIIBUSD', 'KSMBUSD', 'EGLDBUSD', 'DIABUSD', 'RUNEBUSD', 'FIOBUSD', 'BELBUSD', 'WINGBUSD', 'UNIBUSD', 'NBSBUSD', 'OXTBUSD', 'SUNBUSD', 'AVAXBUSD', 'HNTBUSD', 'FLMBUSD', 'ORNBUSD', 'UTKBUSD', 'XVSBUSD', 'ALPHABUSD', 'AAVEBUSD', 'NEARBUSD', 'FILBUSD', 'INJBUSD', 'AUDIOBUSD', 'CTKBUSD', 'AKROBUSD', 'AXSBUSD', 'HARDBUSD', 'DNTBUSD', 'STRAXBUSD', 'UNFIBUSD', 'ROSEBUSD', 'AVABUSD', 'XEMBUSD', 'SKLBUSD','GRTBUSD', 'JUVBUSD', 'PSGBUSD', '1INCHBUSD', 'REEFBUSD', 'OGBUSD', 'ATMBUSD', 'ASRBUSD', 'CELOBUSD', 'RIFBUSD', 'BTCSTBUSD', 'TRUBUSD', 'CKBBUSD', 'TWTBUSD', 'FIROBUSD', 'LITBUSD', 'SFPBUSD', 'DODOBUSD', 'CAKEBUSD', 'ACMBUSD', 'BADGERBUSD', 'FISBUSD', 'OMBUSD', 'PONDBUSD', 'DEGOBUSD', 'ALICEBUSD', 'LINABUSD', 'PERPBUSD', 'RAMPBUSD', 'SUPERBUSD', 'CFXBUSD']
liste_json=[]
positive =0
negative =0
print(len(liste))
class BinanceConnection:
    def __init__(self, file):
        self.connect(file)

    """ Creates Binance client """

    def connect(self, file):
        lines = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)


def generateStochasticRSI(close_array, timeperiod, fastk,slowk,slowd):
    # 1) ilk a??ama rsi de??erini hesapl??yoruz.
    rsi = ta.RSI(close_array, timeperiod=timeperiod)

    # 2) ikinci a??amada rsi arrayinden s??f??rlar?? kald??r??yoruz.
    rsi = rsi[~np.isnan(rsi)]

    # 3) ??????nc?? a??amada ise ta-lib stoch metodunu uyguluyoruz.
    stochrsif, stochrsis = ta.STOCH(rsi, rsi, rsi, fastk_period=fastk, slowk_period=slowk, slowd_period=slowd)

    return stochrsif, stochrsis


def getKlines(connection,pair,interval,limit):

    klines = connection.client.get_klines(symbol=pair, interval=interval, limit=limit)
              
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    close = [float(entry[4]) for entry in klines]

    close_array = np.asarray(close) 
    high_array = np.asarray(high)   
    low_array = np.asarray(low) 

    return close_array


def sendTelegramMsg(token,chat_id,msg):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id,text=msg, parse_mode="html") 

if __name__ == '__main__':
    filename = 'credentials.txt'

    connection = BinanceConnection(filename)

    while 1:
        f = open("rsi.json",)
        liste_json = json.load(f)
        print("Coin Sayisi: {}".format(len(liste_json)))

        for i in range(len(liste_json)):
            try:

                # coin listesini atama yap??yor
                pair = liste_json[i]['name']

                # 5 dakikal??k stoch RSI kontrol?? i??in gerekli data
                close_array_5minute = getKlines(connection,pair,"5m",66)
                stochasticRsiF_5minute, stochasticRsiS_5minute = generateStochasticRSI(close_array_5minute, timeperiod=11, fastk=18, slowk=7, slowd=4)  
                print("5dkl??k data i??lendi.")
            
                # 15 dakikal??k stoch RSI kontrol?? i??in gerekli data
                close_array_15minute = getKlines(connection,pair,"15m",66)
                stochasticRsiF_15minute, stochasticRsiS_15minute = generateStochasticRSI(close_array_15minute, timeperiod=11, fastk=18, slowk=6, slowd=4)  
                print("15dkl??k data i??lendi.")

                # 30 dakikal??k stoch RSI kontrol?? i??in gerekli data
                close_array_30minute = getKlines(connection,pair,"30m",66)
                stochasticRsiF_30minute, stochasticRsiS_30minute = generateStochasticRSI(close_array_30minute, timeperiod=11, fastk=18, slowk=6, slowd=4) 
                print("30dkl??k data i??lendi")

                # 1 saatlik stoch RSI kontrol?? i??in gerekli data
                close_array_1h = getKlines(connection,pair,"1h",66)
                stochasticRsiF_1h, stochasticRsiS_1h = generateStochasticRSI(close_array_1h, timeperiod=11, fastk=18, slowk=6, slowd=4) 
                print("1 saatlik data i??lendi")


                # 2 saatlik stoch RSI kontrol?? i??in gerekli data
                close_array_2h = getKlines(connection,pair,"2h",66)
                stochasticRsiF_2h, stochasticRsiS_2h = generateStochasticRSI(close_array_2h, timeperiod=11, fastk=18, slowk=6, slowd=4) 
              
                print("2 saatlik data i??lendi")

                # 4 saatlik stoch RSI kontrol?? i??in gerekli data 
                close_array_4h = getKlines(connection,pair,"4h",66)
                stochasticRsiF_4h, stochasticRsiS_4h = generateStochasticRSI(close_array_4h, timeperiod=11, fastk=18, slowk=6, slowd=4) 
                print("4 saatlik data i??lendi")
                
                if (liste_json[i]['signalSend'] == False):
                    print("Sinyal durumu: False")
                    print(pair)
                    print("15m: ", stochasticRsiF_15minute[-1], stochasticRsiS_15minute[-1])
                    print("30m: ", stochasticRsiF_30minute[-1], stochasticRsiS_30minute[-1])
                    print("1h: ", stochasticRsiF_1h[-1], stochasticRsiS_1h[-1])
                    print("2h: ", stochasticRsiF_2h[-1], stochasticRsiS_2h[-1])
                    print("4h: ", stochasticRsiF_4h[-1], stochasticRsiS_4h[-1])
                    # 15 dakikal??k, 30 dakikal??k, 1 saatlik, 2 saatlik, 4 saatlik grafiklerde rsi de??eri yukar?? y??nl??yse 
                    if (stochasticRsiF_15minute[-1]>stochasticRsiS_15minute[-1]):
                        liste_json[i].update({"name":pair,"price":close_array_15minute[-1],
                            "5m":{
                                "stochRsi_5m":False,
                                "F":stochasticRsiF_5minute[-1],
                                "S":stochasticRsiS_5minute[-1]
                            },
                            "15m":{
                                "stochRsi_15m":True,
                                "F":stochasticRsiF_15minute[-1],
                                "S":stochasticRsiS_15minute[-1]
                                },
                            "30m":{
                                "stochRsi_30m":False,
                                "F":stochasticRsiF_30minute[-1],
                                "S":stochasticRsiS_30minute[-1]
                            },
                            "1h":{
                                "stochRsi_1h":False,
                                "F":stochasticRsiF_1h[-1],
                                "S":stochasticRsiS_1h[-1]
                            },
                            "2h":{
                                "stochRsi_2h":False,
                                "F":stochasticRsiF_2h[-1],
                                "S":stochasticRsiS_2h[-1]
                            },
                            "4h":{
                                "stochRsi_4h":False,
                                "F":stochasticRsiF_4h[-1],
                                "S":stochasticRsiS_4h[-1]
                            }, 
                            "signalSend":False})
                        print("15 dakikal??k grafikte y??kseli?? var")
                        if(stochasticRsiF_30minute[-1]>stochasticRsiS_30minute[-1]):
                            liste_json[i].update({"name":pair,"price":close_array_15minute[-1],
                                "5m":{
                                    "stochRsi_5m":False,
                                    "F":stochasticRsiF_5minute[-1],
                                    "S":stochasticRsiS_5minute[-1]
                                },
                                "15m":{
                                    "stochRsi_15m":True,
                                    "F":stochasticRsiF_15minute[-1],
                                    "S":stochasticRsiS_15minute[-1]
                                    },
                                "30m":{
                                    "stochRsi_30m":True,
                                    "F":stochasticRsiF_30minute[-1],
                                    "S":stochasticRsiS_30minute[-1]
                                },
                                "1h":{
                                    "stochRsi_1h":False,
                                    "F":stochasticRsiF_1h[-1],
                                    "S":stochasticRsiS_1h[-1]
                                },
                                "2h":{
                                    "stochRsi_2h":False,
                                    "F":stochasticRsiF_2h[-1],
                                    "S":stochasticRsiS_2h[-1]
                                },
                                "4h":{
                                    "stochRsi_4h":False,
                                    "F":stochasticRsiF_4h[-1],
                                    "S":stochasticRsiS_4h[-1]
                                }, 
                                "signalSend":False})
                            print("30 dakikal??k grafikte y??kseli?? var")
                            if(stochasticRsiF_1h[-1]>stochasticRsiS_1h[-1]):
                                liste_json[i].update({"name":pair,"price":close_array_15minute[-1],
                                "5m":{
                                        "stochRsi_5m":False,
                                        "F":stochasticRsiF_5minute[-1],
                                        "S":stochasticRsiS_5minute[-1]
                                    },
                                    "15m":{
                                        "stochRsi_15m":True,
                                        "F":stochasticRsiF_15minute[-1],
                                        "S":stochasticRsiS_15minute[-1]
                                        },
                                    "30m":{
                                        "stochRsi_30m":True,
                                        "F":stochasticRsiF_30minute[-1],
                                        "S":stochasticRsiS_30minute[-1]
                                    },
                                    "1h":{
                                        "stochRsi_1h":True,
                                        "F":stochasticRsiF_1h[-1],
                                        "S":stochasticRsiS_1h[-1]
                                    },
                                    "2h":{
                                        "stochRsi_2h":False,
                                        "F":stochasticRsiF_2h[-1],
                                        "S":stochasticRsiS_2h[-1]
                                    },
                                    "4h":{
                                        "stochRsi_4h":False,
                                        "F":stochasticRsiF_4h[-1],
                                        "S":stochasticRsiS_4h[-1]
                                    }, 
                                    "signalSend":False})
                                print("1 saatlik grafikte y??kseli?? var")
                                if(stochasticRsiF_2h[-1]>stochasticRsiS_2h[-1]):
                                        liste_json[i].update({"name":pair,"price":close_array_15minute[-1],
                                            "5m":{
                                                "stochRsi_5m":False,
                                                "F":stochasticRsiF_5minute[-1],
                                                "S":stochasticRsiS_5minute[-1]
                                            },
                                            "15m":{
                                                "stochRsi_15m":True,
                                                "F":stochasticRsiF_15minute[-1],
                                                "S":stochasticRsiS_15minute[-1]
                                                },
                                            "30m":{
                                                "stochRsi_30m":True,
                                                "F":stochasticRsiF_30minute[-1],
                                                "S":stochasticRsiS_30minute[-1]
                                            },
                                            "1h":{
                                                "stochRsi_1h":True,
                                                "F":stochasticRsiF_1h[-1],
                                                "S":stochasticRsiS_1h[-1]
                                            },
                                            "2h":{
                                                "stochRsi_2h":True,
                                                "F":stochasticRsiF_2h[-1],
                                                "S":stochasticRsiS_2h[-1]
                                            },
                                            "4h":{
                                                "stochRsi_4h":False,
                                                "F":stochasticRsiF_4h[-1],
                                                "S":stochasticRsiS_4h[-1]
                                            }, 
                                            "signalSend":False})
                                        print("2 saatlik grafikte y??kseli?? var")
                                        if(stochasticRsiF_4h[-1]>stochasticRsiS_4h[-1]):
                                            liste_json[i].update({"name":pair,"price":close_array_15minute[-1],
                                                "5m":{
                                                    "stochRsi_5m":False,
                                                    "F":stochasticRsiF_5minute[-1],
                                                    "S":stochasticRsiS_5minute[-1]
                                                },
                                                "15m":{
                                                    "stochRsi_15m":True,
                                                    "F":stochasticRsiF_15minute[-1],
                                                    "S":stochasticRsiS_15minute[-1]
                                                    },
                                                "30m":{
                                                    "stochRsi_30m":True,
                                                    "F":stochasticRsiF_30minute[-1],
                                                    "S":stochasticRsiS_30minute[-1]
                                                },
                                                "1h":{
                                                    "stochRsi_1h":True,
                                                    "F":stochasticRsiF_1h[-1],
                                                    "S":stochasticRsiS_1h[-1]
                                                },
                                                "2h":{
                                                    "stochRsi_2h":True,
                                                    "F":stochasticRsiF_2h[-1],
                                                    "S":stochasticRsiS_2h[-1]
                                                },
                                                "4h":{
                                                    "stochRsi_4h":True,
                                                    "F":stochasticRsiF_4h[-1],
                                                    "S":stochasticRsiS_4h[-1]
                                                }, 
                                                "signalSend":False})
                                            print("4 saatlik grafikte y??kseli?? var")
                                            if(stochasticRsiF_5minute[-2]<=stochasticRsiS_5minute[-2]) and (stochasticRsiF_5minute[-1]>stochasticRsiS_5minute[-1]) and min(stochasticRsiF_5minute[-1],stochasticRsiS_5minute[-1]<=50):
                                                liste_json[i].update({"name":pair,"price":close_array_15minute[-1],
                                                    "5m":{
                                                        "stochRsi_5m":True,
                                                        "F":stochasticRsiF_5minute[-1],
                                                        "S":stochasticRsiS_5minute[-1]
                                                        },
                                                    "15m":{
                                                        "stochRsi_15m":True,
                                                        "F":stochasticRsiF_15minute[-1],
                                                        "S":stochasticRsiS_15minute[-1]
                                                        },
                                                    "30m":{
                                                        "stochRsi_30m":True,
                                                        "F":stochasticRsiF_30minute[-1],
                                                        "S":stochasticRsiS_30minute[-1]
                                                    },
                                                    "1h":{
                                                        "stochRsi_1h":True,
                                                        "F":stochasticRsiF_1h[-1],
                                                        "S":stochasticRsiS_1h[-1]
                                                    },
                                                    "2h":{
                                                        "stochRsi_2h":True,
                                                        "F":stochasticRsiF_2h[-1],
                                                        "S":stochasticRsiS_2h[-1]
                                                    },
                                                    "4h":{
                                                        "stochRsi_4h":True,
                                                        "F":stochasticRsiF_4h[-1],
                                                        "S":stochasticRsiS_4h[-1]
                                                    }, 
                                                    "signalSend":False})
                                                
                                                msg = str("<pre> ## Al???? Emri \n StochRSI: Var \n Koin: {} \n Al???? Fiyat??: {} BUSD </pre>".format(pair,close_array_15minute[-1]))
                                                sendTelegramMsg('1698370648:AAFrYdqmcuro6w_XXWvHaSKO_AiADveN9CQ',-1001453204438,msg)
                                                print("5 dakikal??k ??ak????ma oldu")
                                                print("## Al???? Emri  -|- StochRSI: Var -|- Koin: {} -|- Al???? Fiyat??: {} BUSD".format(pair,close_array_15minute[-1]))
                                                
                                        else:   
                                            liste_json[i].update({"name":pair,"price":close_array_15minute[-1],
                                                "5m":{
                                                    "stochRsi_5m":False,
                                                    "F":stochasticRsiF_5minute[-1],
                                                    "S":stochasticRsiS_5minute[-1]
                                                    },
                                                "15m":{
                                                    "stochRsi_15m":True,
                                                    "F":stochasticRsiF_15minute[-1],
                                                    "S":stochasticRsiS_15minute[-1]
                                                    },
                                                "30m":{
                                                    "stochRsi_30m":True,
                                                    "F":stochasticRsiF_30minute[-1],
                                                    "S":stochasticRsiS_30minute[-1]
                                                },
                                                "1h":{
                                                    "stochRsi_1h":True,
                                                    "F":stochasticRsiF_1h[-1],
                                                    "S":stochasticRsiS_1h[-1]
                                                },
                                                "2h":{
                                                    "stochRsi_2h":True,
                                                    "F":stochasticRsiF_2h[-1],
                                                    "S":stochasticRsiS_2h[-1]
                                                },
                                                "4h":{
                                                    "stochRsi_4h":False,
                                                    "F":stochasticRsiF_4h[-1],
                                                    "S":stochasticRsiS_4h[-1]
                                                }, 
                                                "signalSend":False})   
                                else:
                                    liste_json[i].update({"name":pair,"price":close_array_15minute[-1],
                                        "5m":{
                                            "stochRsi_5m":False,
                                            "F":stochasticRsiF_5minute[-1],
                                            "S":stochasticRsiS_5minute[-1]
                                            },
                                        "15m":{
                                            "stochRsi_15m":True,
                                            "F":stochasticRsiF_15minute[-1],
                                            "S":stochasticRsiS_15minute[-1]
                                            },
                                        "30m":{
                                            "stochRsi_30m":True,
                                            "F":stochasticRsiF_30minute[-1],
                                            "S":stochasticRsiS_30minute[-1]
                                        },
                                        "1h":{
                                            "stochRsi_1h":True,
                                            "F":stochasticRsiF_1h[-1],
                                            "S":stochasticRsiS_1h[-1]
                                        },
                                        "2h":{
                                            "stochRsi_2h":False,
                                            "F":stochasticRsiF_2h[-1],
                                            "S":stochasticRsiS_2h[-1]
                                        },
                                        "4h":{
                                            "stochRsi_4h":False,
                                            "F":stochasticRsiF_4h[-1],
                                            "S":stochasticRsiS_4h[-1]
                                        }, 
                                        "signalSend":False})
                            else:
                                liste_json[i].update({"name":pair,"price":close_array_15minute[-1],
                                    "5m":{
                                        "stochRsi_5m":False,
                                        "F":stochasticRsiF_5minute[-1],
                                        "S":stochasticRsiS_5minute[-1]
                                        },
                                    "15m":{
                                        "stochRsi_15m":True,
                                        "F":stochasticRsiF_15minute[-1],
                                        "S":stochasticRsiS_15minute[-1]
                                        },
                                    "30m":{
                                        "stochRsi_30m":True,
                                        "F":stochasticRsiF_30minute[-1],
                                        "S":stochasticRsiS_30minute[-1]
                                    },
                                    "1h":{
                                        "stochRsi_1h":False,
                                        "F":stochasticRsiF_1h[-1],
                                        "S":stochasticRsiS_1h[-1]
                                    },
                                    "2h":{
                                        "stochRsi_2h":False,
                                        "F":stochasticRsiF_2h[-1],
                                        "S":stochasticRsiS_2h[-1]
                                    },
                                    "4h":{
                                        "stochRsi_4h":False,
                                        "F":stochasticRsiF_4h[-1],
                                        "S":stochasticRsiS_4h[-1]
                                    }, 
                                    "signalSend":False})
                        else:
                            liste_json[i].update({"name":pair,"price":close_array_15minute[-1],
                                "5m":{
                                    "stochRsi_5m":False,
                                    "F":stochasticRsiF_5minute[-1],
                                    "S":stochasticRsiS_5minute[-1]
                                    },
                                "15m":{
                                    "stochRsi_15m":True,
                                    "F":stochasticRsiF_15minute[-1],
                                    "S":stochasticRsiS_15minute[-1]
                                    },
                                "30m":{
                                    "stochRsi_30m":False,
                                    "F":stochasticRsiF_30minute[-1],
                                    "S":stochasticRsiS_30minute[-1]
                                },
                                "1h":{
                                    "stochRsi_1h":False,
                                    "F":stochasticRsiF_1h[-1],
                                    "S":stochasticRsiS_1h[-1]
                                },
                                "2h":{
                                    "stochRsi_2h":False,
                                    "F":stochasticRsiF_2h[-1],
                                    "S":stochasticRsiS_2h[-1]
                                },
                                "4h":{
                                    "stochRsi_4h":False,
                                    "F":stochasticRsiF_4h[-1],
                                    "S":stochasticRsiS_4h[-1]
                                }, 
                                "signalSend":False})
                    else:
                        liste_json[i].update({"name":pair,"price":close_array_15minute[-1],
                            "5m":{
                                "stochRsi_5m":False,
                                "F":stochasticRsiF_5minute[-1],
                                "S":stochasticRsiS_5minute[-1]
                                },
                            "15m":{
                                "stochRsi_15m":False,
                                "F":stochasticRsiF_15minute[-1],
                                "S":stochasticRsiS_15minute[-1]
                                },
                            "30m":{
                                "stochRsi_30m":False,
                                "F":stochasticRsiF_30minute[-1],
                                "S":stochasticRsiS_30minute[-1]
                            },
                            "1h":{
                                "stochRsi_1h":False,
                                "F":stochasticRsiF_1h[-1],
                                "S":stochasticRsiS_1h[-1]
                            },
                            "2h":{
                                "stochRsi_2h":False,
                                "F":stochasticRsiF_2h[-1],
                                "S":stochasticRsiS_2h[-1]
                            },
                            "4h":{
                                "stochRsi_4h":False,
                                "F":stochasticRsiF_4h[-1],
                                "S":stochasticRsiS_4h[-1]
                            }, 
                            "signalSend":False})   

                else:
                    print("Sinyal durumu: True")
                    print(pair)
                    print("15m: ", stochasticRsiF_15minute[-1], stochasticRsiS_15minute[-1])
                    print("30m: ", stochasticRsiF_30minute[-1], stochasticRsiS_30minute[-1])
                    print("1h: ", stochasticRsiF_1h[-1], stochasticRsiS_1h[-1])
                    print("2h: ", stochasticRsiF_2h[-1], stochasticRsiS_2h[-1])
                    print("4h: ", stochasticRsiF_4h[-1], stochasticRsiS_4h[-1])
                    if (stochasticRsiF_5minute[-2]>=stochasticRsiS_5minute[-2]) and (stochasticRsiF_5minute[-1]<stochasticRsiS_5minute[-1]):
                        
                        #json dosyas??ndan koinin al??nan fiyat?? al??n??p "bought_price" a atan??yor
                        bought_price = liste_json[i]['price']

                        #mavi, k??rm??z?? ??izgiyi yukar??dan kesiti??i andaki fiyat?? "sell_price" i??ine atan??yor
                        sell_price = close_array_15minute[-1]

                        #kar oran?? i??in y??zdelik hesaplar(burada asl??nda ayr?? hesaplamalar yapmaya gerek yok ancak ileride gerekli olabilir)
                        #kar pozitif i??in yap??lan hesap
                        if(sell_price > bought_price):
                            result = (sell_price-bought_price)*100/bought_price
                            positive = positive + result
                            msg = str("<pre>## Sat???? Emri \n Koin: {} \n Sat???? Fiyat??: {} BUSD \n Kar Oran??: %{}</pre>".format(pair,sell_price,positive))
                            sendTelegramMsg('1651341698:AAFLLI5mypxjDk2ETCj5SUdgNKaeKgcM9L4',-1001410036844,msg)
                           
                        elif(sell_price < bought_price): #kar negatif i??in yap??lan hesap
                            result = (bought_price-sell_price)*100/bought_price
                            negative = negative + result
                            msg = str("<code>## Sat???? Emri \n Koin: {} \n Sat???? Fiyat??: {} BUSD \n Zarar Oran??: %{}</code>".format(pair,sell_price,negative))
                            sendTelegramMsg('1651341698:AAFLLI5mypxjDk2ETCj5SUdgNKaeKgcM9L4',-1001410036844,msg)
                        else:
                            result = 0
                            msg = str("<code>## Sat???? Emri \n Koin: {} \n Sat???? Fiyat??: {} BUSD \n Kar Oran??: %{}</code>".format(pair,sell_price,positive))
                            sendTelegramMsg('1651341698:AAFLLI5mypxjDk2ETCj5SUdgNKaeKgcM9L4',-1001410036844,msg)

                        liste_json[i].update({"name":pair,"price":close_array_15minute[-1],
                            "5m":{
                                "stochRsi_5m":False,
                                "F":stochasticRsiF_5minute[-1],
                                "S":stochasticRsiS_5minute[-1]
                                },
                            "15m":{
                                "stochRsi_15m":False,
                                "F":stochasticRsiF_15minute[-1],
                                "S":stochasticRsiS_15minute[-1]
                                },
                            "30m":{
                                "stochRsi_30m":False,
                                "F":stochasticRsiF_30minute[-1],
                                "S":stochasticRsiS_30minute[-1]
                            },
                            "1h":{
                                "stochRsi_1h":False,
                                "F":stochasticRsiF_1h[-1],
                                "S":stochasticRsiS_1h[-1]
                            },
                            "2h":{
                                "stochRsi_2h":False,
                                "F":stochasticRsiF_2h[-1],
                                "S":stochasticRsiS_2h[-1]
                            },
                            "4h":{
                                "stochRsi_4h":False,
                                "F":stochasticRsiF_4h[-1],
                                "S":stochasticRsiS_4h[-1]
                            }, 
                            "signalSend":False}) 
                
                print("-----------------------------------------------\n")   
            except:
                continue
        
        json1 = json.dumps(liste_json,ensure_ascii=False)
        with open("rsi.json","w",encoding="utf8") as f:
            f.write(json1)
               
 
    



    





