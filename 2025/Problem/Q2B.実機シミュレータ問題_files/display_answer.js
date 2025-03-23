function setElement(fn){

	var message = "";
	if(window.sessionStorage){

		try{
			// keyにデータを保存する
			//keyName = "key_" + document.forms[fn].elements["q_num"].value;
			var keyName = "val_" + document.forms[fn].elements["q_num"].value;

			//改行除去（ ※procon sakuraでは改行を除去しない）
			var val = document.forms[fn].elements["val"].value;
			//val = val.replace(/\r?\n/g,"");
			document.forms[fn].elements["val"].value = val;

			//sessionStorage.setItem(keyName,  document.forms[fn].elements["val"].value);
			sessionStorage.setItem(keyName,val);

			keyName = "source_" + document.forms[fn].elements["q_num"].value;
			sessionStorage.setItem(keyName,  document.forms[fn].elements["source"].value);
			checkAns(fn);

		}catch(e){

			// エラーを出力
			message = fn + "\n" + e;

		}
	}
}

function getElement(q_num){

	var message = "";
	if(window.sessionStorage){

		var fn = "Q" + q_num;
		try{

			//データを取り出す
			var keyName = "val_" + document.forms[fn].elements["q_num"].value;
			if(sessionStorage.getItem(keyName) == null){
				document.forms[fn].elements["val"].value = "";
			}else{
				document.forms[fn].elements["val"].value = sessionStorage.getItem(keyName);
			}
			var keyName = "source_" + document.forms[fn].elements["q_num"].value;
			if(sessionStorage.getItem(keyName) == null){
				document.forms[fn].elements["source"].value = "";
			}else{
				document.forms[fn].elements["source"].value = sessionStorage.getItem(keyName);
			}

			var adispmsg = document.getElementById("adispmsg_" + q_num);
    		var icon = document.getElementById("icon_" + q_num);
			var keyName_judge = "key_" + q_num + "_judge";
			if(sessionStorage.getItem(keyName_judge) == null){
				icon.innerHTML = "";
				icon.style.display = "none";
			//	adispmsg.style.display ="block";
			}else{
				icon.innerHTML = sessionStorage.getItem(keyName_judge);
				icon.style.display = "block";
			//	adispmsg.innerHTML = "";
			//	adispmsg.style.display ="none";
			}

			var mbox = document.getElementById("message_box_" + q_num);
			var keyName_message = "key_" + q_num + "_message_box";
			if(sessionStorage.getItem(keyName_message) == null){
				mbox.innerHTML = "";
			}else{
				mbox.innerHTML = sessionStorage.getItem(keyName_message);
			}

			var adispmsg = document.getElementById("adispmsg_" + q_num);
			var keyName_adispmsg = "key_"  + q_num + "_adispmsg";
			if(sessionStorage.getItem(keyName_adispmsg) == null){
				adispmsg.innerHTML = "ここに結果が表示されます。";
			}else{
				adispmsg.innerHTML = sessionStorage.getItem(keyName_adispmsg);
			}


			///////////////////////////////
			// ブラウザ落としちゃったとき用に最新の判定を取ってくる
			if(icon.innerHTML == ""){

				$.ajax({

					type:"POST",
					dataType:"json",
					url:"lib/accountLogChecker.php",
					async:false,
					cache:false,
					data:{
						 "q" : fn,
						 "q_num" : document.forms[fn].elements["q_num"].value
					},
					success:function(res) {
						console.log(res);
						var mbox = document.getElementById("message_box_"+ q_num);
						var icon = document.getElementById("icon_"+ q_num);
						var adispmsg = document.getElementById("adispmsg_" + q_num);
						mbox.innerHTML = "<font color='#1a49a7'>"+res["return"]+"</font>";

						if(res["judge"] == "true"){
								console.log("judge = true");
								icon.innerHTML = res["return"];
								icon.style.display = "block";
								adispmsg.innerHTML = res["current_time"];
						}else if(res["judge"] == "false"){
								console.log("judge = false");
								icon.innerHTML = "エラー";
								icon.style.display = "block";
								adispmsg.innerHTML = res["current_time"];
						}else {
								icon.innerHTML = "";
								icon.style.display = "none";
								adispmsg.innerHTML = "ここに得点もしくはエラーが表示されます";
						}

						//SessionStorageにデータを詰めておく
						keyName_mbox = "key_" + res["q_num"] + "_message_box";
						sessionStorage.setItem(keyName_mbox,  mbox.innerHTML);

						keyName_judge = "key_" + res["q_num"] + "_judge";
						sessionStorage.setItem(keyName_judge,  icon.innerHTML);

						keyName_adispmsg = "key_" + res["q_num"] + "_adispmsg";
						sessionStorage.setItem(keyName_adispmsg,  adispmsg.innerHTML);

						let txtarea = document.getElementsByTagName("textarea");
						txtarea[0].value = res["ans"];
						txtarea[1].value = res["source"];

						sessionStorage.setItem("val_" + q_num, res["ans"]);
						sessionStorage.setItem("source_" + q_num, res["source"]);

						return false;

					},
					error:function(XMLHttpRequest, textStatus, errorThrown) {
			          //alert(XMLHttpRequest.status+ "\n" + textStatus + "\n" + errorThrown.message);
						//var mbox = document.getElementById("message_box_"+frm.q_num.value);
						var mbox = document.getElementById("message_box_"+ q_num);
						mbox.style.display = "block";
						mbox.innerHTML = "<font color='#ff6933'>システムエラーです。管理者までご連絡ください。</font>";
						return false;
					}
				});
			}
			// ここまで
			////////////////////////////////





		}catch(e){

			// エラーを出力
			message = fn + "\n" + e;

		}
	}
}

//Drag&Drop
	/*
function fDragOver(e){
		e.preventDefault();//決まり文句
}
// ドロップ
function fDrop(e,qno){
	e.preventDefault();//決まり文句

	var fileInput = document.getElementById('ansfile_'+qno);
	var files = e.dataTransfer.files;
  fileInput.files = files;
}
	*/
