
  function get_start_date_and_end_date(calendar_id){
    var date = $("#" + calendar_id + " span").text();
    list_date = date.split(" - ");
    return {
      'start_date' : list_date[0],
      'end_date' : list_date[1]
    }
  }

  function init_calendar(calendar_id) {
    var cb = function (start, end, label) {
      //Hiển thị cho khách hàng tháng/ngày/năm
      $("#"+ calendar_id +" span").html(start.format("YYYY-MM-DD") + " - " + end.format("YYYY-MM-DD"));
    };
    
    var optionSet1 = {
      dateFormat: "YYYY-MM-DD",
      startDate: moment().subtract(13, "days"),
      endDate: moment(),
      // startDate: moment().add(1, "days"),
      // endDate: moment().add(1, "days"),
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
        "Last 14 Days": [moment().subtract(13, "days"), moment()],
        "Last 30 Days": [moment().subtract(29, "days"), moment()],
        //"This Month": [moment().startOf("month"), moment().endOf("month")],
        "Last Month": [moment().subtract(1, "month").startOf("month"),moment().subtract(1, "month").endOf("month")]
      },
      // opens: 'left',
      buttonClasses: ["btn btn-default"],
      applyClass: "btn-small btn-primary",
      cancelClass: "btn-small btn-danger",
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
    $("#"+ calendar_id).daterangepicker(optionSet1, cb);
    $("#" + calendar_id + " span").html(moment().subtract(13, "days").format("YYYY-MM-DD") + " - " + moment().format("YYYY-MM-DD"));

    //Format date span.drp-selected
    $("#" + calendar_id).click(function(){
      var object_date = get_start_date_and_end_date(calendar_id)
      var start_date = object_date.start_date;
      var end_date = object_date.end_date;
      $('span.drp-selected').html(start_date + ' - ' + end_date);
    });
    // ================================================================================
    // ======= Khi nhấn clear thì set start_date và end_date bằng ngày hiện tại =======
    // ================================================================================
    $("#"+ calendar_id).on('cancel.daterangepicker', function(ev, picker) {
      var startDate = moment().subtract(13, "days").format("MM/DD/YYYY");
      var endDate = moment().format("MM/DD/YYYY");      
      $(this).data('daterangepicker').setStartDate(startDate);
      $(this).data('daterangepicker').setEndDate(endDate);
      $("#" + calendar_id + " span").html(moment().subtract(13, "days").format("YYYY-MM-DD") + " - " + moment().format("YYYY-MM-DD"));
    });   
    console.log("startDate")

  }


  function set_date_calendar(calendar_id, start_date, end_date) {
    // ================================================================================
    // =======  set start_date và end_date  =======
    // ================================================================================

    var start_date_n = moment(start_date.replace('/','-')).format('MM-DD-YYYY');
    var end_date_n = moment(end_date.replace('/','-')).format('MM-DD-YYYY');
    
    $("#"+ calendar_id).data('daterangepicker').setStartDate(start_date);
    $("#"+ calendar_id).data('daterangepicker').setEndDate(end_date);
    $("#" + calendar_id + " span").html( moment(start_date_n).format("YYYY-MM-DD") + " - " + moment(end_date_n).format("YYYY-MM-DD"));

  }
