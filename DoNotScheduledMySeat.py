import requests
import time

print("请输入你的一卡通账号,仅用于座位保护识别")
#hostID = input(">>>")
hostID = "220XXXXXXX"
print("请输入你想抢占保护的区域,仅需要输入大写字母")
#areaID = input(">>>")
areaID = "E"
print("请输入你想抢占保护的座位,仅需要输入阿拉伯数字")
#deskID = input(">>>")
deskID = "88"
print("请输入你想抢占的时间段,上午1,下午2,晚上3,全部0")
#numID = input(">>>")
numID = "3"
print("是否需要自动预约 Y/n")
#isLoad = input(">>>")
isLoad = "Y"

area = {
    'A': "23",
    'B': "21",
    'C': "24",
    'D': "25",
    'E': "116",
    'F': "115",
    'G': "113",
    'H': "114"
}

timeSalt = {
    '1':'%2012%3A00',
    '2':'%2017%3A00',
    '3':'%2023%3A00'
}

todayTime = time.strftime("%Y-%m-%d", time.localtime())
checkUrl = f"https://wxcourse.jxufe.cn/wxlib/wx/data/seatDistribution?venueDistributionId={area[str(areaID)]}&appointmentTime={todayTime}&num="
cancelUrlOne = "https://wxcourse.jxufe.cn/wxlib/wx/cancel?id="
cancelUrlTwo = "https://wxcourse.jxufe.cn/wxlib/wx/release?colleageId=51&appointId="

def Doload(time, seat):
    if time == '0':
        for i in range(1, 4, 1):
            loadUrl = f"https://wxcourse.jxufe.cn/wxlib/wx/appoint?officeCode=jxcjdx&colleageId=51&isPeriod=1&appointType=0&userId={hostID}&seatId={seat}&vdId={area[str(areaID)]}&timeSlot={i}&day={todayTime}&appointTo={timeSalt[str(i)]}"
            requests.get(loadUrl)
        else:
            loadUrl = f"https://wxcourse.jxufe.cn/wxlib/wx/appoint?officeCode=jxcjdx&colleageId=51&isPeriod=1&appointType=0&userId={hostID}&seatId={seat}&vdId={area[str(areaID)]}&timeSlot={time}&day={todayTime}&appointTo={timeSalt[str(i)]}"
            requests.get(loadUrl)

def Cancel(set, host, num):
    Result = requests.get(checkUrl + str(num))
    if isLoad in ['y', 'Y']:
        Doload(time, str(Result.json()['result']['seatInfo'][int(numID) - 1]['id']))
    for Sea in range(int(set) - 3, int(set) + 3, 1):
        MineSeat = Result.json()['result']['seatInfo'][Sea]
        if MineSeat['seat_status'] == '1' and MineSeat['seat_user'] != host:
            Response = requests.get(cancelUrlOne + str(MineSeat['seat_appoint_id']))
            return Response.json()
        elif MineSeat['seat_status'] == '2' and MineSeat['seat_user'] != host:
            Response = requests.get(cancelUrlTwo + str(MineSeat['seat_appoint_id']))
            return Response.json()
        else:
            return

if __name__ == '__main__':
    if numID == '0':
        for i in range(1, 4, 1):
            Cancel(deskID, hostID, i)
    else:
        Cancel(deskID, hostID, numID)
