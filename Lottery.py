import requests
import bs4
from sys import argv
import datetime


url = 'http://ketqua.net/'
reps = requests.get(url)

id_tag = ['rs_0_0','rs_1_0','rs_2_0','rs_2_1','rs_3_0','rs_3_1','rs_3_2','rs_3_3','rs_3_4','rs_3_5',
'rs_4_0','rs_4_1','rs_4_2','rs_4_3','rs_5_0','rs_5_1','rs_5_2','rs_5_3','rs_5_4','rs_5_5',
'rs_6_0','rs_6_1','rs_6_2','rs_7_0','rs_7_1','rs_7_2','rs_7_3'
]
tree = bs4.BeautifulSoup(markup=reps.text,features="lxml")
Lottery = []
for i in id_tag:
    tag = tree.find_all(attrs={'id':'{}'.format(i)})[0].text
    Lottery.append(tag)

input_cmd = argv
Lottery_match = []
today = datetime.date.today()
time = {
    'day': today.day,
    'month': today.month,
    'year': today.year
}
for Lot in Lottery:
    for i in input_cmd[1:]:
        if str(i).strip() == Lot[-2:]:
            Lottery_match.append(i)
if not Lottery_match:    
    print('Chúc bạn may mắn lần sau!')
    print('Các giải trong ngày {day} tháng {month} năm {year} là: '.format(**time),Lottery)
else:
    print('Bạn đã trúng lô!')
    print(Lottery_match)
