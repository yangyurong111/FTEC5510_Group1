var mask=mui.createMask();
mui.ajax(host + "/deposit-experience/deposit/account/accountDetails/",{
	data:data,
	dataType:'json',//服务器返回json格式数据
	type:'post',//HTTP请求类型
	timeout:10000,//超时时间设置为10秒；
	headers:{
		'accept':'*/*',
		'token':token,
		'clientid':clientid,
		'messageid':messageid,
		'Content-Type':'application/json'
		},
	beforeSend: function() {
		plus.nativeUI.showWaiting("Loading…", "div");
		mask.show();
	},
	complete: function() {
		plus.nativeUI.closeWaiting();
		mask.close();
	},
	success:function(data){
		
	},
	error:function(xhr,type,errorThrown){
		console.log(type);
		mui.alert("Get account info failed! The response is: \n" + xhr.responseText + ".", "Error", "OK")
	}
});