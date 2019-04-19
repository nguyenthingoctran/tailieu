var start_day = moment().format("YYYY-MM-D");
var end_day = moment().format("YYYY-MM-D");

function split_calendar(calendar_id){
  
}
function init_calendar(div_reportrange) {
  var cb = function (start, end, label) {
    //Hiển thị cho khách hàng tháng/ngày/năm
    $("#" + div_reportrange + " span").html(start.format("YYYY-MM-DD") + " - " + end.format("YYYY-MM-DD")); 
    var date = $("#"+ div_reportrange + " span").text();

  };
  var optionSet1 = {
    dateFormat: "YYYY-MM-DD",
    //startDate: moment().subtract(6, "days"),
    //endDate: moment(),
    startDate: moment().add(1, "days"),
    endDate: moment().add(1, "days"),
    minDate: "01/01/2012",
    maxDate: moment().endOf("day"),
    //Có cái này thì range mới chạy được
    dateLimit: {
      days: 365
    },
    //hiển thị để chọn năm,  tháng
    showDropdowns: true,
    //Hiển thị cái cột  tuần ở bên cạnh
    showWeekNumbers: true,
    // timePicker: false,
    // timePickerIncrement: 1,
    // timePicker12Hour: true,
    //Luôn hiện cái bảng dù có chọn là 7 ngày, 1 tháng
    alwaysShowCalendars: true,
    ranges: {
      Today: [moment(), moment()],
      Yesterday: [moment().subtract(1, "days"), moment().subtract(1, "days")],
      "Last 7 Days": [moment().subtract(6, "days"), moment()],
      "Last 30 Days": [moment().subtract(29, "days"), moment()],
      "This Month": [moment().startOf("month"), moment().endOf("month")],
      "Last Month": [
        moment()
          .subtract(1, "month")
          .startOf("month"),
        moment()
          .subtract(1, "month")
          .endOf("month")
      ]
    },
    // opens: 'left',
    buttonClasses: ["btn btn-default"],
    applyClass: "btn-small btn-primary",
    cancelClass: "btn-small",
    format: "MM/DD/YYYY",
    separator: " to ",
    locale: {
      applyLabel: "Submit",
      cancelLabel: "Clear",
      fromLabel: "From",
      toLabel: "To",
      customRangeLabel: "Custom",
      daysOfWeek: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
      monthNames: [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
      ]
    }
  };
  //Đặt dữ liệu mặc định cho Chart
  $("#"+ div_reportrange).daterangepicker(optionSet1, cb);
  $("#"+ div_reportrange + " span").html(moment().format("YYYY-MM-DD") + " - " + moment().format("YYYY-MM-DD"));

  // Lấy dữ liệu start_date and end_date
  var date = $("#"+ div_reportrange + " span").text();
}