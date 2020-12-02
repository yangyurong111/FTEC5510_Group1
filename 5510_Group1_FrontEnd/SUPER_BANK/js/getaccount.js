//获取当前用户account列表
mui.ajax(host + "/deposit/deposit/account/allAccounts/"+customernumber+"/0/10000",{
	dataType:'json',//服务器返回json格式数据
	type:'get',//HTTP请求类型
	timeout:60000,
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
		if (data.code == "200") {
			mui.alert("Loss reporting accepted.", "Success", "OK")
		} else {
			mui.alert("Get accout list failed! The response is: \n" + JSON.stringify(data) + ".", "Error", "OK")
		}
	},
	error:function(xhr,type,errorThrown){
		console.log(type);
		var msg = "Get accout list failed! The response is: \n" + xhr.responseText + "."
		if(type == "timeout"){
			msg = "Get accout list failed. Time out!"
		}
		mui.alert(msg, "Error", "OK")
	}
});