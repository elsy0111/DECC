function checkAns(frm){
	var formdata = new FormData($('#'+frm).get(0));
	frm = document.forms[frm];
	
	// 必須入力のname属性
	var req = Array("val","source");

	// アラート表示用
	var req_nm = Array("回答","ソース");

	// 必須入力の数
	var len=req.length;
	
	for(i=0; i<len; i++){
		var obj=frm.elements[req[i]];

		if(obj.type == "text" || obj.type == "textarea" ){
			if(obj.value == ""){
				// 入力されていなかったらアラート表示
				alert(req_nm[i]+"が入力されていません");

				// 未入力のエレメントにフォーカスを当てる
				frm.elements[req[i]].focus();

				return false;
			}
		}
	}

	//
	var iconArea = document.getElementById("icon_" + frm.q_num.value);
	if(iconArea){
		iconArea.innerHTML = "";
	}
	
	var msgArea = document.getElementById("adispmsg_" + frm.q_num.value);
	if(msgArea){
		msgArea.innerHTML = "<span color='color:red;'>判定中…</span>";
	}
	
	var mboxArea = document.getElementById("message_box_" + frm.q_num.value);
	if(mboxArea){
		mboxArea.innerHTML = "";
	}
	
	var sendBtn = document.querySelector(".email");
	if(sendBtn){
		sendBtn.style.color = "#cccccc"; //#1a49a7
		sendBtn.style.backgroundColor = "#999999"; //#bac8e2
	}

	//必須入力項目が全て入力されている場合はAjaxで送信
	var res = new Array();

	$.ajax({
		type: "POST",
		dataType:"json",
		url:"lib/procon.php",
		async:false,
		cache:false,
		data:{
			 "q_num" : frm.q_num.value,
			 "val"   : frm.val.value,
			 "source"   : frm.source.value
		},
		success:function(res) {
			if(res["msg"] == "OK"){
				//alert("認証OK");
				var mbox = document.getElementById("message_box_"+res["q_num"]);
				var icon = document.getElementById("icon_"+res["q_num"]);
				var adispmsg = document.getElementById("adispmsg_" +res["q_num"]);
				
				//mbox.innerHTML = "<font color='#1a49a7'>"+res["return"]+"</font>";

				if(res["return"] != null || res["return"] != ""){
					mbox.innerHTML = "<font color='#1a49a7'>"+res["return"]+"</font>";
				}else{
					mbox.innerHTML = "<font color='#ff000'>判定エラー<br>管理者にお問い合わせください</font>";
				}

				if(res["judge"] == "true"){
						icon.innerHTML = res["return"];
						icon.style.display = "block";
						adispmsg.innerHTML = res["current_time"];
				}else if(res["judge"] == "error"){
						icon.innerHTML = "エラー";
						icon.style.display = "block";
						adispmsg.innerHTML =  res["current_time"];
				}else {
						icon.innerHTML = "";
						icon.style.display = "none";
						adispmsg.innerHTML = "ここに得点もしくはエラーが表示されます";
				}
				
				if(sendBtn){
					sendBtn.style.color = "#1a49a7";
					sendBtn.style.backgroundColor = "#bac8e2";
				}

				//SessionStorageにデータを詰めておく
				keyName_mbox = "key_" + res["q_num"] + "_message_box";
				sessionStorage.setItem(keyName_mbox,  mbox.innerHTML);

				keyName_judge = "key_" + res["q_num"] + "_judge";
				sessionStorage.setItem(keyName_judge,  icon.innerHTML);

				keyName_adispmsg = "key_" + res["q_num"] + "_adispmsg";
				sessionStorage.setItem(keyName_adispmsg,  adispmsg.innerHTML);

				return false;

			}else if(res["msg"] == "NG"){
				var mbox = document.getElementById("message_box_"+res["q_num"]);
				mbox.innerHTML = "<font color='#ff6933'>"+res["return"]+"</font>";
				return false;
			}else if(res["msg"] == "NOT_LOGIN"){
				window.location.href = res["URL"];
			}
		},
		error:function(XMLHttpRequest, textStatus, errorThrown) {
			// alert(XMLHttpRequest.status+ "\n" + textStatus + "\n" + errorThrown.message);
			var mbox = document.getElementById("message_box_"+frm.q_num.value);
			mbox.style.display = "block";
			mbox.innerHTML = "<font color='#ff6933'>システムエラーです。管理者までご連絡ください。</font>";
			return false;
		}
	});

}

 function getExtension(fileName) {
    var ret;
    if (!fileName) {
      return ret;
    }
    var fileTypes = fileName.split(".");
    var len = fileTypes.length;
    if (len === 0) {
      return ret;
    }
    ret = fileTypes[len - 1];
    return ret;
  }


function getNow() {
	var now = new Date();
	var year = now.getFullYear();
	var mon = now.getMonth()+1; //１を足すこと
	var day = now.getDate();
	var hour = toDoubleDigits(now.getHours());
	var min = toDoubleDigits(now.getMinutes());
	var sec = toDoubleDigits(now.getSeconds());

	//出力用
	var s = year + "/" + mon + "/" + day + " " + hour + ":" + min + ":" + sec ; 
	return s;
}
var toDoubleDigits = function(num) {
  num += "";
  if (num.length === 1) {
    num = "0" + num;
  }
 return num;     
};