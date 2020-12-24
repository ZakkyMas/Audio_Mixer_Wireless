function PostJson(link, val){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("POST", link, false);
    Httpreq.send(JSON.stringify(val));
}

function GetJson(link){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET", link, false);
    Httpreq.send(null);
    return JSON.parse(Httpreq.responseText);
}

function StatusLogin(){
    var Json = {
        "name": "Login",
        "user": "",
        "pass": ""
    }
    Json["user"] = document.forms["login"]["USERNAME"].value;
    Json["pass"] = document.forms["login"]["PASSWORD"].value;

    if ((Json["user"] == "") | (Json["pass"] == "")){
        return false;
    }

    PostJson("/postJson", JSON.stringify(Json));
    if(GetJson("/getJson?name=Login")["status"] == true){
        return true;
    }
    alert("Username atau Password salah")
    return false;
}
