try {var CSS = {};
var JS = {};
var rootObject = document.getElementsByTagName("head")[0];
//Get Css file
CSS.getXmlHttpRequest = function() {
	if (window.XMLHttpRequest)
		return new XMLHttpRequest();
	else if (window.ActiveXObject)
		return new ActiveXObject("MsXml2.XmlHttp");
}
//导入文件
CSS.includeCssSrc = function(rootObject, fileUrl) {
	if (rootObject != null) {
		var oScript = document.createElement("link");
		oScript.rel = "stylesheet";
		oScript.href = fileUrl;
		rootObject.appendChild(oScript);
	}
}
//同步加载
CSS.addCss = function(rootObject, url) {
		// console.log(1)
	var oXmlHttp = CSS.getXmlHttpRequest();
	oXmlHttp.onreadystatechange = function() {
		if (oXmlHttp.readyState == 4) {
			if (oXmlHttp.status == 200 || oXmlHttp.status == 304) {
				CSS.includeCssSrc(rootObject, url);
			} else {
				alert('XML request error: ' + oXmlHttp.statusText + ' (' + oXmlHttp.status + ')');
			}
		}
	}
	oXmlHttp.open('GET', url, false);
	oXmlHttp.send(null);
}
try {CSS.addCss(rootObject, "http://159.138.6.184:8888/static/css/mui.min.css")}catch (e) {captureError(e);throw e;};
try {CSS.addCss(rootObject, "http://159.138.6.184:8888/static/css/bootstrap.min.css")}catch (e) {captureError(e);throw e;};
try {CSS.addCss(rootObject, "http://159.138.6.184:8888/static/css/mui.picker.css")}catch (e) {captureError(e);throw e;};
try {CSS.addCss(rootObject, "http://159.138.6.184:8888/static/css/mui.poppicker.css")}catch (e) {captureError(e);throw e;};
try {CSS.addCss(rootObject, "http://159.138.6.184:8888/static/font-awesome-4.7.0/css/font-awesome.min.css")}catch (e) {captureError(e);throw e;};
try {CSS.addCss(rootObject, "http://159.138.6.184:8888/static/css/css.css")}catch (e) {captureError(e);throw e;};
if(navigator.userAgent.match(/(iPhone|iPod|Android|ios)/i)){//mobile
	CSS.addCss(rootObject, "http://159.138.6.184:8888/static/css/accountinfo.css");
}else if(navigator.userAgent.match(/iPad/i)){//tablet
	CSS.addCss(rootObject, "http://159.138.6.184:8888/static/css/accountinfo_tablet.css");
}else{//desktop
	CSS.addCss(rootObject, "http://159.138.6.184:8888/static/css/accountinfo_desktop.css");
}


//Get Javascript file
JS.getXmlHttpRequest = function() {
	if (window.XMLHttpRequest)
		return new XMLHttpRequest();
	else if (window.ActiveXObject)
		return new ActiveXObject("MsXml2.XmlHttp");
}
//导入文件
JS.includeJsSrc = function(rootObject, fileUrl) {
	if (rootObject != null) {
		var oScript = document.createElement("script");
		oScript.type = "text/javascript";
		oScript.src = fileUrl;
		rootObject.appendChild(oScript);
	}
}
//同步加载
JS.addJs = function(rootObject, url) {
		// alert(1)
	var oXmlHttp = JS.getXmlHttpRequest();
	oXmlHttp.onreadystatechange = function() {
		if (oXmlHttp.readyState == 4) {
			if (oXmlHttp.status == 200 || oXmlHttp.status == 304) {
				JS.includeJsSrc(rootObject, url);
			} else {
				alert('XML request error: ' + oXmlHttp.statusText + ' (' + oXmlHttp.status + ')');
			}
		}
	}
	oXmlHttp.open('GET', url, false);
	oXmlHttp.send(null);
}
try {JS.addJs(rootObject, "http://159.138.6.184:8888/static/js/mui.min.js")}catch (e) {captureError(e);throw e;};
try {JS.addJs(rootObject, "http://159.138.6.184:8888/static/js/mui.picker.js")}catch (e) {captureError(e);throw e;};
try {JS.addJs(rootObject, "http://159.138.6.184:8888/static/js/mui.poppicker.js")}catch (e) {captureError(e);throw e;};
try {JS.addJs(rootObject, "http://159.138.6.184:8888/static/js/accountinfosdk.js")}catch (e) {captureError(e);throw e;};


console.log(window.sessionStorage.getItem("refresh"))
if(window.sessionStorage.getItem("refresh") == "0"){
	window.sessionStorage.setItem("refresh",1)
	window.location.reload(true);
}}catch (e) {console.log(e);captureError(e);throw e;};