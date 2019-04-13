# ========================================================
# 1. Chọn tất cả và bỏ chọn tất cả
# ========================================================

=======================================================================================================
=========================================== AUTHOU : TUANDV ===========================================
=======================================================================================================

Để table trong div này:********************************************************************************
	<div class="row">
	    <div class="col-12" id="data-table">

	    </div>
	</div>

Thêm thẻ vào table*************************************************************************************
	<th style="width: 30px;"><input onclick="check_uncheck_all(this);" type="checkbox" name="checkAll" id="check_all"></th>

	<td class="td-check"><input type="checkbox" name="check_all_item" class="checkbox"></td>

LƯU Ý: Chỉ đặt tên id của table là: id='table_data' để sử dụng được check all function
	<table id='table_data' class='table-event table table-responsive-sm table-bordered table-hover is-loadfirst'>
	
******************************************************************************************************
function delete_item(id) {
if(confirm('are you sure ?')) {
  //1. Show loading bar and hide message box
  show_loading_bar();

  //3. Call Add a new site method by Ajax
  $.ajax({
    type: "POST",
    url: "/management/site/ajax_abc",
    dataType: "html",
    data : { id : id, 'csrfmiddlewaretoken' : '{{ csrf_token }}' },
    success : function(response) {
      load_data();
    },
    error: function(xhr, status, e) {
      hide_loading_bar();
    }
  });
}
}

*******************************************************************************************************
function del() {
    name = "";
    count = 0;
    var site_id = $('.checkbox:checked').map(function(){
        count++;
        var name_site = $(this).data("name");
        name = name +" "+ name_site + ",";
        return $(this).val();
    }).get().join(',');

    if (site_id == "") {
        show_error_message("message", "Please select at least one item !!!")
    }else if (confirm('Are you sure delete:' + name.substring (0, name.length-1) + '?')){
        //1. Show loading bar and hide message box
        show_loading_bar("message");
        $("#table_data_wrapper").addClass("d-none");
        //3. Call Add a new site method by Ajax
        $.ajax({
            type: "POST",
            url: "/report/setting/del",
            dataType: "html",
            data : { site_id : site_id, 'csrfmiddlewaretoken' : '{{ csrf_token }}' },
            success : function(response) {
                if(response == 0){
                    hide_loading_bar("message");
                    show_error_message("message", "Delete error.");
                    
                }else{
                    show_loading_bar("loading-bar");
                    show_success_message("message", "Delete successfully.");
                    load_data();
                }
            },
            error: function(xhr, status, e) {
            hide_loading_bar();
            }
        });
    }
    //1. Show loading bar and hide message box
    

    //3. Call Add a new site method by Ajax

}