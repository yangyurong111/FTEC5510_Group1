//Global Host Configuration
window.localStorage.setItem("host", "http://{{Platform_API_Gateway_Host}}")
const host = window.localStorage.getItem("host")
const messageid = "006f7113e5fa48559549c4dfe74e2cd6";
const clientid = "devin"
const customernumber = "{{Your Customer Number}}"
const currency = "HKD"
const transactionccy = "HKD"
const termperiodlist = {
	"1day":{
		"time":1,
		"type":"d"
	},
	"1week":{
		"time":1,
		"type":"w"
	},
	"2weeks":{
		"time":2,
		"type":"w"
	},
	"1month":{
		"time":1,
		"type":"M"
	},
	"2months":{
		"time":2,
		"type":"M"
	},
	"3months":{
		"time":3,
		"type":"M"
	},
	"6months":{
		"time":6,
		"type":"M"
	},
	"9months":{
		"time":9,
		"type":"M"
	},
	"12months":{
		"time":1,
		"type":"y"
	}
}
const currencypickerdata = [{
	value: currency,
	text: currency
}]
const merchantNumberpickerdata = [{
	value: merchantNumber,
	text: merchantNumber
}]
const transactionccypickerdata = [{
	value: transactionccy,
	text: transactionccy
}]
const debitAccountNumberpickerdata = [
	{
		value: savingaccount1,
		text: savingaccount1
	}
]
const tdAccountNumberpickerdata = [{
	value: TDaccount,
	text: TDaccount
}]
const accountpickerdata1 = [
	{
		value: savingaccount1,
		text: savingaccount1
	},
	{
		value: currentaccount,
		text: currentaccount
	}
]
const accountpickerdata2 = [
	{
		value: savingaccount1,
		text: savingaccount1
	},
	{
		value: savingaccount2,
		text: savingaccount2
	},
	{
		value: currentaccount,
		text: currentaccount
	}
]
const accountdetailpickerdata = [{
			value: savingaccount1,
			text: savingaccount1
		},
		{
			value: savingaccount2,
			text: savingaccount2
		},
		{
			value: currentaccount,
			text: currentaccount
		},
		{
			value: SettlementAccount1,
			text: SettlementAccount1
		},
		{
			value: TDaccount,
			text: "Term Deposite: " + TDaccount
		},
		{
			value: creditcardnumber2,
			text: "Credit Card: " + creditcardnumber2
		},
		{
			value: creditcardnumber1,
			text: "Credit Card: " + creditcardnumber1
		},
		{
			value: fxaccount,
			text: "Foreign Exchange: " + fxaccount
		},
		{
			value: mutualfundaccount,
			text: "Mutual Fund: " + mutualfundaccount
		},
		// {
		// 	value: preciousmetal,
		// 	text: "Precious Metal: " + preciousmetal
		// },
		{
			value: stockaccount,
			text: "Stock: " + stockaccount
		}
		]

	!function(window) {
		var ua = window.navigator.userAgent.toLowerCase(),
			reg = /msie|applewebkit.+safari/;
		if (reg.test(ua)) {
			var _sort = Array.prototype.sort;
			Array.prototype.sort = function(fn) {
				if (!!fn && typeof fn === 'function') {
					if (this.length < 2) return this;
					var i = 0,
						j = i + 1,
						l = this.length,
						tmp, r = false,
						t = 0;
					for (; i < l; i++) {
						for (j = i + 1; j < l; j++) {
							t = fn.call(this, this[i], this[j]);
							r = (typeof t === 'number' ? t :
									!!t ? 1 : 0) > 0 ?
								true : false;
							if (r) {
								tmp = this[i];
								this[i] = this[j];
								this[j] = tmp;
							}
						}
					}
					return this;
				} else {
					return _sort.call(this);
				}
			};
		}
	}(window);

//对输入金额进行校验
function clearNoNum(obj) {
	obj.value = obj.value.replace(/[^\d.]/g, ""); //清除"数字"和"."以外的字符
	obj.value = obj.value.replace(/^\./g, ""); //验证第一个字符是数字而不是字符          
	obj.value = obj.value.replace(/\.{2,}/g, "."); //只保留第一个.清除多余的       
	obj.value = obj.value.replace(".", "$#$").replace(/\./g, "").replace("$#$", ".");
	obj.value = obj.value.replace(/^(\-)*(\d+)\.(\d\d).*$/, '$1$2.$3'); //只能输入两个小数
}

//金额格式化
function decimal_format(number, decimals, dec_point, thousands_sep,round_tag) {
   /**
		* number：需要处理的数字；
		* decimals：保留几位小数，默认两位，可不传；
		* dec_point：小数点符号，默认为‘.’，可不传；
		* thousands_sep：千分位符号，默认为‘,’，可不传;
		* round_tag:舎入方式，默认为四舍五入（'round'），可不传； 向上取值（'ceil'）；向下取值（'floor'）;
		*/
    number = (number + '').replace(/[^0-9+-Ee.]/g, '');
    decimals = decimals || 2; //默认保留2位
    dec_point = dec_point || "."; //默认是'.';
    thousands_sep = thousands_sep || ","; //默认是',';
    round_tag = round_tag || "round"; //默认是四舍五入
    var n = !isFinite(+number) ? 0 : +number,
        prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
        sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
        dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
        s = '',
        toFixedFix = function (n, prec) {
  
            var k = Math.pow(10, prec);
            console.log();
  
            return '' + parseFloat(Math[round_tag](parseFloat((n * k).toFixed(prec*2))).toFixed(prec*2)) / k;
        };
    s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
    var re = /(-?\d+)(\d{3})/;
    while (re.test(s[0])) {
        s[0] = s[0].replace(re, "$1" + sep + "$2");
    }
    if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
    }
    return s.join(dec);
}
 
 //小数转百分比
 function toPercent(point){
    var str=Number(point*100).toFixed(2);
    str+="%";
    return str;
}
var mask = mui.createMask();
//获取当前用户account列表
function getaccoutlist(){
	var token = plus.storage.getItem("token")
	mui.ajax(host + "/deposit-experience/deposit/account/allAccounts/"+customernumber+"/0/10000",{
		dataType:'json',//服务器返回json格式数据
		type:'post',//HTTP请求类型
		timeout:60000,
		async:false,
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
			console.log(JSON.stringify(data))
			if (data.code == "200") {
				plus.storage.setItem("savingaccountlist",JSON.stringify(data.data.saving))
				plus.storage.setItem("currentaccountlist",JSON.stringify(data.data.current))
				plus.storage.setItem("termDepositaccountlist",JSON.stringify(data.data.termDeposit))
				plus.storage.setItem("fexaccountlist",JSON.stringify(data.data.fex))
				plus.storage.setItem("stockaccountlist",JSON.stringify(data.data.stock))
				plus.storage.setItem("mutualFundaccountlist",JSON.stringify(data.data.mutualFund))
				plus.storage.setItem("preciousMetalaccountlist",JSON.stringify(data.data.preciousMetal))
				plus.storage.setItem("creditCardaccountlist",JSON.stringify(data.data.creditCard))
				plus.storage.setItem("loanaccountlist",JSON.stringify(data.data.loan))
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
}

/**
 * 获取本周、本季度、本月、上月的开始日期、结束日期
 */
var now = new Date(); //当前日期
var nowDayOfWeek = now.getDay(); //今天本周的第几天
var nowDay = now.getDate(); //当前日
var nowMonth = now.getMonth(); //当前月
var nowYear = now.getYear(); //当前年
nowYear += (nowYear < 2000) ? 1900 : 0; //
var lastMonthDate = new Date(); //上月日期
lastMonthDate.setDate(1);
lastMonthDate.setMonth(lastMonthDate.getMonth() - 1);
var lastYear = lastMonthDate.getYear();
var lastMonth = lastMonthDate.getMonth();
var nextMonthDate = new Date(); //下月日期
nextMonthDate.setDate(1);
nextMonthDate.setMonth(nextMonthDate.getMonth() + 1);
var nextYear = nextMonthDate.getYear();
var nextMonth = nextMonthDate.getMonth();
//格式化日期：yyyy-MM-dd
function formatDate(date) {
    var myyear = date.getFullYear();
    var mymonth = date.getMonth() + 1;
    var myweekday = date.getDate();
    if (mymonth < 10) {
        mymonth = "0" + mymonth;
    }
    if (myweekday < 10) {
        myweekday = "0" + myweekday;
    }
    return (myyear + "-" + mymonth + "-" + myweekday);
}
//获得某月的天数
function getMonthDays(myMonth) {
    var monthStartDate = new Date(nowYear, myMonth, 1);
    var monthEndDate = new Date(nowYear, myMonth + 1, 1);
    var days = (monthEndDate - monthStartDate) / (1000 * 60 * 60 * 24);
    return days;
}
//获得本季度的开始月份
function getQuarterStartMonth() {
    var quarterStartMonth = 0;
    if (nowMonth < 3) {
        quarterStartMonth = 0;
    }
    if (2 < nowMonth && nowMonth < 6) {
        quarterStartMonth = 3;
    }
    if (5 < nowMonth && nowMonth < 9) {
        quarterStartMonth = 6;
    }
    if (nowMonth > 8) {
        quarterStartMonth = 9;
    }
    return quarterStartMonth;
}
//获得本周的开始日期
function getWeekStartDate() {
    var weekStartDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek);
    return formatDate(weekStartDate);
}
//获得本周的结束日期
function getWeekEndDate() {
    var weekEndDate = new Date(nowYear, nowMonth, nowDay + (6 - nowDayOfWeek));
    return formatDate(weekEndDate);
}
//获得上周的开始日期
function getLastWeekStartDate() {
    var weekStartDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek - 7);
    return formatDate(weekStartDate);
}
//获得上周的结束日期
function getLastWeekEndDate() {
    var weekEndDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek - 1);
    return formatDate(weekEndDate);
}
//获得本月的开始日期
function getMonthStartDate() {
    var monthStartDate = new Date(nowYear, nowMonth, 1);
    return formatDate(monthStartDate);
}
//获得本月的结束日期
function getMonthEndDate() {
    var monthEndDate = new Date(nowYear, nowMonth, getMonthDays(nowMonth));
    return formatDate(monthEndDate);
}
//获得上月开始时间
function getLastMonthStartDate() {
    var lastMonthStartDate = new Date(nowYear, lastMonth, 1);
    return formatDate(lastMonthStartDate);
}
//获得上月结束时间
function getLastMonthEndDate() {
    var lastMonthEndDate = new Date(nowYear, lastMonth, getMonthDays(lastMonth));
    return formatDate(lastMonthEndDate);
}
//获得下月开始时间
function getNextMonthStartDate() {
    var nextMonthStartDate = new Date(nowYear, nextMonth, 1);
    return formatDate(nextMonthStartDate);
}
//获得下月结束时间
function getNextMonthEndDate() {
    var nextMonthEndDate = new Date(nowYear, nextMonth, getMonthDays(nextMonth));
    return formatDate(nextMonthEndDate);
}
//获得本季度的开始日期
function getQuarterStartDate() {
    var quarterStartDate = new Date(nowYear, getQuarterStartMonth(), 1);
    return formatDate(quarterStartDate);
}
//或的本季度的结束日期
function getQuarterEndDate() {
    var quarterEndMonth = getQuarterStartMonth() + 2;
    var quarterStartDate = new Date(nowYear, quarterEndMonth,
            getMonthDays(quarterEndMonth));
    return formatDate(quarterStartDate);
}
//获取当月和之前的月份
function gethistorymonth(num){
	//创建现在的时间
	var data=new Date();
	//获取年
	var year=data.getFullYear();
	//获取月
	var mon=data.getMonth()+1;
	var arry=new Array();
	var pickerdata = new Array();
	
	if(mon<10){
		mon="0"+mon;
	}
	pickerdata.push({
			text:year+"-"+mon,
			value:year+"-"+mon
		})
	for(var i=0;i<num;i++){
		mon=mon-1;
		if(mon<=0){
			year=year-1;
			mon=mon+12;
		}
		if(mon<10){
			mon="0"+mon;
		}
		
		arry[i]=year+"-"+mon;
		pickerdata.push({
			text:arry[i],
			value:arry[i]
		})
	}
	
	return pickerdata;
}
//获取所选月份下一个月的第一天
//data为YYYY-MM
function getnextmonthtime(data){
	//创建现在的时间
	var origindate = data.replace(/[\r-]/g,"/");
	var originyear = Number(origindate.split("/")[0]);
	var originmonth = Number(origindate.split("/")[1]);
	var nextmonth = originmonth+1;
	
	if(nextmonth > 12){
		originyear = toString(nextmonth+1);
		nextmonth = "01";
	}
	return new Date(originyear+"/"+nextmonth+"/01 00:00:00").getTime();
}
			
//生成Credit Card account下拉菜单
function getcreditcardnumberpickerdata(){
	var list = plus.storage.getItem("creditCardaccountlist")
	var accountlist = JSON.parse(list);
	var pickerdata = [];
	for(var i=0;i<accountlist.length;i++){
		if(accountlist[i].accountStatus == "A"){
			pickerdata.push({
				text:accountlist[i].accountNumber,
				value:accountlist[i].accountNumber
			})
		}
	}
	return pickerdata;
}

//生成Saving account下拉菜单
function getsavingnumberpickerdata(){
	var list = plus.storage.getItem("savingaccountlist")
	var accountlist = JSON.parse(list);
	var pickerdata = [];
	for(var i=0;i<accountlist.length;i++){
		if(accountlist[i].accountStatus == "A"){
			pickerdata.push({
				text:accountlist[i].accountNumber,
				value:accountlist[i].accountNumber
			})
		}
	}
	return pickerdata;
}

//生成current account下拉菜单
function getcurrentnumberpickerdata(){
	var list = plus.storage.getItem("currentaccountlist")
	var accountlist = JSON.parse(list);
	var pickerdata = [];
	for(var i=0;i<accountlist.length;i++){
		if(accountlist[i].accountStatus == "A"){
			pickerdata.push({
				text:accountlist[i].accountNumber,
				value:accountlist[i].accountNumber
			})
		}
	}
	return pickerdata;
}

//生成termDeposit account下拉菜单
function gettermdepositnumberpickerdata(){
	var list = plus.storage.getItem("termDepositaccountlist")
	var accountlist = JSON.parse(list);
	var pickerdata = [];
	for(var i=0;i<accountlist.length;i++){
		if(accountlist[i].accountStatus == "A"){
			pickerdata.push({
				text:accountlist[i].accountNumber,
				value:accountlist[i].accountNumber
			})
		}
	}
	return pickerdata;
}

//生成fex account下拉菜单
function getfexnumberpickerdata(){
	var list = plus.storage.getItem("fexaccountlist")
	var accountlist = JSON.parse(list);
	var pickerdata = [];
	for(var i=0;i<accountlist.length;i++){
		if(accountlist[i].accountStatus == "A"){
			pickerdata.push({
				text:accountlist[i].accountNumber,
				value:accountlist[i].accountNumber
			})
		}
	}
	return pickerdata;
}

//生成stock account下拉菜单
function getstocknumberpickerdata(){
	var list = plus.storage.getItem("stockaccountlist")
	var accountlist = JSON.parse(list);
	var pickerdata = [];
	for(var i=0;i<accountlist.length;i++){
		if(accountlist[i].accountStatus == "A"){
			pickerdata.push({
				text:accountlist[i].accountNumber,
				value:accountlist[i].accountNumber
			})
		}
	}
	return pickerdata;
}

//生成mutualFund account下拉菜单
function getmutualfundnumberpickerdata(){
	var list = plus.storage.getItem("mutualFundaccountlist")
	var accountlist = JSON.parse(list);
	var pickerdata = [];
	for(var i=0;i<accountlist.length;i++){
		if(accountlist[i].accountStatus == "A"){
			pickerdata.push({
				text:accountlist[i].accountNumber,
				value:accountlist[i].accountNumber
			})
		}
	}
	return pickerdata;
}

//生成preciousMetal account下拉菜单
function getpreciousmetalnumberpickerdata(){
	var list = plus.storage.getItem("preciousMetalaccountlist")
	var accountlist = JSON.parse(list);
	var pickerdata = [];
	for(var i=0;i<accountlist.length;i++){
		if(accountlist[i].accountStatus == "A"){
			pickerdata.push({
				text:accountlist[i].accountNumber,
				value:accountlist[i].accountNumber
			})
		}
	}
	return pickerdata;
}
