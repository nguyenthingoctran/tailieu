# ========================================================
# 1. Chọn tất cả và bỏ chọn tất cả
# ========================================================
1.1 Checkbox chọn tất cả
    <input onclick="checkAll(this,'card-footer','checkbox');" id="checkAll"  type="checkbox" value="">
1.2 Checkbox tự chọn
    <input class='checkbox' type='checkbox' name='check_all_item' value='3'/>

      Lưu ý:
      + Đặt class = "check" cho tất cả các checkbox ảnh hưởng
1.3 Đặt hàm này ở ready
	checked_show_button('checkbox', 'card-footer');

1.3 JS:
	1.3.1 Hàm checkAll của checkbox chọn tất cả
	function checkAll(element,div_show,checkbox_item_class){
	  var is_checked = $(element).is(':checked');
	  $('.' + checkbox_item_class).prop('checked', is_checked);
	  if(is_checked == true){
	    $('.' + div_show).fadeIn();
	  }else{
	    $('.' + div_show).fadeOut();
	  }
	}

	1.3.2 Hàm checked_show_button()
	function checked_and_show_button(check_all_id,checkbox_class, div_show, arr_checked = []){
	  $('.' + checkbox_class).change(function(){
	    var status = this.checked;
	    console.log(status);
	    if(status == true){
	      arr_checked.push(status);
	    }else{
	      arr_checked.pop();
	      $('#' + check_all_id).prop('checked',false);
	    }
	    
	    if(arr_checked.length == 0){
	      $('.' + div_show).fadeOut();
	    }else{
	      $('.' + div_show).fadeIn();
	    }
	  });
	}

	



