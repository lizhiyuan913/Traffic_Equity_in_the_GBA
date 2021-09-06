import requests,re,time
import pandas as pd
key='6a803535ccaeb1ad3677a7ec2bf80c00'
locationdic={}
def getdic(url):
    count=0
    while True :
        try:
            res = requests.get(url)
            dic = res.json()

            return dic
        except:
            time.sleep(1)
            count+=1
def getxy(address):
    try:
        if address in locationdic:
            return locationdic[address]
        url=f'https://restapi.amap.com/v3/place/text?keywords={address}&offset=20&page=1&key={key}&citylimit=true'
        #res = requests.get(url)
        dic = getdic(url)
        pois=dic['pois']
        location=pois[0]['location']
        locationdic[address]=location
        return location
    except Exception as e:
        print(e)
def getdrive(s,e):

    url=f'https://restapi.amap.com/v3/direction/driving?origin={s}&destination={e}&key={key}'
    # res = requests.get(url)
    dic = getdic(url)
    route=dic['route']['paths']
    distance=int(route[0]['distance'])
    duration=int(route[0]['duration'])//60
    return  distance,duration

try:
    last_dis_df=pd.read_excel('distance.xlsx')
    last_dur_df = pd.read_excel('duration.xlsx')
    print('读取原始数据成功')
except:
    print('读取原始数据失败')

places=['广州市越秀区府前路1号市政府大院', '深圳市民中心c区', '珠海市香洲区人民东路2号', '汕头市金平区跃进路28号', '佛山市禅城区岭南大道北12号', '韶关市浈江区风度北路75号', '河源市源城区沿江中路19号', '梅州市梅江区新中路38号', '惠州市惠城区云山西路6号', '汕尾市城区汕尾大道北市政府办公楼', '东莞市南城胜和鸿福路99号', '中山市松苑路1号', '江门市蓬江区白沙大道西1号', '阳江市江城区东风二路60号', '湛江市赤坎区跃进路67号', '茂名市茂南区油城六路2号', '肇庆市端州区城中路49号', '清远市清城区人民二路18号', '潮州市湘桥区枫春路1号', '揭阳市榕城区临江北路39号', '云浮市云城区世纪大道行政中心']
columns=[' ',]+places
distance_datas=[]
duration_datas=[]
for sindex,sname in enumerate(places):
    distance_oneline=[sname,]
    duration_oneline = [sname,]
    s = getxy(sname)
    for eindex,ename in enumerate(places):
        if ename==sname:
            distance_oneline.append(0)
            duration_oneline.append(0)
        else:

            e = getxy(ename)
            distance, duration = getdrive(s, e)
            try:
                distance=min(distance,last_dis_df.iloc[sindex,eindex+1])
                duration = min(duration, last_dur_df.iloc[sindex, eindex + 1])
            except:
                pass
            distance_oneline.append(distance)
            duration_oneline.append(duration)
    distance_datas.append(distance_oneline)
    duration_datas.append(duration_oneline)
    print(distance_oneline)
    print(duration_oneline)
dis_df=pd.DataFrame(distance_datas,columns=columns)
dur_df=pd.DataFrame(duration_datas,columns=columns)
dis_df.to_excel('distance.xlsx',index=None)
dur_df.to_excel('duration.xlsx',index=None)

