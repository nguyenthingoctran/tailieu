==================================================================================
================================== EMAIL =========================================
==================================================================================
C1:
	var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/; 
	if(!filter.test(value)){
		alert("Invalid email");
	}else{
		$('#download').css({'pointer-events':'auto','opacity':'1'});
	}

C2:
    $("#txt_internal_email").focusout(function(){
      var internal_email = $("#txt_internal_email").val();
      if (internal_email != ""){
        var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if(!filter.test(internal_email)){
          $("#internal_email").append("<span class='text-danger'>Please enter your email address in format: yourname@example.com </span>")
        }else{
          $("#internal_email span").remove();
        }
      }
    });

============================= SỬ DỤNG TRONG TOOL ============================
<div class="row">
    <div class="col-5">Internal Email <span class="required text-danger">*</span></div>
    <div class="col-7" id="internal_email"><input type="text" class="form-control" id="txt_internal_email" {% if site_detail.internal_email != None %}value="{{site_detail.internal_email}}"{% endif %}></div>
</div> <br>

validation_email("txt_internal_email", "internal_email"); 
--> txt_internal_email : id của input
    internal_email : id của div


==================================================================================
============================== INPUT REQUIRED ====================================
==================================================================================
// Đã viết trong common khi dùng không dùng hai hàm này
// Lưu ý 2 hàm này chỉ là hiển thị và ẩn thông báo lỗi ()
function validate_input_text(div_id){
  $(div_id).append("<span class='text-danger error-required'>Please fill out this field. </span>")
}

function remove_validate_input_text(){
  $(".error-required").remove();
}

// CÁCH DÙNG (Tham khảo trang )
  // HTML: thêm class
  <div class="col-12 error-requried"></div>

// JS
  // Validate
  validate = ''
  var validate_input = $("input[type='text']").each(function(){
    if($(this).val() == ""){
      validate = validate + '0';
      var div_id = $(this).parent().parent().parent().find('.error-requried');
      validate_input_text(div_id);
      btn.stop();
    }
  });