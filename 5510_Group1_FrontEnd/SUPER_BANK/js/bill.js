var isShowType = false;
var typeArr = [
    {name:"all", title:"all type", value:""},
    {name:"packet", title:"packet", value:""},
    {name:"transfer", title:"transfer", value:""},
    {name:"gathering", title:"gathering", value:""},
    {name:"collection", title:"collection", value:""},
    {name:"consume", title:"consume", value:""},
    {name:"recharge", title:"recharge", value:""},
    {name:"repayment", title:"repayment", value:""},
    {name:"refund", title:"refund", value:""},
]

//生成图标
function generateTable() {
    //实例化图标插件
    var myChart = echarts.init(document.getElementById('table'));
    // 指定图表的配置项和数据
    var option = {
        title: {
            text: 'expand'
        },
        itemStyle: {
            //颜色
            color: 'green'
        },
        tooltip: {},
        // legend: {
        //     data:['销量']
        // },
        xAxis: {
            data: ["January","February","March","April","May","June"]
        },
        yAxis: {},
        series: [{
            name: 'amount',
            type: 'bar',
            data: [6000, 500, 1000, 3000, 5000, 7500]
        }]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

//初始化
$(function(){
    generateTable();
})

//显示、隐藏类型弹窗
function showType() {
    isShowType = !isShowType;
    if(isShowType) {
        $('.bg').addClass('show');
        $('.panel').addClass('show');
    }else {
        $('.bg').removeClass('show');
        $('.panel').removeClass('show');
    }
}

//改变类型
function changeType(index) {
    var type = typeArr[index];
    $("#type_title").html(type.title);
    showType();
}

//改变tab选项卡
function changeTab(obj) {
    $(obj).parent().children('.tab').removeClass('select');
    $(obj).addClass('select');
}