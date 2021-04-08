from datetime import datetime,timedelta
import time
from datetime import timezone
from flask import Flask,request, render_template
from helper import validate
from flask import jsonify
import json

app = Flask(__name__)

@app.route('/index_one')
def index():
    return render_template('index_one.html')


@app.route('/result_one',methods=['POST'])
def result():
    if request.method=='POST':
        start_time=request.form.get('st')
        end_time=request.form.get('et')
        counter=0
        counterAA=0;
        counterAB=0;
        counterBA=0;
        counterBB=0;
        counterCA=0;
        counterCB=0;
        counterDA=0;
        counterDB=0;


## J's Space

## V's Space

        if(validate(start_time) and validate(end_time)):
            start=datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z')
            end=datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
            with open('data2.json') as f:
                data_list = json.load(f)
                shifta_start=datetime.strptime('00:30:01','%H:%M:%S')
                shifta_end=datetime.strptime('08:30:00', '%H:%M:%S')
                shiftb_start=datetime.strptime('08:30:01','%H:%M:%S')
                shiftb_end=datetime.strptime('14:30:00', '%H:%M:%S')
                shiftc_1_start=datetime.strptime('14:30:01','%H:%M:%S')
                shiftc_1_end=datetime.strptime('23:59:59', '%H:%M:%S')
                shiftc_2_start=datetime.strptime('00:00:00','%H:%M:%S')
                shiftc_2_end=datetime.strptime('00:30:00', '%H:%M:%S')
                shifta_start=shifta_start.time()
                shifta_end=shifta_end.time()
                shiftb_start=shiftb_start.time()
                shiftb_end=shiftb_end.time()
                shiftc_1_start=shiftc_1_start.time()
                shiftc_1_end=shiftc_1_end.time()
                shiftc_2_start=shiftc_2_start.time()
                shiftc_2_end=shiftc_2_end.time()
                dbg = True
                if(dbg):
                    print("DEBUG_START")
                    print("Time entered : ", start, " to ", end)
                    print("Shift A : ", shifta_start, " to ", shifta_end)
                    print("Shift B : ", shiftb_start, " to ", shiftb_end)
                    print("Shift C : ", shiftc_1_start, " to ", shiftc_1_end)
                    print("Shift C : ", shiftc_2_start, " to ", shiftc_2_end)
                for item in data_list:
                    t=datetime.strptime(item['time'], '%Y-%m-%d %H:%M:%S')
                    t=t.replace(tzinfo=timezone.utc)
                    if t>=start and t<=end:
                        if(dbg):
                            print("Counter is ", counter, " Item time is : ", item['time'], " t is ", t)
                        nt=t.time()
                        if(item['production_A']==True):
                            if(dbg):
                                print("Found A at counter index : ", counter, ", item is ", item )
                            if(nt>=shifta_start and nt<=shifta_end):
                                counterAA+=1;
                            if(nt>=shiftb_start and nt<=shiftb_end):
                                counterBA+=1;
                            if(nt>=shiftc_1_start and nt<=shiftc_1_end):
                                counterCA+=1;
                            if(nt>=shiftc_2_start and nt<=shiftc_2_end):
                                counterDA+=1;

                        if(item['production_B']==True):
                            if(dbg):
                                print("Found B at counter index : ", counter, ", item is ", item)
                            if(nt>=shifta_start and nt<=shifta_end):
                                counterAB+=1;
                            if(nt>=shiftb_start and nt<=shiftb_end):
                                counterBB+=1;
                            if(nt>=shiftc_1_start and nt<=shiftc_1_end):
                                counterCB+=1;
                            if(nt>=shiftc_2_start and nt<=shiftc_2_end):
                                counterDB+=1;
                        counter+=1

        dic={
                'shiftA':{'production_A_count':counterAA,'production_B_count':counterAB},
                'shiftB':{'production_A_count':counterBA,'production_B_count':counterBB},
                'shiftC':{'production_A_count':counterCA + counterDA,'production_B_count':counterCB + counterDB}

            }
        # jo = json.dumps(dic)


    return jsonify(dic)

app.run(debug=True)
