window.addEventListener("load", function decc_faqcheck_onLoad() {
	window.removeEventListener("load", decc_faqcheck_onLoad, false);

	if(document.getElementById("noticePop")){
		FaqCheck.initTimer();
	}
});

let FaqCheck = {
	timer : null,
	initTimer : function(){
		this.timer = setInterval(this.check, 30000);
	},
	stopTimer : function(){
		clearInterval(this.timer);
	},
	check : function(){
		FaqCheck.getFaq(function(ret){
			if(ret != "error"){
				//console.log(ret);
				//document.getElementById("noticePop").style.visibility != "visible"
				if(ret.visibleStyle != ""){
					document.getElementById("noticePop").setAttribute("style", ret.visibleStyle);
					document.getElementById("noticePop_infoCnt").textContent = ret.infoCnt;
					document.getElementById("noticePop_ansCnt").textContent = ret.ansCnt;
				}
			}
		});
	},
	getFaq : function(callback){
		try{
			let url = "lib/faq.php?mode=1";

			let xhr = new XMLHttpRequest();

			xhr.onload = function(aEvent) {
				let res = xhr.responseText;
				if(res != null && res != ""){
					//console.log(res);
					callback(JSON.parse(res));
				}
			};

			xhr.onerror = function(aEvent) {
				callback("error");
			};

			xhr.ontimeout = function(aEvent) {
				callback("error");
			};

			// 非同期
			xhr.open("GET", url, true);
			xhr.setRequestHeader('Pragma', 'no-cache');
			xhr.setRequestHeader('Cache-Control', 'no-cache');
			xhr.setRequestHeader('If-Modified-Since', 'Thu, 01 Jun 1970 00:00:00 GMT');
			//xhr.timeout = 5000;
			xhr.send();

		}catch(e){
			callback("error");
		}
	}
}