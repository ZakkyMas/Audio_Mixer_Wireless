
function GetJson(link){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET", link, false);
    Httpreq.send(null);
    return JSON.parse(Httpreq.responseText);
}

function PostJson(link, val){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("POST", link, false);
    Httpreq.send(JSON.stringify(val));
}

function replaceTarget(name, val){
    var str = document.getElementById(name).innerHTML; 
    var res = str.replace(str, val);
    document.getElementById(name).innerHTML = res;
}

function reMap(curr, oldA, oldB, newA, newB){
    return newA + (newB - newA) * (curr - oldA) / (oldB - oldA);
}

function setSelectBoxByValue(id, val) {
    document.getElementById(id).value = val;
}

function setRange(id, id2, val, oldA, oldB, newA, newB, text){
    var myRange = document.querySelector('#'+id2);
    var myValue = document.querySelector('#'+id);
    myRange.value = val;
    myValue.innerHTML = reMap(val, oldA, oldB, newA, newB) + text;
    myRange.oninput =function(){
        myValue.innerHTML = reMap(myRange.value, oldA, oldB, newA, newB) + text;
    };
}

function setRangeMod(id, id2, val, text){
    function range(val){
        var a = (val-7)*2
        if(isNaN(a)){
            a = 0
        }
        if (a > 0){
            a = '+' + a
        }
        return a
    }

    var myRange = document.querySelector('#'+id2);
    var myValue = document.querySelector('#'+id);
    myRange.value = val;
    myValue.innerHTML = range(val) + text;
    myRange.oninput =function(){
        myValue.innerHTML = range(myRange.value) + text;
    };
}

function void_Audio(){
    var Json = {
        "name": "Audio",
        "inpu": 0,
        "loud": 0, 
        "gain": 0,
        "volu": 0,
        "bass": 0,
        "treb": 0,
        "ba-r": 0,
        "ba-l": 0
    }
    Json["inpu"] = document.forms["Audio"]["InputStereo"].value;
    Json["loud"] = document.forms["Audio"]["InputLoud"].value;
    Json["gain"] = document.forms["Audio"]["InputGain"].value;
    Json["volu"] = document.forms["Audio"]["InputVolume"].value;
    Json["bass"] = document.forms["Audio"]["InputBass"].value;
    Json["treb"] = document.forms["Audio"]["InputTreble"].value;
    Json["ba-r"] = document.forms["Audio"]["InputBalanceR"].value;
    Json["ba-l"] = document.forms["Audio"]["InputBalanceL"].value;
    PostJson("/postJson", JSON.stringify(Json));
    return true
}

function void_Wifi(){
    var Json = {
        "name": "Wifi",
        "mode": 0,
        "user": "",
        "passA": "",
        "passB": ""
    }

    Json["mode"] = document.forms["Wifi"]["ModeWiFi"].value;
    Json["user"] = document.forms["Wifi"]["UserWiFi"].value;
    Json["passA"] = document.forms["Wifi"]["UserWiFiA"].value;
    Json["passB"] = document.forms["Wifi"]["UserWiFiB"].value;

    if (Json["passA"] != Json["passB"]){
        return false;
    }
    PostJson("/postJson", JSON.stringify(Json));
    return true;
}

function void_Profil(){
    var Json = {
        "name": "Profil",
        "userA": "",
        "userB": "",
        "passA": "",
        "passB": "",
        "passC": ""
    }

    Json["userA"] = document.forms["Profil"]["UserLama"].value;
    Json["userB"] = document.forms["Profil"]["UserBaru"].value;
    Json["passA"] = document.forms["Profil"]["PassLama"].value;
    Json["passB"] = document.forms["Profil"]["PassBaruA"].value;
    Json["passC"] = document.forms["Profil"]["PassBaruB"].value;

    if (Json["passB"] != Json["passC"]){
        return false;
    }
    PostJson("/postJson", JSON.stringify(Json));
    return true;
}

function void_Keluar(){
    var Json = {
        "name": "Keluar",
        "status": true
    }
    PostJson("/postJson", JSON.stringify(Json));
    return true;
}

var json_file = GetJson("/b_web.json");
var current_link = "/" + window.location.href.split("/")[3].split('?')[0];

window.onload = function(){
    switch(current_link){
        case "/home":
            replaceTarget("stat_A-0", function(){
                return json_file['wifi']['mode_str'][json_file['wifi']['mode']]
            });
            replaceTarget("stat_A-1", json_file['wifi']['SSID'])

            replaceTarget("stat_B-0", json_file['hardware']['volt']+' Volt')
            replaceTarget("stat_B-1", function(){
                return reMap(json_file['hardware']['volt'], 6.0, 8.4, 0, 100).toFixed(2) + "%";
            });
            replaceTarget("stat_B-2", function(){
                return json_file['hardware']['free'] + ' Byte'
            })
            replaceTarget("stat_B-3", function(){
                return json_file['hardware']['use'] + ' Byte'
            })
            replaceTarget("stat_B-4", function(){
                return json_file['hardware']['freq'] + ' Hz'
            })
            
            replaceTarget("stat_C-0", function(){
                return json_file['audio']['inpu_str'][json_file['audio']['inpu']]
            });
            replaceTarget("stat_C-1", function(){
                return json_file['audio']['loud_str'][json_file['audio']['loud']]
            });
            replaceTarget("stat_C-2", function(){
                return json_file['audio']['gain_str'][json_file['audio']['gain']]
            });
            replaceTarget("stat_C-3", function(){
                return reMap(json_file['audio']['volu'], 0, 63, -78.75, 0) + "dB";
            });
            replaceTarget("stat_C-4", function(){
                var a = (json_file['audio']['bass'] - 7)*2;
                if(isNaN(a)){
                    a = 0
                }
                if (a > 0){
                    a = '+' + a
                }
                return a + 'dB'
            });
            replaceTarget("stat_C-5", function(){
                var a = (json_file['audio']['treb'] - 7)*2;
                if(isNaN(a)){
                    a = 0
                }
                if (a > 0){
                    a = '+' + a
                }
                return a + 'dB'
            });
            replaceTarget("stat_C-6", function(){
                return reMap(json_file['audio']['ba-r'], 0, 31, -38.75, 0) + "dB";
            });
            replaceTarget("stat_C-7", function(){
                return reMap(json_file['audio']['ba-l'], 0, 31, -38.75, 0) + "dB";
            });
            break;
        
        case "/audiomixer":
            setSelectBoxByValue('stat_0', json_file['audio']['inpu']);
            setSelectBoxByValue('stat_1', json_file['audio']['loud']);
            setSelectBoxByValue('stat_2', json_file['audio']['gain']);
            setRange('stat_3', 'stat_4', json_file['audio']['volu'], 0, 63, -78.75, 0, "dB")
            setRangeMod('stat_5', 'stat_6', json_file['audio']['bass'], "dB")
            setRangeMod('stat_7', 'stat_8', json_file['audio']['treb'], "dB")
            setRange('stat_9', 'stat_10', json_file['audio']['ba-r'], 0, 31, -38.75, 0, "dB")
            setRange('stat_11', 'stat_12', json_file['audio']['ba-l'], 0, 31, -38.75, 0, "dB")
            break;

        case "/wifi":
            setSelectBoxByValue('stat_0', json_file['wifi']['mode']);
            break;

        case "/a_profil":
            break
    }
}
