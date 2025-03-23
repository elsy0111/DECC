window.addEventListener("load", function decc_common_onLoad() {
	window.removeEventListener("load", decc_common_onLoad, false);

	let pageTop = document.getElementById("pageTop");
	if(pageTop){
		window.addEventListener("scroll", function(){
			let scrollVolY = window.scrollY;
			if(scrollVolY > 100){
				pageTop.style.display = "block";
			}else{
				pageTop.style.display = "none";
			}
		});

		pageTop.addEventListener("click", function(){
			window.scroll({top: 0, behavior: 'smooth'});
		});
	}

	//var form = document.getElementsByTagName('form')[0];
	//if(form){
	//	form.addEventListener('keypress', function(event){
	//		if(event.target.tagName == "INPUT" && event.key === 'Enter'){
	//			event.preventDefault();
	//		}
	//	});
	//}

});

let Common = {
	cbcp : function(val){
		if(!navigator.clipboard){
			this.showMsg("クリップボードへのコピーが失敗しました");
		}

		navigator.clipboard.writeText(val).then(function(){
			Common.showMsg("クリップボードにコピーしました");
		});
	},
	showMsg : function(msg){
		let div = document.createElement("div");
		div.setAttribute("class", "toast");
		div.style.visibility = "visible";
		div.style.right = 15 + "px";

		let p = document.createElement("p");
		p.textContent = msg;
		div.appendChild(p);
		document.body.appendChild(div);

		setTimeout(function(){
			document.body.removeChild(div);
		}, 2000);
	}
}
