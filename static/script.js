function loadConetnt(length, list){
    var load = ""
    for(var i = 0 ; i < length ; i++){
        load += "<div class='showContent'><span style='color: gray;'>id:"
        +list[i][0]+"</span><br>";
        if(list[i][2] == "text"){
            load += list[i][1]+"<br><br><a href='javascript:void(0);' onclick='cp("
            +String.fromCharCode(34)+list[i][1]+String.fromCharCode(34)+")'>复制</a><br>";
        }
        else if(list[i][2] == "file"){
            load += list[i][1]+"<br><br><a href='/download/"
            +list[i][1]+"' download='"
            +list[i][1]+"'>下载</a><br>";
        }

        load += "<a href='/remove/"
        +list[i][0]+"'>删除</a></div>";
    }
    document.getElementById("Body").innerHTML = load;
}

function cp(content){
    var tmpInput = document.createElement("textarea");
    tmpInput.value = content.replace(/<br>/g,"\n");
    document.body.appendChild(tmpInput);
    tmpInput.select();
    document.execCommand('copy');
    document.body.removeChild(tmpInput);
}